#!/usr/bin/env python3
#
# Copyright (C) 2021 Amlogic, Inc. All rights reserved.
#
# This source code is subject to the terms and conditions defined in the
# file 'LICENSE' which is part of this source code package.

import sys

sys.dont_write_bytecode = True
import soc

TARGET_NAME = 'dgpk1-efuse-pattern'
SCRIPT_PATH = sys.path[0] + '/../dependents/dgpk1_efuse_pattern_derive.py'
ENCRYPT_TOOL_PATH = sys.path[0] + '/aml_encrypt_' + soc.SOC

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--dgpk1', type = str, required = True, help = 'dgpk1 file')
	parser.add_argument('--out_dir', type = str, default = './' + soc.SOC + '-' + TARGET_NAME + '/', help = 'output directory')
	return parser.parse_args()

def main():
	import os
	import sys
	import subprocess

	args = get_args()

	cmd = [sys.executable, SCRIPT_PATH]
	cmd.extend(['--soc=' + soc.SOC])
	cmd.extend(['--dgpk1=' + args.dgpk1])
	cmd.extend(['--encrypt_tool=' + ENCRYPT_TOOL_PATH])
	cmd.extend(['--dgpk1_offset=' + str(int(soc.DGPK1_OFFSET, 16))])
	cmd.extend(['--lock_offset=' + str(int(soc.DGPK1_LOCK_OFFSET, 16))])
	cmd.extend(['--lock_bit=' + str(int(soc.DGPK1_LOCK_BIT, 16))])
	cmd.extend(['--efuse_size=' + str(int(soc.EFUSE_TOTAL_SIZE, 16))])
	cmd.extend(['--out_dir=' + args.out_dir])
	sub = subprocess.Popen(cmd)
	sub.communicate()

if __name__ == '__main__':
	main()
