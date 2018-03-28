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

	return parser.parse_args()

def file_write(head, start_p, length, fd, name):
	import gc
	ret = 0
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
# 16KB buf > a attestation key size
	keybuf = fd.read(0x4000)

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


def file_excision(data_file, key_s, key_e):

	import sys
	import os
	import gc
	import logging
	import subprocess

	log = logging.getLogger("Core.Analysis.Processing")
	INTERPRETER = "/usr/bin/python"

	file_path = str(sys.path[0])
	processor1 = file_path + "/attest_parse_key.py"
	cmd = [INTERPRETER, processor1]

	if not os.path.exists(INTERPRETER):
		log.error("Cannot find INTERPRETER at path \"%s\"." % INTERPRETER)

	fd = open(data_file, 'rb')

#	/* find the end of  the file and redundant 16 Bytes */
	fd.seek(0,2)
	file_end = fd.tell() - len("</AndroidAttestation>") - 16;

	end_p = 0;
	while end_p < file_end:
		(ret, start_p, end_p) = file_get_pos(key_s, key_e, fd, end_p)
		if ret != 0:
			print 'error'
			fd.close()
			sys.exit(0)

		(ret, name_sp, name_ep) = file_get_pos('="', '">', fd, start_p)
		if ret != 0:
			print 'error'
			fd.close()
			sys.exit(0)

		fd.seek(name_sp, 0)
		dir_name = "provisionkey/" + fd.read(name_ep - name_sp - 2);

		if os.path.exists(dir_name) == False:
			os.mkdir(dir_name)
		name = dir_name + "/Attestation.key"
		file_write(key_s, start_p, end_p - start_p, fd, name)

		cmd.extend(["--in=" + file_path + '/' + name])
		cmd.extend(["--out=" + file_path + '/' +  dir_name])
		sub = subprocess.Popen(cmd)
		sub.communicate()
		del sub
		gc.collect()

	fd.close()

	return ret

def main():
	import os
	import sys

	# parse arguments
	args = get_args()

	key_start = "<Keybox DeviceID"
	key_end = "</Key></Keybox>"
	if os.path.exists("provisionkey") == False:
		os.mkdir("provisionkey")

	ret = file_excision(args.inf, key_start, key_end);

if __name__ == "__main__":
	main()
