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
	parser.add_argument('--dev_cert', required = True, help = 'device certificate file')
	parser.add_argument('--dev_key', required = True, help = 'device key file')
	parser.add_argument('--type', type = int, default = 0, choices = [0, 1], help = '0: not ecp; 1: ecp')
	parser.add_argument('--out', type = str, default = 'ciplus_keybox', help = 'prefix of output file name')

	return parser.parse_args()

import binascii

CIPLUS_KEY_NUM_ONE_GROUP = 12
CIPLUS_KEYBOX_MAGIC = 0x43494B42 # "CIKB"
CIPLUS_KEYBOX_VERSION = 0x1

KEYBOX_TYPE_CIPLUS = 0
KEYBOX_TYPE_CIPLUS_ECP = 1

PRNG_SEED = binascii.unhexlify('12233445122334451223344512233445')
PRNG_KEY_K = binascii.unhexlify('e58297317f8c6047ddd4a5d3d32dc15c')
DH_P = binascii.unhexlify( \
		'a479272e243d4436c85c82b0ff7d93e1' \
		'638d829d2ac79d4d4099c8d325a54f01' \
		'15ec2901183b93b836b8e0aa4f3a2077' \
		'6eb4963736551c366000f795717448c4' \
		'776cb279caaa336287f542121c43e01c' \
		'1253b2ef3156915ee0f3927180440da2' \
		'f2142fb429daf6e631654f12ea8812c3' \
		'64e5f6e829c42db384e76a15910bd238' \
		'48355978d7adef521e5c294eead030d9' \
		'c29666c69220c2fad5d558d726ef4658' \
		'36c622087e482fa6d59e1c1c8a0f5a09' \
		'e17db7e69ab26fe734969663bd71aafd' \
		'818199efaadc54ed6a4befcd39677169' \
		'760cd554d4f3cf9052ceadc605e605b4' \
		'e2ff0025a23afcc1546e526e830bde3c' \
		'62d73c7a8eee14349a2ecb69df1cc003' \
	)
DH_G = binascii.unhexlify( \
		'96b19bd8e10c5f9de4126649cb511165' \
		'739feb2caf27202477f84292c3303606' \
		'64a4895dce0a5134560fba2425cc4029' \
		'725d403b6e6f1f223f4e3db736ee10bb' \
		'd8453ce4693c333451f21013add31ee8' \
		'0baba24fdfa4ecb605f03c9f0935a87f' \
		'd44d3b9c234db9ded7a720ce259d1c65' \
		'4932ed9efe0276110d235baaaf61a51e' \
		'04e9372a2397556443534f3bb7fb7323' \
		'61034a1665786dcc9441f560408e15f2' \
		'878e353aa6b078edcd718f5cffee9e69' \
		'1ae0a8d0d5f9242addbdf23d21b2132f' \
		'e7d2e3c91a646514143747237cbbd30f' \
		'4dc9659df5b7f586cbd7295b08317715' \
		'c581f204602f39b8fd6ca6c4c94335c1' \
		'400e300b229acd508734616d235b1560' \
	)
DH_Q = binascii.unhexlify( \
		'd85eabe8be5be3d2cf50e790a86a3fad' \
		'dab6e8a50f328771fd0bf052ae3ca937' \
	)
SIV = binascii.unhexlify('d1e8de322e44d87c569081895f505035')
SLK = binascii.unhexlify('9c69d146700d816cfd4969712693a38a')
CLK = binascii.unhexlify('aedc1b804c50d95dad6d3d46acd601a8')

STB_CI_KEY_ROOT_CERT = 0
#STB_CI_KEY_BRAND_CERT
#STB_CI_KEY_DEVICE_CERT
#STB_CI_KEY_PRNG_SEED
#STB_CI_KEY_PRNG_KEY_K
#STB_CI_KEY_DH_P
#STB_CI_KEY_DH_G
#STB_CI_KEY_DH_Q
#STB_CI_KEY_HDQ
#STB_CI_KEY_SIV
#STB_CI_KEY_SLK
#STB_CI_KEY_CLK

STB_CI_ECP_KEY_ROOT_CERT = 16
#STB_CI_ECP_KEY_BRAND_CERT
#STB_CI_ECP_KEY_DEVICE_CERT
#STB_CI_ECP_KEY_PRNG_SEED
#STB_CI_ECP_KEY_PRNG_KEY_K
#STB_CI_ECP_KEY_DH_P
#STB_CI_ECP_KEY_DH_G
#STB_CI_ECP_KEY_DH_Q
#STB_CI_ECP_KEY_HDQ
#STB_CI_ECP_KEY_SIV
#STB_CI_ECP_KEY_SLK
#STB_CI_ECP_KEY_CLK

def main():
	import sys
	import struct
	import hashlib

	args = get_args()

	f = open(args.rt_cert, 'rb')
	ROOT_CERT = f.read()
	f.close()

	f = open(args.br_cert, 'rb')
	BRAND_CERT = f.read()
	f.close()

	f = open(args.dev_cert, 'rb')
	DEVICE_CERT = f.read()
	f.close()

	f = open(args.dev_key, 'rb')
	HDQ = f.read()
	f.close()

	if args.type == 0:
		root_key_type = STB_CI_KEY_ROOT_CERT
		keybox_type = KEYBOX_TYPE_CIPLUS
	elif args.type == 1:
		root_key_type = STB_CI_ECP_KEY_ROOT_CERT
		keybox_type = KEYBOX_TYPE_CIPLUS_ECP
	else:
		print('keybox type is incorrect')
		sys.exit(1)

	ci_keys = (ROOT_CERT, BRAND_CERT, DEVICE_CERT, PRNG_SEED, PRNG_KEY_K, DH_P, DH_G, DH_Q, HDQ, SIV, SLK, CLK)
	payload = b''
	for idx in range(CIPLUS_KEY_NUM_ONE_GROUP):
		key_type = root_key_type + idx
		key_size = len(ci_keys[idx])
		payload +=  struct.pack('<2I', key_type, key_size) + ci_keys[idx]

	keybox_hdr = struct.pack('<5I', CIPLUS_KEYBOX_MAGIC, \
			CIPLUS_KEYBOX_VERSION, keybox_type, \
			CIPLUS_KEY_NUM_ONE_GROUP, len(payload))

	keybox = keybox_hdr + payload

	sha256 = hashlib.sha256()
	sha256.update(keybox)
	kb_sha256 = sha256.digest()

	kb_file_name = args.out
	if keybox_type == KEYBOX_TYPE_CIPLUS_ECP:
		kb_file_name += '.ecp.bin'
	else:
		kb_file_name += '.bin'

	f = open(kb_file_name, 'wb')
	f.write(keybox)
	f.close()

	f = open(kb_file_name + '.sha256', 'wb')
	f.write(kb_sha256)
	f.close()

	print('Making CIPlus Keybox ...')
	print('  Input:    root certificate file = ' + args.rt_cert)
	print('           brand certificate file = ' + args.br_cert)
	print('          device certificate file = ' + args.dev_cert)
	print('                  device key file = ' + args.dev_key)
	print('                      keybox type = ' + str(args.type))
	print('  Output:      ciplus keybox file = ' + kb_file_name)
	print('        ciplus keybox sha256 file = ' + kb_file_name + '.sha256')

if __name__ == "__main__":
	main()
