#!/usr/bin/env python3
#
# Copyright (C) 2021 Amlogic, Inc. All rights reserved.
#
# This source code is subject to the terms and conditions defined in the
# file 'LICENSE' which is part of this source code package.

ALGO = 'gen-prot-aes128'
MRK_NAME = 'DGPK2'
BOOT_STAGE = 2
EK3 = 'a1f9288d5e382b34a2897e9194ee2911'
EK2 = '754ac2fdb002e3fa13407d3367ce293d'
#EK1 = '8b8f5a227bb1c1487d21a0fd6d842833'

TARGET_NAME = 'dac'
MAX_IDX = 100000000
DERIVED_FILE_NUM = 0

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--soc', type = str, required = True, help = 'soc')
	parser.add_argument('--key_tool', type = str, required = True, help = 'vendor key tool path')
	parser.add_argument('--pfpk_hmac_generator', type = str, required = True, help = 'pfpk hmac generator path')
	parser.add_argument('--dgpk2', type = str, required = True, help = 'dgpk2 file or directory')
	parser.add_argument('--pfid', type = str, required = True, help = 'pfid file or directory')
	parser.add_argument('--out_dir', type = str, required = True, help = 'output directory')
	return parser.parse_args()

def derive_one_dac(file_dgpk2, file_pfid, out_dir, idx, key_tool, soc, pfpk_hmac_generator):
	import os
	import sys
	import binascii
	import hmac
	import hashlib

	if int(idx) > MAX_IDX:
		print('the number of files exceeds the limit')
		sys.exit(1)

	f = open(file_dgpk2, 'rb')
	mrk = f.read()
	f.close()

	f = open(file_pfid, 'rb')
	ek1 = f.read()
	f.close()

	# due to the other para aren't supported, can only use "SC2"
	cmd = key_tool + ' ' + ALGO + ' --chipset=SC2' \
	      + ' --mrk=' + bytes.decode(binascii.b2a_hex(mrk)) \
	      + ' --mrk-name=' + MRK_NAME + ' --boot-stage=' + str(BOOT_STAGE) \
	      + ' --ek3=' + EK3 + ' --ek2=' + EK2 \
	      + ' --ek1=' + bytes.decode(binascii.b2a_hex(ek1))
	pfpk = os.popen(cmd).read()[:32]

	cmd = pfpk_hmac_generator + ' -p ' + pfpk
	pfpk_hmac = binascii.unhexlify((os.popen(cmd).read())[:64])

	dac = hmac.HMAC(pfpk_hmac, ek1, hashlib.sha256).digest()

	file_dac = out_dir + '/' + soc + '_' + TARGET_NAME + '_' + idx + '.bin'
	f = open(file_dac, 'wb')
	f.write(dac)
	f.close()

	global DERIVED_FILE_NUM
	DERIVED_FILE_NUM = DERIVED_FILE_NUM + 1
	print(os.path.abspath(file_dac) + ' derived successfully')

def main():
	import os
	import sys

	args = get_args()

	if not os.path.exists(args.key_tool):
		print(args.key_tool + ' not exist')
		sys.exit(1)

	if not os.path.exists(args.pfpk_hmac_generator):
		print(args.pfpk_hmac_generator + ' not exist')
		sys.exit(1)

	if not os.path.exists(args.out_dir):
		os.mkdir(args.out_dir)

	if os.path.isfile(args.dgpk2) and os.path.isfile(args.pfid):
		derive_one_dac(args.dgpk2, args.pfid, args.out_dir, '000000001', args.key_tool, args.soc, args.pfpk_hmac_generator)
	elif os.path.isdir(args.dgpk2) and os.path.isdir(args.pfid):
		for parent, dnames, fnames in os.walk(args.dgpk2):
			for fname in fnames:
				idx = fname[-13 : -4]
				file_pfid = args.pfid + '/' + args.soc + '_pfid_' + idx + '.bin'
				file_dgpk2 = os.path.join(parent, fname)
				if os.path.exists(file_pfid):
					derive_one_dac(file_dgpk2, file_pfid, args.out_dir, idx, args.key_tool, args.soc, args.pfpk_hmac_generator)
	else:
		print('input parameter error')
		sys.exit(1)

	print(str(DERIVED_FILE_NUM) + ' ' + TARGET_NAME + ' files derived successfully')

if __name__ == '__main__':
	main()
