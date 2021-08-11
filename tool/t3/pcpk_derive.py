#!/usr/bin/env python3
#
# Copyright (C) 2016 Amlogic, Inc. All rights reserved.
#
#
# This source code is subject to the terms and conditions defined in the
# file 'LICENSE' which is part of this source code package.
#
#

import sys

CHIP = "t3"
VENDOR_KEYTOOL = sys.path[0] + "/../../../../../../bootloader/uboot-repo/fip/" + CHIP + "/binary-tool/vendor-keytool"
ALGO = "gen-prot-aes128"
MRK_NAME = "DGPK1"
BOOT_STAGE = 2
EK3 = "0f3edbdb962f84c4c442defca2ce8c35"
EK2 = "bef32c3e35bccde2525bf7e780088760"
EK1 = "9146456a8c11c3ae180cc148372ac64b"

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--dgpk1', type = str, required = True, \
			help = 'dgpk1 string')

	return parser.parse_args()

def main():
	import os
	import sys
	import binascii

	if not os.path.exists(VENDOR_KEYTOOL):
		print (VENDOR_KEYTOOL + " not exist")
		sys.exit(1)

	args = get_args()
	mrk = args.dgpk1

	# due to the parameter "T3" aren't supported, can only use "SC2"
	cmd = VENDOR_KEYTOOL + " " + ALGO + " --chipset=" + "SC2" + " --mrk=" \
	      + mrk + " --mrk-name=" + MRK_NAME + " --boot-stage=" \
		+ str(BOOT_STAGE) + " --ek3=" + EK3 + " --ek2=" + EK2 \
		+ " --ek1=" + EK1

	pcpk = os.popen(cmd).read()

	f = open(CHIP + "_pcpk.bin", 'wb')
	f.write(binascii.unhexlify(pcpk[:32]))
	f.close()

	print ('Generating PCPK ...')
	print ("  Input: DGPK1 = " + args.dgpk1)
	print ("  Output: PCPK(" + CHIP + "_pcpk.bin)" + " = " + pcpk)

if __name__ == "__main__":
	main()
