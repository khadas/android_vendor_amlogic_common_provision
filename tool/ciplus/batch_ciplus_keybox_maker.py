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
	parser.add_argument('--rt_cert', required = True, help = 'root certificate file')
	parser.add_argument('--br_cert', required = True, help = 'brand certificate file')
	parser.add_argument('--dev_dir', required = True, help = 'directory of device certificate and key')
	parser.add_argument('--type', type = int, default = 0, choices = [0, 1], help = '0: not ecp; 1: ecp')
	parser.add_argument('--out_dir', type = str, default = 'ciplus_keyboxs', help = 'output directory of keybox')

	return parser.parse_args()

def main():
	import os
	import sys
	import shutil
	import subprocess

	args = get_args()

	if not os.path.exists(args.dev_dir):
		print('directory of device certificate and key is incorrect')
		sys.exit(1)

	if not os.path.exists(args.out_dir):
		os.makedirs(args.out_dir)

	if not os.path.exists(args.out_dir + '/sha256_files/'):
		os.makedirs(args.out_dir + '/sha256_files/')

	for root, dirs, files in os.walk(args.dev_dir):
		for f in files:
			if f.find('cert') > 0:
				keybox_pre = f[:f.find('cert')] + 'ciplus-keybox'
				dev_cert = os.path.join(root, f)
				dev_key = os.path.join(root, f[:f.find('cert')] + 'key.der')

				maker_cmd = ['/usr/bin/python', str(sys.path[0]) + '/ciplus_keybox_maker.py']
				maker_cmd.extend(['--rt_cert=' + args.rt_cert])
				maker_cmd.extend(['--br_cert=' + args.br_cert])
				maker_cmd.extend(['--dev_cert=' + dev_cert])
				maker_cmd.extend(['--dev_key=' + dev_key])
				maker_cmd.extend(['--type=' + str(args.type)])
				maker_cmd.extend(['--out=' + keybox_pre])
				subprocess.Popen(maker_cmd).communicate()

				if args.type == 0:
					keybox = keybox_pre + '.bin'
					sha256 = keybox_pre + '.bin.sha256'
				else:
					keybox = keybox_pre + '.ecp.bin'
					sha256 = keybox_pre + '.ecp.bin.sha256'

				if os.path.exists(keybox):
					shutil.move(keybox, args.out_dir)
				if os.path.exists(sha256):
					shutil.move(sha256, args.out_dir + '/sha256_files/')

if __name__ == "__main__":
	main()
