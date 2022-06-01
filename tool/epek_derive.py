#!/usr/bin/env python3
#
# Copyright (C) 2022 Amlogic, Inc. All rights reserved.
#
# This source code is subject to the terms and conditions defined in the
# file 'LICENSE' which is part of this source code package.

TARGET_NAME = 'epek'
MAX_IDX = 100000000
DERIVED_FILE_NUM = 0

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--ppk', type = str, required = True, help = 'ppk file or directory')
	parser.add_argument('--pek', type = str, required = True, help = 'pek file or directory')
	parser.add_argument('--out_dir', type = str, default = './' + TARGET_NAME + '/', help = 'output directory')
	return parser.parse_args()

def derive_one_epek(file_ppk, file_pek, out_dir, idx):
	import os
	import sys
	from Cryptodome.Cipher import AES

	if int(idx) > MAX_IDX:
		print('the number of files exceeds the limit')
		sys.exit(1)

	f = open(file_ppk, 'rb')
	ppk = f.read()
	f.close()

	f = open(file_pek, 'rb')
	pek = f.read()
	f.close()

	iv = '\x00' * 16
	epek = AES.new(ppk, AES.MODE_CBC, iv.encode('utf-8')).encrypt(pek)

	file_epek = out_dir + '/' + TARGET_NAME + '_' + idx + '.bin'
	f = open(file_epek, 'wb')
	f.write(epek)
	f.close()

	global DERIVED_FILE_NUM
	DERIVED_FILE_NUM = DERIVED_FILE_NUM + 1
	print(os.path.abspath(file_epek) + ' derived successfully')

def main():
	import os
	import sys

	args = get_args()

	if not os.path.exists(args.ppk):
		print(args.ppk + ' not exist')
		sys.exit(1)

	if not os.path.exists(args.pek):
		print(args.pek + ' not exist')
		sys.exit(1)

	if not os.path.exists(args.out_dir):
		os.mkdir(args.out_dir)

	if os.path.isfile(args.ppk) and os.path.isfile(args.pek):
		derive_one_epek(args.ppk, args.pek, args.out_dir, '000000001')
	elif os.path.isdir(args.ppk) and os.path.isdir(args.pek):
		for parent, dnames, fnames in os.walk(args.ppk):
			for fname in fnames:
				idx = fname[-13 : -4]
				file_pek = args.pek + '/' + 'pek_' + idx + '.bin'
				file_ppk = os.path.join(parent, fname)
				if os.path.exists(file_pek):
					derive_one_epek(file_ppk, file_pek, args.out_dir, idx)
	else:
		print('input parameter error')
		sys.exit(1)

	print(str(DERIVED_FILE_NUM) + ' ' + TARGET_NAME + ' files derived successfully')

if __name__ == '__main__':
	main()
