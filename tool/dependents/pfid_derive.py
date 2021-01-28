#!/usr/bin/env python3
#
# Copyright (C) 2021 Amlogic, Inc. All rights reserved.
#
# This source code is subject to the terms and conditions defined in the
# file 'LICENSE' which is part of this source code package.

TARGET_NAME = 'pfid'
MAX_IDX = 100000000

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--soc', type = str, required = True, help = 'soc')
	parser.add_argument('--model_id', type = int, required = True, help = 'model id')
	parser.add_argument('--sub_id', type = int, required = True, help = 'sub id')
	parser.add_argument('--counter_base', type = int, required = True, help = 'counter base')
	parser.add_argument('--count', type = int, required = True, help = 'device count')
	parser.add_argument('--out_dir', type = str, required = True, help = 'output directory')
	return parser.parse_args()

#pfid: provision field id
def main():
	import os
	import struct

	args = get_args()

	if not os.path.exists(args.out_dir):
		os.mkdir(args.out_dir)

	if args.count > MAX_IDX:
		args.count = MAX_IDX
		print('the max number of ' + TARGET_NAME + ' derived at one time is ' + MAX_IDX)

	derived_num = 0
	for i in range(1, args.count + 1):
		fpath = args.out_dir + '/' + args.soc + '_' + TARGET_NAME + '_' + str(i).zfill(9) + '.bin'
		f = open(fpath, 'wb')
		f.write(struct.pack('<H', args.model_id))
		f.write(struct.pack('<H', args.sub_id))
		f.write(struct.pack('<I', args.counter_base + i))
		f.write(8 * b'\x00')
		f.close()

		derived_num = derived_num + 1
		print(os.path.abspath(fpath) + ' derived successfully')

	print(str(derived_num) + ' ' + TARGET_NAME + ' files derived successfully')

if __name__ == '__main__':
	main()
