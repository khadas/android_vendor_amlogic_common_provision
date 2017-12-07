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

#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <sys/stat.h>

#include <provision_api.h>

#define PROVISION_DEBUG 0
#define PROVISION_LOG_TAG "[PROVISION-CA] "

#if PROVISION_DEBUG
#define LOGD(arg...) fprintf(stderr, PROVISION_LOG_TAG arg)
#else
#define LOGD(arg...)
#endif
#define LOGR(arg...) fprintf(stderr, arg)
#define LOGI(arg...) fprintf(stderr, PROVISION_LOG_TAG arg)
#define LOGE(arg...) fprintf(stderr, PROVISION_LOG_TAG arg)

#define PROVISION_FILENAME_LENGTH (32)
#define PROVISION_BUFFER_LENGTH   (16 * 1024)

#define PROVISION_TOOL_NAME       "tee_provision"
#define PROVISION_TOOL_VERSION    "0.1"

#define PROVISION_OP_STORE         0x1
#define PROVISION_OP_QUERY         0x2
#define PROVISION_OP_LIST          0x3

static unsigned char data_buff[PROVISION_BUFFER_LENGTH] = { 0 };

struct s_key_type {
	char *name;
	uint32_t type;
};
static struct s_key_type provision_keys[] = {
	{
		.name = "KEY_WIDEVINE",
		.type = PROVISION_KEY_TYPE_WIDEVINE,
	},
	{
		.name = "KEY_PLAYREADY_PRIVATE",
		.type = PROVISION_KEY_TYPE_PLAYREADY_PRIVATE,
	},
	{
		.name = "KEY_PLAYREADY_PUBLIC",
		.type = PROVISION_KEY_TYPE_PLAYREADY_PUBLIC,
	},
	{
		.name = "KEY_HDCP_14",
		.type = PROVISION_KEY_TYPE_HDCP_14,
	},
	{
		.name = "KEY_HDCP_22",
		.type = PROVISION_KEY_TYPE_HDCP_22,
	},
};

static int provision_list(void);

static void usage(void)
{
	LOGR("Amlogic Provision Tool v" PROVISION_TOOL_VERSION "\n");
	LOGR("Usage: %s [-t <type>] [-i <file>]"
		" [-q] [-l] [-v] [-h]\n", PROVISION_TOOL_NAME);
	LOGR("\n");
	LOGR("  -i, --in            Input data file\n");
	LOGR("  -t, --type          Specify key type\n");
	LOGR("  -q, --query         Query key provisioned or not\n");
	LOGR("  -l, --list          List all key types\n");
	LOGR("  -v, --version       Show tool version\n");
	LOGR("  -h, --help          Show this help\n");
}

static void check_key_file(char *key_file)
{
	if (!key_file) {
		usage();
		exit(-1);
	}
}

static void check_key_type(uint32_t type)
{
	int i = 0;
	int flag = 0;

	for (; i < (int)(sizeof(provision_keys) / sizeof(struct s_key_type)); i++) {
		if (type == provision_keys[i].type) {
			flag = 1;
			break;
		}
	}

	if (flag == 0) {
		LOGR("key type: 0x%x not supported.\n", type);
		provision_list();
		exit(-1);
	}
}

static char *get_key_name_by_type(uint32_t type)
{
	int i = 0;
	char *name = NULL;

	for (; i < (int)(sizeof(provision_keys) / sizeof(struct s_key_type)); i++) {
		if (type == provision_keys[i].type) {
			name = provision_keys[i].name;
			break;
		}
	}

	return name;
}
static int provision_store(int32_t key_type, char *file)
{
	int ret = 0;
	struct stat statbuf;
	int data_size = 0;
	FILE *fp = NULL;

	fp = fopen(file, "rb");
	if (!fp) {
		LOGE("open %s failed\n", file);
		ret = -1;
		goto exit;
	}
	stat(file, &statbuf);
	data_size = statbuf.st_size;
	if (data_size > PROVISION_BUFFER_LENGTH) {
		LOGE("ERROR: data size(%d) too large!\n", data_size);
		ret = -2;
		goto exit;
	}
	ret = fread(data_buff, 1, data_size, fp);
	if (ret != data_size) {
		LOGE("ERROR: data size(%d) too large!\n", data_size);
		ret = -3;
		goto exit;
	}

	ret = key_provision_store(key_type, data_buff, data_size);

	LOGI("store [0x%02x %s] %s\n",
			key_type,
			get_key_name_by_type(key_type),
			(ret == 0) ? "Okay." : "Error.");
exit:
	if (fp)
		fclose(fp);

	return ret;
}

static int provision_query(int32_t key_type)
{
	int ret = 0;

	ret = key_provision_query(key_type);
	LOGI("query [0x%02x %s] %s\n", key_type,
			get_key_name_by_type(key_type),
			(ret == 0) ? "provisioned." : "not provisioned.");

	return ret;
}

static int provision_list(void)
{
	int ret = 0;
	int i = 0;

	LOGR("Amlogic Provision Key Type List:\n");
	for (; i < (int)(sizeof(provision_keys) / sizeof(struct s_key_type)); i++) {
		LOGR("    [%d] 0x%02x %s\n", i,
				provision_keys[i].type, provision_keys[i].name);
	}

	return ret;
}


int main(int argc, char **argv)
{
	int ret = 0;
	int option_char = 0;
	int option_index = 0;
	char *data_file = NULL;
	uint32_t key_type = 0;
	uint32_t op_flag = 0;

	if (argc <= 1) {
		usage();
		exit(-1);
	}

	char *short_options = "i:t:qlvh";
	struct option long_options[] = {
		{ "in", required_argument, 0, 'i' },
		{ "type", required_argument, 0, 't' },
		{ "query", no_argument, 0, 'q' },
		{ "list", no_argument, 0, 'l' },
		{ "version", no_argument, 0, 'v' },
		{ "help", no_argument, 0, 'h' },
		{ 0, 0, 0, 0 },
	};

	while ((option_char = getopt_long(argc, argv, short_options,
					long_options, &option_index)) != -1) {
		switch (option_char) {
		case 'i':
			op_flag = PROVISION_OP_STORE;
			data_file = optarg;
			break;
		case 't':
			key_type = strtol(optarg, NULL, 0);
			break;
		case 'q':
			op_flag = PROVISION_OP_QUERY;
			break;
		case 'l':
			op_flag = PROVISION_OP_LIST;
			break;
		case 'v':
			LOGR("%s v%s\n", PROVISION_TOOL_NAME, PROVISION_TOOL_VERSION);
			exit(-1);
		case 'h':
			usage();
			exit(-1);
		default:
			break;
		}
	}

	switch (op_flag) {
	case PROVISION_OP_STORE:
		check_key_type(key_type);
		check_key_file(data_file);
		ret = provision_store(key_type, data_file);
		break;
	case PROVISION_OP_QUERY:
		check_key_type(key_type);
		ret = provision_query(key_type);
		break;
	case PROVISION_OP_LIST:
		ret = provision_list();
		break;
	default:
		usage();
		break;
	}

	return ret;
}
