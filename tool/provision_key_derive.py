#!/usr/bin/env python
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
	parser.add_argument('--model_id', type = int, required = True, \
			help = 'model id')
	parser.add_argument('--sub_id', type = int, required = True, \
			help = 'sub id')
	parser.add_argument('--counter_base', type = int, required = True, \
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

def derive_key_files(key_size, key_cnt, key_name, out_dir):
	import struct

	key = []
	if key_cnt == 1:
		derive_random(key, key_size)
		f = open(out_dir + "/" + key_name + ".bin", 'wb')
		for i in range(key_size):
			f.write(struct.pack("B", key[i]))
		f.close()
	elif key_cnt > 1:
		for i in range(1, key_cnt + 1):
			derive_random(key, key_size)
			f = open(out_dir + "/" + key_name + "-" + str(i) \
					+ ".bin", 'wb')
			for j in range(key_size):
				f.write(struct.pack("B", key[j]))
			f.close()

def derive_pcpk_file(key_size, out_dir):
	derive_key_files(key_size, 1, "pcpk", out_dir)

def derive_pek_files(key_size, key_cnt, out_dir):
	derive_key_files(key_size, key_cnt, "pek", out_dir)

def derive_psk_files(key_size, key_cnt, out_dir):
	derive_key_files(key_size, key_cnt, "psk", out_dir)

def derive_pfid_files(model_id, sub_id, counter_base, id_cnt, out_dir):
	import numpy
	import struct

	for i in range(1, id_cnt + 1):
		f = open(out_dir + "/pfid-" + str(i) + ".bin", 'wb')
		f.write(struct.pack('I', model_id))
		f.write(struct.pack('I', sub_id))
		f.write(struct.pack('Q', numpy.int64(counter_base + i)))
		f.close()

def derive_pfpk_files(key_size, key_cnt, out_dir):
	derive_key_files(key_size, key_cnt, "pfpk", out_dir)

# pcpk:		provision common protect key
# pek:		provision encrypt key
# psk:		provision sign key
# pfpk:		provision field protect key
# pfid:		provision field id

def main():
	import os

	args = get_args()

	if not os.path.exists(args.out_dir):
		os.mkdir(args.out_dir)

	derive_pcpk_file(16, args.out_dir)
	derive_pek_files(16, args.count, args.out_dir)
	derive_psk_files(32, args.count, args.out_dir)
	derive_pfid_files(args.model_id, args.sub_id, args.counter_base, \
			args.count, args.out_dir)
	derive_pfpk_files(16, args.count, args.out_dir)

	print 'Provision Key Derive ...'
	print '  Input:                 model_id = ' + str(args.model_id)
	print '                           sub_id = ' + str(args.sub_id)
	print '                     counter_base = ' + str(args.counter_base)
	print '                            count = ' + str(args.count)
	print '                          out_dir = ' + args.out_dir

if __name__ == "__main__":
	main()
