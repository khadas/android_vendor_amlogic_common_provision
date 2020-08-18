/*
 * Copyright (C) 2014-2017 Amlogic, Inc. All rights reserved.
 *
 * All information contained herein is Amlogic confidential.
 *
 * This software is provided to you pursuant to Software License Agreement
 * (SLA) with Amlogic Inc ("Amlogic"). This software may be used
 * only in accordance with the terms of this agreement.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification is strictly prohibited without prior written permission from
 * Amlogic.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef _PROVISION_API_H_
#define _PROVISION_API_H_

/* Provision Key Type Definition */
#define PROVISION_KEY_TYPE_WIDEVINE                    0x11
#define PROVISION_KEY_TYPE_PLAYREADY_PRIVATE           0x21
#define PROVISION_KEY_TYPE_PLAYREADY_PUBLIC            0x22
#define PROVISION_KEY_TYPE_HDCP_TX14                   0x31
#define PROVISION_KEY_TYPE_HDCP_TX22                   0x32
#define PROVISION_KEY_TYPE_HDCP_RX14                   0x33
#define PROVISION_KEY_TYPE_HDCP_RX22_WFD               0x34
#define PROVISION_KEY_TYPE_HDCP_RX22_FW                0x35
#define PROVISION_KEY_TYPE_HDCP_RX22_FW_PRIVATE        0x36
#define PROVISION_KEY_TYPE_KEYMASTER                   0x41
#define PROVISION_KEY_TYPE_KEYMASTER_3                 0x42
#define PROVISION_KEY_TYPE_KEYMASTER_3_ATTEST_DEV_ID_BOX  0x43
#define PROVISION_KEY_TYPE_EFUSE                       0x51
#define PROVISION_KEY_TYPE_CIPLUS                      0x61
#define PROVISION_KEY_TYPE_NAGRA_DEV_UUID              0x71
#define PROVISION_KEY_TYPE_NAGRA_DEV_SECRET            0x72
#define PROVISION_KEY_TYPE_PFID                        0x81
#define PROVISION_KEY_TYPE_PFPK                        0x82
#define PROVISION_KEY_TYPE_NETFLIX_MGKID               0xA2
#define PROVISION_KEY_TYPE_WIDEVINE_CAS                0xB1
#define PROVISION_KEY_TYPE_INVALID                     0xFFFFFFFF

// PFID: Provision Feild ID
#define PROVISION_PFID_LENGTH                          (16)

// DAC: Device Authentication Code
#define PROVISION_DAC_LENGTH                           (32)

#define PROVISION_KEY_CHECKSUM_LENGTH                  (32)

#define TEE_STORAGE_PRIVATE_REE      0x80000000
#define TEE_STORAGE_PRIVATE_RPMB     0x80000100

int32_t key_provision_store(
		uint8_t *name_buff,
		uint32_t name_size,
		uint8_t *key_buff,
		uint32_t key_size);

int32_t key_provision_query(
		uint8_t *name_buff,
		uint32_t name_size,
		uint32_t key_type,
		uint32_t *storage,
		uint32_t *key_size);

int32_t key_provision_query_v2(
		uint8_t *name_buff,
		uint32_t name_size,
		uint32_t key_type,
		uint8_t *uuid,
		uint32_t *storage,
		uint32_t *key_size);

int32_t key_provision_get_pfid(uint8_t *pfid, uint32_t *id_size);
int32_t key_provision_get_dac(uint8_t *dac, uint32_t *dac_size);

int32_t key_provision_checksum(uint32_t key_type, uint8_t *name_buff,
		uint32_t name_size, uint8_t *checksum);

int32_t key_provision_checksum_v2(uint32_t key_type, uint8_t *name_buff,
		uint32_t name_size, uint8_t *uuid, uint8_t *checksum);

int32_t key_provision_delete(uint32_t key_type, const uint8_t* uuid);

#endif /* _PROVISION_API_H_ */
