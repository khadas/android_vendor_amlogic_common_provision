#!/usr/bin/env python3
#
# Copyright (C) 2021 Amlogic, Inc. All rights reserved.
#
# This source code is subject to the terms and conditions defined in the
# file 'LICENSE' which is part of this source code package.

import sys

SOC = 'sc2'
TARGET_NAME = 'dgpk1'
SCRIPT_PATH = sys.path[0] + '/../dependents/dgpk1_derive.py'

def get_args():
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('--out_dir', type = str, default = './'+ SOC + '-' + TARGET_NAME + '/', help = 'output directory')
	return parser.parse_args()

# dgpk: device global protect key
def main():
	import os
	import sys
	import subprocess

	args = get_args()

	cmd = [sys.executable, SCRIPT_PATH]
	cmd.extend(['--soc=' + SOC])
	cmd.extend(['--out_dir=' + args.out_dir])
	sub = subprocess.Popen(cmd)
	sub.communicate()

if __name__ == '__main__':
	main()
