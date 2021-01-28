#!/usr/bin/env python3
#
# Copyright (C) 2016 Amlogic, Inc. All rights reserved.
#
#
# This source code is subject to the terms and conditions defined in the
# file 'LICENSE' which is part of this source code package.
#
#

ALGO = 'gen-prot-aes128'
MRK_NAME = 'DGPK1'
BOOT_STAGE = 2
EK3 = '0f3edbdb962f84c4c442defca2ce8c35'
EK2 = 'bef32c3e35bccde2525bf7e780088760'
EK1 = '9146456a8c11c3ae180cc148372ac64b'

TARGET_NAME = 'pcpk'

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--soc', type = str, required = True, help = 'soc')
	parser.add_argument('--key_tool', type = str, required = True, help = 'vendor key tool path')
	parser.add_argument('--dgpk1', type = str, required = True, help = 'dgpk1 file')
	parser.add_argument('--out_dir', type = str, required = True, help = 'output directory')
	return parser.parse_args()

def main():
	import os
	import sys
	import binascii

	args = get_args()

	if not os.path.exists(args.key_tool):
		print(args.key_tool + ' not exist')
		sys.exit(1)

	if not os.path.exists(args.dgpk1):
		print(args.dgpk1 + ' not exist')
		sys.exit(1)

	if not os.path.exists(args.out_dir):
		os.mkdir(args.out_dir)

	f = open(args.dgpk1, 'rb')
	mrk = bytes.decode(binascii.b2a_hex(f.read()))
	f.close()

	# due to the other para aren't supported, can only use "SC2"
	cmd = args.key_tool + ' ' + ALGO + ' --chipset=SC2' + ' --mrk=' \
	      + mrk + ' --mrk-name=' + MRK_NAME + ' --boot-stage=' \
		+ str(BOOT_STAGE) + ' --ek3=' + EK3 + ' --ek2=' + EK2 \
		+ ' --ek1=' + EK1

	pcpk = os.popen(cmd).read()

	fpath = args.out_dir + '/' + args.soc + '_' + TARGET_NAME + '.bin'
	f = open(fpath, 'wb')
	f.write(binascii.unhexlify(pcpk[:32]))
	f.close()

	print(os.path.abspath(fpath) + ' derived successfully')

if __name__ == '__main__':
	main()
