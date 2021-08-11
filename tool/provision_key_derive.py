#!/usr/bin/env python3
#
# Copyright (C) 2016 Amlogic, Inc. All rights reserved.
#
#
# This source code is subject to the terms and conditions defined in the
# file 'LICENSE' which is part of this source code package.
#
#

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--model_id', type = int, default = 0, \
			help = 'model id')
	parser.add_argument('--sub_id', type = int, default = 0, \
			help = 'sub id')
	parser.add_argument('--counter_base', type = int, default = 0, \
			help = 'counter base')
	parser.add_argument('--count', type = int, required = True, \
			help = 'device count')
	parser.add_argument('--out_dir', type = str, default = './', \
			help = 'output directory of the derived key files')

	return parser.parse_args()

def derive_random(buf, size):
	import random

	for i in range(size):
		buf.append(random.randint(0, 255))

def make_file_path(file_dir, pre_file_name, file_no, need_no):
	if need_no == True:
		return file_dir + "/" + pre_file_name + "-" + str(file_no) \
		+ ".bin"
	else:
		return file_dir + "/" + pre_file_name + ".bin"

def derive_key_files(key_size, key_cnt, key_name, out_dir):
	import struct

	key = []
	for i in range(1, key_cnt + 1):
		derive_random(key, key_size)
		f = open(make_file_path(out_dir, key_name, i, key_cnt > 1), \
				'wb')
		for j in range(key_size):
			f.write(struct.pack("B", key[j]))
		f.close()

def derive_pcpk_file(key_size, out_dir):
	derive_key_files(key_size, 1, "pcpk", out_dir)

def derive_pek_files(key_size, key_cnt, out_dir):
	derive_key_files(key_size, key_cnt, "pek", out_dir)

def derive_pfid_files(model_id, sub_id, counter_base, id_cnt, out_dir):
	import numpy
	import struct

	for i in range(1, id_cnt + 1):
		f = open(make_file_path(out_dir, "pfid", i, id_cnt > 1), 'wb')
		f.write(struct.pack('I', model_id))
		f.write(struct.pack('I', sub_id))
		f.write(struct.pack('Q', numpy.int64(counter_base + i)))
		f.close()

def derive_pfpk_files(key_size, key_cnt, out_dir):
	derive_key_files(key_size, key_cnt, "pfpk", out_dir)

# pcpk:		provision common protect key
# pek:		provision encrypt key
# pfpk:		provision field protect key
# pfid:		provision field id

def main():
	import os

	args = get_args()

	if not os.path.exists(args.out_dir):
		os.mkdir(args.out_dir)

	derive_pcpk_file(16, args.out_dir)
	derive_pek_files(16, args.count, args.out_dir)
	derive_pfid_files(args.model_id, args.sub_id, args.counter_base, \
			args.count, args.out_dir)
	derive_pfpk_files(16, args.count, args.out_dir)

	print ('Provision Key Derive ...')
	print ('  Input:                 model_id = ' + str(args.model_id))
	print ('                           sub_id = ' + str(args.sub_id))
	print ('                     counter_base = ' + str(args.counter_base))
	print ('                            count = ' + str(args.count))
	print ('                          out_dir = ' + args.out_dir)
	if args.count == 1:
		print ('  Output:               pcpk file = pcpk.bin')
		print ('                         pek file = pek.bin')
		print ('                        pfid file = pfid.bin')
		print ('                        pfpk file = pfpk.bin')
	else:
		print ('  Output:               pcpk file = pcpk.bin')
		print ('                         pek file = pek-{1...' \
			+ str(args.count) + '}.bin')
		print ('                        pfid file = pfid-{1...' \
			+ str(args.count) + '}.bin')
		print ('                        pfpk file = pfpk-{1...' \
			+ str(args.count) + '}.bin')

if __name__ == "__main__":
	main()
