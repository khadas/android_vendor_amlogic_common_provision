#!/usr/bin/env python
#
# Copyright (C) 2018 Amlogic, Inc. All rights reserved.
#
# All information contained herein is Amlogic confidential.
#
# This software is provided to you pursuant to Software License
# Agreement (SLA) with Amlogic Inc ("Amlogic"). This software may be
# used only in accordance with the terms of this agreement.
#
# Redistribution and use in source and binary forms, with or without
# modification is strictly prohibited without prior written permission
# from Amlogic.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--in', required=True, dest='inf', help='Name of input file')
	parser.add_argument('--skip', type=int, default=1, help='key cutting interval')

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

	args = get_args()
	skip_num = args.skip
	log = logging.getLogger("Core.Analysis.Processing")
	INTERPRETER = "/usr/bin/python"

	file_path = str(sys.path[0])
	processor1 = file_path + "/attest_parse_key.py"
	cmd = [INTERPRETER, processor1]

	if not os.path.exists(INTERPRETER):
		log.error("Cannot find INTERPRETER at path \"%s\"." % INTERPRETER)

	fd = open(data_file, 'rb')

	# find the end of  the file and redundant 16 Bytes
	fd.seek(0,2)
	file_end = fd.tell() - len("</AndroidAttestation>") - 16;

	end_p = 0;
	key_num = 0;
	while end_p < file_end:
		(ret, start_p, end_p) = file_get_pos(key_s, key_e, fd, end_p)
		if ret != 0:
			print 'error'
			fd.close()
			sys.exit(0)
		if key_num % skip_num != 0:
			# Do not skip the last key
			if end_p + 4096 < file_end:
				key_num += 1;
				continue

		key_num += 1;
		(ret, name_sp, name_ep) = file_get_pos('="', '">', fd, start_p)
		if ret != 0:
			print 'error'
			fd.close()
			sys.exit(0)

		fd.seek(name_sp, 0)
		file_name = "provisionkey/" + fd.read(name_ep - name_sp - 2) + ".origin";

		file_write(key_s, start_p, end_p - start_p, fd, file_name)

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
