#!/usr/bin/env python
#
# Copyright (C) 2016 Amlogic, Inc. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--in', required=True, dest='inf', help='Name of input file')
	parser.add_argument('--out', type=str, default='null', help='Name of output file')

	return parser.parse_args()

def file_write(head, start_p, length, fd, name):
	import gc
	ret = 0

	args = get_args()

	if args.out != 'null':
		name = args.out + '/' + name

	size_h = len(head)
	fd1 = open(name, 'w+')

	fd1.write(head)
	fd.seek(start_p, 0)
	buf = fd.read(length)
	fd1.write(buf)

	del buf
	gc.collect()
	fd1.close()

	return ret

def file_get_pos(start, end, fd, cursor):
	import re
	import gc
	ret = 0

	fd.seek(cursor, 0)
	keybuf = fd.read()

	start_m = re.search(start, keybuf)
	if start_m == None:
		ret = -1
		print "not found the start position of key\n"
		return ret, 0, 0

	end_m = re.search(end, keybuf)
	if end_m == None:
		ret = -1
		return ret, 0, 0

	start_p = cursor + start_m.end()
	end_p = cursor + end_m.end()

	del keybuf
	gc.collect()
	return ret, start_p, end_p


def file_excision(data_file, key_s, key_e, suffix):

	import sys
	cert_s = "-----BEGIN CERTIFICATE-----"
	cert_e = "-----END CERTIFICATE-----"
	fd = open(data_file, 'rb')

	name = "AttestKey." + suffix + ".pem"
	(ret, start_p, end_p) = file_get_pos(key_s, key_e, fd, 0)
	if ret != 0:
		print 'error'
		fd.close()
		sys.exit(0)


	ret = file_write(key_s, start_p, end_p - start_p, fd, name)
	if ret != 0:
		print 'error'
		fd.close()
		sys.exit(0)

	for i in range(0, 3):
		(ret, start_p, end_p) = file_get_pos(cert_s, cert_e, fd, end_p)
		if ret != 0:
			print 'error'
			sys.exit(0)
		name = "AttestCert." + suffix + bytes(i) + ".pem"
		ret = file_write(cert_s, start_p, end_p - start_p, fd, name)
		if ret != 0:
			print 'error'
			sys.exit(0)

	fd.close()

	return ret

def main():
	import sys
	import gc

	# parse arguments
	args = get_args()

	ec_key_s = "-----BEGIN EC PRIVATE KEY-----"
	ec_key_e = "-----END EC PRIVATE KEY-----"
	rsa_key_s = "-----BEGIN RSA PRIVATE KEY-----"
	rsa_key_e = "-----END RSA PRIVATE KEY-----"
	ret = file_excision(args.inf, ec_key_s, ec_key_e,"ec");
	ret = file_excision(args.inf, rsa_key_s, rsa_key_e,"rsa");

	gc.collect()
if __name__ == "__main__":
	main()
