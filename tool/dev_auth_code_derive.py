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
	parser.add_argument('--pfpk', required = True, \
			help = 'provision field protect key file')
	parser.add_argument('--pfid', required = True, \
			help = 'provision field id')
	parser.add_argument('--dac', type = str, default = 'dac.bin', \
			help = 'device authentication code file(output)')

	return parser.parse_args()

# pfpk:		provision field protect key
# pfid:		provision field id
# dac:		device authentication code

def main():
	import os
	import hmac
	import hashlib
	import struct

	args = get_args()

	f = open(args.pfpk, 'rb')
	pfpk = f.read(16)
	f.close()

	f = open(args.pfid, 'rb')
	pfid = f.read(16)
	f.close()

	hmac_key = pfpk + struct.pack('<4I', *([0] * 4))
	dac = hmac.HMAC(hmac_key, pfid, hashlib.sha256).digest()
	f = open(args.dac, 'wb')
	f.write(dac)
	f.close()

	print ('Device Authentication Code Derive ...')
	print ('  Input:                 pfpk file = ' + args.pfpk)
	print ('                         pfid file = ' + args.pfid)
	print ('  Output:                 dac file = ' + args.dac)

if __name__ == "__main__":
	main()
