#!/usr/bin/env python3
#
# Copyright (C) 2021 Amlogic, Inc. All rights reserved.
#
# This source code is subject to the terms and conditions defined in the
# file 'LICENSE' which is part of this source code package.

TARGET_NAME = 'dgpk1'
DGPK1_SIZE = 16

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--soc', type = str, required = True, help = 'soc')
	parser.add_argument('--out_dir', type = str, required = True, help = 'output directory')
	return parser.parse_args()

# dgpk: device global protect key
def main():
	import os

	args = get_args()

	if not os.path.exists(args.out_dir):
		os.mkdir(args.out_dir)

	dgpk1 = os.getrandom(DGPK1_SIZE)

	fpath = args.out_dir + '/' + args.soc + '_' + TARGET_NAME + '.bin'
	f = open(fpath, 'wb')
	f.write(dgpk1)
	f.close()

	print(os.path.abspath(fpath) + ' derived successfully')

if __name__ == '__main__':
	main()
