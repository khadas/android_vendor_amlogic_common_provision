#!/usr/bin/env python3
#
# Copyright (C) 2021 Amlogic, Inc. All rights reserved.
#
# This source code is subject to the terms and conditions defined in the
# file 'LICENSE' which is part of this source code package.

DGPK1_SIZE = 16

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--soc', type = str, required = True, help = 'soc')
	parser.add_argument('--dgpk1', type = str, required = True, help = 'dgpk1 file')
	parser.add_argument('--encrypt_tool', type = str, required = True, help = 'efuse encrypt tool path')
	parser.add_argument('--dgpk1_offset', type = int, required = True, help = 'dgpk1 offset')
	parser.add_argument('--lock_offset', type = int, required = True, help = 'dgpk1 lock offset')
	parser.add_argument('--lock_bit', type = int, required = True, help = 'dgpk1 lock bit')
	parser.add_argument('--efuse_size', type = int, required = True, help = 'efuse layout size')
	parser.add_argument('--out_dir', type = str, required = True, help = 'output directory')
	return parser.parse_args()

def main():
	import os
	import sys
	import subprocess

	args = get_args()

	if not os.path.exists(args.dgpk1):
		print(args.dgpk1 + ' not exist')
		sys.exit(1)

	if not os.path.exists(args.encrypt_tool):
		print(args.encrypt_tool + ' not exist')
		sys.exit(1)

	if not os.path.exists(args.out_dir):
		os.mkdir(args.out_dir)

	efuse_layout = bytes(args.efuse_size)

	f = open(args.dgpk1, 'rb')
	dgpk1 = f.read()
	f.close()
	if len(dgpk1) != DGPK1_SIZE:
		print('dgpk1 size error')
		sys.exit(1)

	out_file = args.out_dir + '/' + args.soc + '_dgpk1_efuse_pattern.bin'

	f = open(out_file, 'wb')
	f.write(efuse_layout)

	f.seek(args.dgpk1_offset)
	f.write(dgpk1)

	f.seek(args.lock_offset)
	lock_value = (1 << args.lock_bit)
	f.write(lock_value.to_bytes(1, byteorder = 'little'))

	f.close()

	subprocess.run([args.encrypt_tool, "--efsproc", "--input", os.path.abspath(out_file)])

	print(os.path.abspath(out_file) + '.efuse derived successfully')

if __name__ == '__main__':
	main()
