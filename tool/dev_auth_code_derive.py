#!/usr/bin/env python3
#
# Copyright (C) 2022 Amlogic, Inc. All rights reserved.
#
# This source code is subject to the terms and conditions defined in the
# file 'LICENSE' which is part of this source code package.

import sys

GENERATOR_PATH = sys.path[0] + '/dependents/pfpk-hmac-generator/pfpk_hmac_generator'

TARGET_NAME = 'dac'
MAX_IDX = 100000000
DERIVED_FILE_NUM = 0

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--pfpk', type = str, required = True, help = 'pfpk file or directory')
	parser.add_argument('--pfid', type = str, required = True, help = 'pfid file or directory')
	parser.add_argument('--out_dir', type = str, default = './dacs/', help = 'output directory')
	return parser.parse_args()

def derive_one_dac(file_pfpk, file_pfid, out_dir, idx):
	import os
	import sys
	import binascii
	import hmac
	import hashlib

	if int(idx) > MAX_IDX:
		print('the number of files exceeds the limit')
		sys.exit(1)

	f = open(file_pfpk, 'rb')
	pfpk = f.read()
	f.close()

	f = open(file_pfid, 'rb')
	pfid = f.read()
	f.close()

	cmd = GENERATOR_PATH + ' -p ' + bytes.decode(binascii.b2a_hex(pfpk))
	pfpk_hmac = binascii.unhexlify((os.popen(cmd).read())[:64])

	dac = hmac.HMAC(pfpk_hmac, pfid, hashlib.sha256).digest()

	file_dac = out_dir + '/' + TARGET_NAME + '_' + idx + '.bin'
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

	if not os.path.exists(GENERATOR_PATH):
		print(GENERATOR_PATH + ' not exist')
		sys.exit(1)

	if not os.path.exists(args.out_dir):
		os.mkdir(args.out_dir)

	if os.path.isfile(args.pfpk) and os.path.isfile(args.pfid):
		derive_one_dac(args.pfpk, args.pfid, args.out_dir, '000000001')
	elif os.path.isdir(args.pfpk) and os.path.isdir(args.pfid):
		for parent, dnames, fnames in os.walk(args.pfpk):
			for fname in fnames:
				idx = fname[-13 : -4]
				file_pfid = args.pfid + '/' + 'pfid_' + idx + '.bin'
				file_pfpk = os.path.join(parent, fname)
				if os.path.exists(file_pfid):
					derive_one_dac(file_pfpk, file_pfid, args.out_dir, idx)
	else:
		print('input parameter error')
		sys.exit(1)

	print(str(DERIVED_FILE_NUM) + ' ' + TARGET_NAME + ' files derived successfully')

if __name__ == '__main__':
	main()
