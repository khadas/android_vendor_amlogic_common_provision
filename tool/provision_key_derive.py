#!/usr/bin/env python3
#
# Copyright (C) 2022 Amlogic, Inc. All rights reserved.
#
# This source code is subject to the terms and conditions defined in the
# file 'LICENSE' which is part of this source code package.

MAX_IDX = 100000000
KEY_SIZE = 16

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--model_id', type = int, default = 0, help = 'model id')
	parser.add_argument('--sub_id', type = int, default = 0, help = 'sub id')
	parser.add_argument('--counter_base', type = int, default = 0, help = 'counter base')
	parser.add_argument('--count', type = int, required = True, help = 'device count')
	parser.add_argument('--out_dir', type = str, default = './provision-keys/', help = 'output directory of the derived key files')

	return parser.parse_args()

def derive_key_files(key_cnt, key_name, out_dir):
	import struct
	import os

	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	for i in range(1, key_cnt + 1):
		file_path = out_dir + '/' + key_name + '_' + str(i).zfill(9) + '.bin'
		f = open(file_path, 'wb')
		f.write(os.getrandom(KEY_SIZE))
		f.close()
		print(os.path.abspath(file_path) + ' derived successfully')

def derive_pcpk_file(out_dir):
	derive_key_files(1, 'pcpk', out_dir + '/pcpk/')

def derive_pek_files(key_cnt, out_dir):
	derive_key_files(key_cnt, 'pek', out_dir + '/peks/')

def derive_pfid_files(model_id, sub_id, counter_base, id_cnt, out_dir):
	import numpy
	import struct
	import os

	out_dir = out_dir + '/pfids/'
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	for i in range(1, id_cnt + 1):
		file_path = out_dir + '/pfid_' + str(i).zfill(9) + '.bin'
		f = open(file_path, 'wb')
		f.write(struct.pack('>I', model_id))
		f.write(struct.pack('>I', sub_id))
		f.write(struct.pack('>Q', numpy.int64(counter_base + i)))
		f.close()
		print(os.path.abspath(file_path) + ' derived successfully')

def derive_pfpk_files(key_cnt, out_dir):
	derive_key_files(key_cnt, 'pfpk', out_dir + '/pfpks/')

# pcpk:		provision common protect key
# pek:		provision encrypt key
# pfpk:		provision field protect key
# pfid:		provision field id
def main():
	import os

	args = get_args()

	if not os.path.exists(args.out_dir):
		os.mkdir(args.out_dir)

	if args.count > MAX_IDX:
		args.count = MAX_IDX
		print('the max number of device is ' + MAX_IDX)

	derive_pcpk_file(args.out_dir)
	derive_pek_files(args.count, args.out_dir)
	derive_pfid_files(args.model_id, args.sub_id, args.counter_base, args.count, args.out_dir)
	derive_pfpk_files(args.count, args.out_dir)

if __name__ == '__main__':
	main()
