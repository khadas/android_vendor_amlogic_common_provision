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

#ifndef _PROVISION_KEYWRAPPER_H_
#define _PROVISION_KEYWRAPPER_H_

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
#define PROVISION_KEY_TYPE_CIPLUS_ECP                  0x62
#define PROVISION_KEY_TYPE_NAGRA_DEV_UUID              0x71
#define PROVISION_KEY_TYPE_NAGRA_DEV_SECRET            0x72
#define PROVISION_KEY_TYPE_PFID                        0x81
#define PROVISION_KEY_TYPE_PFPK                        0x82
#define PROVISION_KEY_TYPE_YOUTUBE_SECRET              0x91
#define PROVISION_KEY_TYPE_NETFLIX_MGKID               0xA2
#define PROVISION_KEY_TYPE_WIDEVINE_CAS                0xB1
#define PROVISION_KEY_TYPE_DOLBY_ID                    0xC1
#define PROVISION_KEY_TYPE_INVALID                     0xFFFFFFFF

#ifdef __cplusplus
extern "C" {
#endif

/* out_buf: output parameter, output data buffer;
   out_size: input/output parameter,
             input: buffer size(min value: key_size + 164),
             output: encrypted keybox size;
   key_data: input parameter, raw key data;
   key_size: input parameter, raw key size(max value: 1024 * 16 - 164);
   pcpk: input parameter, pcpk data;
   pcpk_size: input parameter, pcpk size(must be equal to 16);
   pek: input parameter, pek data;
   pek_size: input parameter, pek size(must be equal to 16);
   key_type: input parameter, key type;
   encrypt_mode: input parameter, 0: factory; 1: factory user; 2: field
   ta_uuid: input parameter, be necessary by the custom key type;
   uuid_size: input parameter, uuid size(must be equal to 0 or 36)

   return value: 0: success; non 0: failed;
 */
int encrypt_keybox(
		uint8_t *out_buf,
		uint32_t *out_size,
		const uint8_t *key_data,
		uint32_t key_size,
		const uint8_t *pcpk,
		uint32_t pcpk_size,
		const uint8_t *pek,
		uint32_t pek_size,
		uint32_t key_type,
		uint32_t encrypt_mode,
		const uint8_t *ta_uuid,
		uint32_t uuid_size
		);

#ifdef __cplusplus
}
#endif

#endif /* _PROVISION_KEYWRAPPER_H_ */
