#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import subprocess
import os

DEBUG_ENABLE = 0

##### SC2 Efuse Configuration #####
SC2_EFUSE_ENTIRE_SIZE       = 4096
EFUSE_PATTERN_OUTPUT = "sc2_dgpk_efuse_pattern"
EFUSE_ENCRYPT_TOOL = "./aml_encrypt_sc2"

##### DGPK Configuration #####
DGPK_1_CONFIG = {
    'name': 'DGPK_1',
    'key_block': 228,
    'key_offset': 0xE40,
    'key_size': 16,
    'lock_block': 31,
    'lock_offset': 0x1FC,
    'lock_bit': 4,
}
DGPK_2_CONFIG = {
    'name': 'DGPK_2',
    'key_block': 229,
    'key_offset': 0xE50,
    'key_size': 16,
    'lock_block': 31,
    'lock_offset': 0x1FC,
    'lock_bit': 5,
}
DGPK_CONFIGS = [
    DGPK_1_CONFIG,
    DGPK_2_CONFIG,
]

##### ETSI Configuration #####
ETSI_SCK_0_CONFIG = {
    'name': 'ETSI_SCK_0',
    'key_block': 232,
    'key_offset': 0xE80,
    'key_size': 16,
    'lock_block': 31,
    'lock_offset': 0x1FD,
    'lock_bit': 0,
}
ETSI_SCK_1_CONFIG = {
    'name': 'ETSI_SCK_1',
    'key_block': 233,
    'key_offset': 0xE90,
    'key_size': 16,
    'lock_block': 31,
    'lock_offset': 0x1FD,
    'lock_bit': 1,
}
ETSI_SCK_2_CONFIG = {
    'name': 'ETSI_SCK_0',
    'key_block': 234,
    'key_offset': 0xEA0,
    'key_size': 16,
    'lock_block': 31,
    'lock_offset': 0x1FD,
    'lock_bit': 2,
}
ETSI_SCK_3_CONFIG = {
    'name': 'ETSI_SCK_0',
    'key_block': 235,
    'key_offset': 0xEB0,
    'key_size': 16,
    'lock_block': 31,
    'lock_offset': 0x1FD,
    'lock_bit': 3,
}
ETSI_SCK_CONFIGS = [
    ETSI_SCK_0_CONFIG,
    ETSI_SCK_1_CONFIG,
    ETSI_SCK_2_CONFIG,
    ETSI_SCK_3_CONFIG,
]

ETSI_KL_0_CONFIG = {
    'name': 'ETSI_KL_CONFIG_0',
    'block': 14,
    'offset': 0xE0,
}
ETSI_KL_1_CONFIG = {
    'name': 'ETSI_KL_CONFIG_1',
    'block': 14,
    'offset': 0xE4,
}
ETSI_KL_2_CONFIG = {
    'name': 'ETSI_KL_CONFIG_2',
    'block': 14,
    'offset': 0xE8,
}
ETSI_KL_3_CONFIG = {
    'name': 'ETSI_KL_CONFIG_3',
    'block': 14,
    'offset': 0xEC,
}

ETSI_KL_CONFIGS = [
    ETSI_KL_0_CONFIG,
    ETSI_KL_1_CONFIG,
    ETSI_KL_2_CONFIG,
    ETSI_KL_3_CONFIG,
]
ETSI_TEE_BITS_OFFSET        = 31
ETSI_ALGO_BITS_OFFSET       = 29
ETSI_MASKID_BITS_OFFSET     = 27
ETSI_WITH_MID_BITS_OFFSET   = 26
ETSI_KL_LEVEL_BITS_OFFSET   = 24
ETSI_VID_BITS_OFFSET_0      = 8
ETSI_VID_BITS_OFFSET_1      = 16
ETSI_MRK_BITS_OFFSET        = 0

ETSI_ALGO_TDES              = 0
ETSI_ALGO_AES_DECRYPT       = 1
ETSI_ALGO_AES_ENCRYPT       = 2


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

def parse_etsi_sck_config(item, outf):
    name = item.get('name')
    if 'ETSI_SCK_0' in name:
        idx = 0
    elif 'ETSI_SCK_1' in name:
        idx = 1
    elif 'ETSI_SCK_2' in name:
        idx = 2
    elif 'ETSI_SCK_3' in name:
        idx = 3
    else:
        print("Wrong ETSI SCK config: %s!" %(name))
        os._exit(0)

    value = item.find('value').text
    value_bytes = bytes.fromhex(value.replace('0x', ''))
    write_key(outf, ETSI_SCK_CONFIGS, idx, value_bytes)

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

def parse_etsi_profile(algo, with_mid, item):
    if algo is ETSI_ALGO_TDES and with_mid is 0:
        profile_name = 'Profile 1 - TDES Profile'
    elif algo is ETSI_ALGO_TDES and with_mid is 1:
        profile_name = 'Profile 1a - TDES Profile with Module Key'
    elif algo is ETSI_ALGO_AES_ENCRYPT and with_mid is 0:
        profile_name = 'Profile 2 - AES Encrypt Profile'
    elif algo is ETSI_ALGO_AES_ENCRYPT and with_mid is 1:
        profile_name = 'Profile 2a - AES Encrypt Profile with Module Key'
    elif algo is ETSI_ALGO_AES_DECRYPT and with_mid is 1:
        profile_name = 'Profile 2b - AES Decrypt Profile with Module Key'
    else:
        profile_name = 'Wrong profile'
        print('%s, Please check algo and with_mid field in %s' \
                %(profile_name, item.get('name')))
        os._exit(0)

    return profile_name

def parse_etsi_config(item, outf):
    for element in ETSI_KL_CONFIGS:
        if element['name'] in item.get('name'):
            offset = element['offset']
            found = 1
            break

    if found is 0:
        print("Wrong ETSI KL config!")
        os._exit(0)

    tee = int(item.find('tee').text)
    algo = int(item.find('algo').text)
    maskid = int(item.find('maskid').text)
    with_mid = int(item.find('with_mid').text)
    level = int(item.find('level').text)
    vid_str = item.find('vid').text
    vid_bytes = bytearray.fromhex(vid_str.replace('0x', ''))
    mrk = int(item.find('mrk').text)

    profile_name = parse_etsi_profile(algo, with_mid, item)
    config = (tee << ETSI_TEE_BITS_OFFSET |
                algo << ETSI_ALGO_BITS_OFFSET |
                maskid << ETSI_MASKID_BITS_OFFSET |
                with_mid << ETSI_WITH_MID_BITS_OFFSET |
                level << ETSI_KL_LEVEL_BITS_OFFSET |
                vid_bytes[0] << ETSI_VID_BITS_OFFSET_0 |
                vid_bytes[1] << ETSI_VID_BITS_OFFSET_1 |
                mrk << ETSI_MRK_BITS_OFFSET)
    if DEBUG_ENABLE:
        print('------ETSI Configuration------')
        print('%s' %(profile_name))
        print('tee:%d' %(tee))
        print('algo:%d' %(algo))
        print('maskid:%d' %(maskid))
        print('with_mid:%d' %(with_mid))
        print('level:%d' %(level))
        print('vid:0x%x, 0x%x' %(vid_bytes[0], vid_bytes[1]))
        print('mrk:%d' %(mrk))
        print('config:0x%x' %(config))
        print('------------------------------')

    value = config.to_bytes(4, byteorder='little')
    outf.seek(offset)
    outf.write(value)

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
