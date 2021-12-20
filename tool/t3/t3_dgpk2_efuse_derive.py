#!/usr/bin/env python3
#
# Copyright (C) 2021 Amlogic, Inc. All rights reserved.
#
# This source code is subject to the terms and conditions defined in the
# file 'LICENSE' which is part of this source code package.

import sys

sys.dont_write_bytecode = True
import soc

TARGET_NAME = 'dgpk2-efuse-pattern'
SCRIPT_PATH = sys.path[0] + '/../dependents/dgpk2_efuse_pattern_derive.py'
ENCRYPT_TOOL_PATH = sys.path[0] + '/aml_encrypt_' + soc.SOC

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--dgpk2', type = str, required = True, help = 'dgpk2 file or directory')
	parser.add_argument('--pfid', type = str, required = True, help = 'pfid file or directory')
	parser.add_argument('--out_dir', type = str, default = './' + soc.SOC + '-' + TARGET_NAME + '/', help = 'output directory')
	return parser.parse_args()

def main():
	import os
	import sys
	import subprocess

	args = get_args()

	cmd = [sys.executable, SCRIPT_PATH]
	cmd.extend(['--soc=' + soc.SOC])
	cmd.extend(['--dgpk2=' + args.dgpk2])
	cmd.extend(['--pfid=' + args.pfid])
	cmd.extend(['--encrypt_tool=' + ENCRYPT_TOOL_PATH])
	cmd.extend(['--dgpk2_offset=' + str(int(soc.DGPK2_OFFSET, 16))])
	cmd.extend(['--dgpk2_lock_offset=' + str(int(soc.DGPK2_LOCK_OFFSET, 16))])
	cmd.extend(['--dgpk2_lock_bit=' + str(int(soc.DGPK2_LOCK_BIT, 16))])
	cmd.extend(['--pfid_offset=' + str(int(soc.PFID_OFFSET, 16))])
	cmd.extend(['--pfid_lock_offset=' + str(int(soc.PFID_LOCK_OFFSET, 16))])
	cmd.extend(['--pfid_lock_bit=' + str(int(soc.PFID_LOCK_BIT, 16))])
	cmd.extend(['--efuse_size=' + str(int(soc.EFUSE_TOTAL_SIZE, 16))])
	cmd.extend(['--out_dir=' + args.out_dir])
	sub = subprocess.Popen(cmd)
	sub.communicate()

if __name__ == '__main__':
	main()
