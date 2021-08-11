#!/usr/bin/env python3
#
# Copyright (C) 2016 Amlogic, Inc. All rights reserved.
#
#
# This source code is subject to the terms and conditions defined in the
# file 'LICENSE' which is part of this source code package.
#
#

# dgpk: device global protect key
def main():
	import os
	import random
	import uuid
	from Cryptodome.Hash import SHA256

	uuid = uuid.uuid4()
	sha = SHA256.new()
	sha.update(uuid.bytes_le)

	dgpk1 = sha.digest()[:16]
	dgpk2 = sha.digest()[16:]

	f = open("dgpk1.bin", 'wb')
	f.write(dgpk1)
	f.close()

	f = open("dgpk2.bin", 'wb')
	f.write(dgpk2)
	f.close()

	print ('Generating DGPK1 and DGPK2 ...')
	print ('Output:    DGPK1(dgpk1.bin) = ' + sha.hexdigest()[:32])
	print ('           DGPK2(dgpk2.bin) = ' + sha.hexdigest()[32:])

if __name__ == "__main__":
	main()
