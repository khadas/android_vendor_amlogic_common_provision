#!/usr/bin/env python3
#
# Copyright (C) 2021 Amlogic, Inc. All rights reserved.
#
# This source code is subject to the terms and conditions defined in the
# file 'LICENSE' which is part of this source code package.

TARGET_NAME = 'dgpk2_efuse_pattern'
MAX_IDX = 100000000
DERIVED_FILE_NUM = 0
DGPK2_SIZE = 16
PFID_SIZE = 16

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--soc', type = str, required = True, help = 'soc')
	parser.add_argument('--dgpk2', type = str, required = True, help = 'dgpk2 file or directory')
	parser.add_argument('--pfid', type = str, required = True, help = 'pfid file or directory')
	parser.add_argument('--encrypt_tool', type = str, required = True, help = 'efuse encrypt tool path')
	parser.add_argument('--dgpk2_offset', type = int, required = True, help = 'dgpk2 offset')
	parser.add_argument('--pfid_offset', type = int, required = True, help = 'pfid offset')
	parser.add_argument('--dgpk2_lock_offset', type = int, required = True, help = 'dgpk1 lock offset')
	parser.add_argument('--pfid_lock_offset', type = int, required = True, help = 'pfid lock offset')
	parser.add_argument('--dgpk2_lock_bit', type = int, required = True, help = 'dgpk2 lock bit')
	parser.add_argument('--pfid_lock_bit', type = int, required = True, help = 'pfid lock bit')
	parser.add_argument('--efuse_size', type = int, required = True, help = 'efuse layout size')
	parser.add_argument('--out_dir', type = str, required = True, help = 'output directory')
	return parser.parse_args()

def derive_one_pattern(args, dgpk2_file, pfid_file, idx):
	import os
	import sys
	import subprocess

	if int(idx) > MAX_IDX:
		print('the number of files exceeds the limit')
		sys.exit(1)

	efuse_layout = bytes(args.efuse_size)

	f = open(dgpk2_file, 'rb')
	dgpk2 = f.read()
	f.close()
	if len(dgpk2) != DGPK2_SIZE:
		print('dgpk2 size error')
		sys.exit(1)

	f = open(pfid_file, 'rb')
	pfid = f.read()
	f.close()
	if len(pfid) != PFID_SIZE:
		print('pfid size error')
		sys.exit(1)

	out_file = args.out_dir + '/' + args.soc + '_' + TARGET_NAME + '_' + idx + '.bin'

	f = open(out_file, 'wb')
	f.write(efuse_layout)

	f.seek(args.dgpk2_offset)
	f.write(dgpk2)

	f.seek(args.pfid_offset)
	f.write(pfid)

	f.seek(args.dgpk2_lock_offset)
	lock_value = (1 << args.dgpk2_lock_bit)
	f.write(lock_value.to_bytes(1, byteorder = 'little'))

	f.seek(args.pfid_lock_offset)
	lock_value = (3 << args.pfid_lock_bit) #pfid lock use 2bits, 32bit-lock
	f.write(lock_value.to_bytes(1, byteorder = 'little'))

	f.close()

	subprocess.run([args.encrypt_tool, "--efsproc", "--input", os.path.abspath(out_file)])

	global DERIVED_FILE_NUM
	DERIVED_FILE_NUM = DERIVED_FILE_NUM + 1
	print(os.path.abspath(out_file) + '.efuse derived successfully')

def main():
	import os
	import sys

	args = get_args()

	if not os.path.exists(args.encrypt_tool):
		print(args.encrypt_tool + ' not exist')
		sys.exit(1)

	if not os.path.exists(args.out_dir):
		os.mkdir(args.out_dir)

	if os.path.isfile(args.dgpk2) and os.path.isfile(args.pfid):
		derive_one_pattern(args, args.dgpk2, args.pfid, '000000001')
	elif os.path.isdir(args.dgpk2) and os.path.isdir(args.pfid):
		for parent, dnames, fnames in os.walk(args.dgpk2):
			for fname in fnames:
				idx = fname[-13 : -4]
				file_pfid = args.pfid + '/' + args.soc + '_pfid_' + idx + '.bin'
				file_dgpk2 = os.path.join(parent, fname)
				if os.path.exists(file_pfid):
					derive_one_pattern(args, file_dgpk2, file_pfid, idx)
	else:
		print('input parameter error')
		sys.exit(1)

	print(str(DERIVED_FILE_NUM) + ' ' + TARGET_NAME + ' files derived successfully')

if __name__ == '__main__':
	main()
