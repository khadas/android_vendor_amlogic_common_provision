#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import subprocess
import os

DEBUG_ENABLE = 0

##### T7 Efuse Configuration #####
SC2_EFUSE_ENTIRE_SIZE       = 1024
EFUSE_PATTERN_OUTPUT = "t7_dgpk_efuse_pattern"
EFUSE_ENCRYPT_TOOL = "./aml_encrypt_t7"

##### DGPK Configuration #####
DGPK_1_CONFIG = {
    'name': 'DGPK_1',
    'key_block': 228,
    'key_offset': 0x340,
    'key_size': 16,
    'lock_block': 29,
    'lock_offset': 0x1D6,
    'lock_bit': 4,
}
DGPK_2_CONFIG = {
    'name': 'DGPK_2',
    'key_block': 229,
    'key_offset': 0x350,
    'key_size': 16,
    'lock_block': 29,
    'lock_offset': 0x1D6,
    'lock_bit': 5,
}
DGPK_CONFIGS = [
    DGPK_1_CONFIG,
    DGPK_2_CONFIG,
]


def get_args():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--cfg', required = True, \
            help = 'Keyladder config file')
    parser.add_argument('--in', type = str, dest = 'inf', default = 'null', \
            help = 'Input Efuse pattern binary')
    parser.add_argument('--out', type = str, default = 'null', \
            help = 'Output Efuse pattern binary')
    return parser.parse_args()

def write_key(outf, array, idx, key_value):
    # write key value
    value_offset = array[idx]['key_offset']
    outf.seek(value_offset)
    outf.write(key_value)
    # write lock bit
    lock_block = array[idx]['lock_block']
    lock_offset = array[idx]['lock_offset']
    lock_bit = array[idx]['lock_bit']
    outf.seek(lock_offset)
    lock_byte = outf.read(1)
    lock_value = int(lock_byte.hex(), 16)
    lock_value |= (1 << lock_bit)
    outf.seek(lock_offset)
    outf.write(lock_value.to_bytes(1, byteorder='little'))

def parse_dgpk_config(item, outf):
    name = item.get('name')
    if 'DGPK_1' in name:
        idx = 0
    elif 'DGPK_2' in name:
        idx = 1
    else:
        print("Wrong DGPK config!")
        os._exit(0)

    value = item.find('value').text
    value_bytes = bytes.fromhex(value.replace('0x', ''))
    write_key(outf, DGPK_CONFIGS, idx, value_bytes)

def parse_lockable_config(root, offset, outf):
    lock_array = [0] * 16
    for item in root.findall('bit'):
        bit = int(item.text)
        index = int(bit/8)
        lock_array[index] |= (1 << (bit % 8))
#    print(bytes(lock_array).hex())
    for i in range(16):
        write_offset = offset + i
        outf.seek(write_offset)
        outf.write(lock_array[i].to_bytes(1, byteorder='little'))

def parse_efuse_config(cfg, outf):
    tree = ET.parse(cfg)
    root = tree.getroot()

    for item in root.findall('item'):
        name = item.get('name')
        try:
            block = item.find('block').text
            offset = int(item.find('offset').text, 0)
        except:
            block = 0
            offset = 0

        if DEBUG_ENABLE:
            print("Item Name:%s, block:%s, offset:%s" %(name, block, offset))
        if 'ETSI_KL_CONFIG' in name:
            parse_etsi_config(item, outf)
        elif 'OTP_LOCK_CONFIG' in name:
            parse_lockable_config(item, offset, outf)
        elif 'DGPK' in name:
            parse_dgpk_config(item, outf)
        elif 'ETSI_SCK' in name:
            parse_etsi_sck_config(item, outf)
        else:
            value = item.find('value').text
            value_bytes = bytes.fromhex(value.replace('0x', ''))
            outf.seek(offset)
            outf.write(value_bytes)


def main():
    import struct
    import binascii

    # read input efuse pattern
    args = get_args()
    if not args.inf == 'null':
        try:
            inf = open(args.inf, 'rb+')
            raw_data = inf.read()
            inf.close
        except:
            print ("Open File: %s fail!", args.inf)
    else:
        raw_data = bytes(SC2_EFUSE_ENTIRE_SIZE)

    # generage efuse pattern with all zero
    if args.out == 'null':
        args.out = EFUSE_PATTERN_OUTPUT
    try:
        outf = open(args.out, 'wb+')
        outf.write(raw_data)
    except:
        print ("Open File: %s fail!" %(args.out))


    # parse efuse configuration
    parse_efuse_config(args.cfg, outf)
    outf.close()

    # generate efuse pattern
    subprocess.run([EFUSE_ENCRYPT_TOOL, "--efsproc", "--input", args.out])

    print('Generating Efuse Pattern ...')
    print('    Input:                efue_config = ' + args.cfg)
    print('    Output:       clear_efuse_pattern = ' + args.out)
    print('             obfuscated_efuse_pattern = %s.efuse' %(args.out))



if __name__ == "__main__":
    main()
