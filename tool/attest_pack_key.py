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
	parser.add_argument('--in', required=True, dest='inf', help='Name of input file')

	return parser.parse_args()

def main():
	import sys
	import os
	import struct

	dirname = sys.path[0] + "/unifykey"
	if os.path.exists(dirname) == False:
		os.mkdir(dirname)

	# parse arguments
	args = get_args()
	keyname = dirname + '/' + args.inf + ".keybox"

	keyoffset = [0] * 8
	keysize = [0] * 8
	keynum = 0
# version,keynum,keyoffset[],keysize[] = 18int
	keyheadlen = struct.calcsize('<IIIIIIIIIIIIIIIIII')
	keyoffset[0] = keyheadlen

	file_name = ("AttestKey.rsa", "AttestCert.rsa0", "AttestCert.rsa1", \
			"AttestCert.rsa2", "AttestKey.ec", "AttestCert.ec0", \
			"AttestCert.ec1", "AttestCert.ec2")

	for i in range(0, 8):
		if os.path.exists(file_name[i]):
			fd = open(file_name[i], 'rb')
			fd.seek(0, 2)
			keysize[i] = fd.tell()
			keynum = keynum + 1
			fd.close()
		else:
			keysize[i] = 0

		if i != 0:
			keyoffset[i] = keyoffset[i-1] + keysize[i-1]

	keyhead = struct.pack('<IIIIIIIIIIIIIIIIII', \
			0x0, keynum, keyoffset[0], \
			keysize[0], keyoffset[1], keysize[1], keyoffset[2], keysize[2], \
			keyoffset[3], keysize[3], keyoffset[4], keysize[4], \
			keyoffset[5], keysize[5], keyoffset[6], keysize[6], \
			keyoffset[7], keysize[7])

	fdw = open(keyname, 'w+')
	fdw.seek(0, 0)
	fdw.write(keyhead)

	for i in range(0, 8):
		if keysize[i] != 0:
			fd = open(file_name[i], 'rb')
			buf = fd.read()
			fdw.write(buf)
			fd.close()

	fdw.close()

if __name__ == "__main__":
	main()
