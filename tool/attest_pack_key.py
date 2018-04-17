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
