LOCAL_PATH := $(call my-dir)
TA_UUID := e92a43ab-b4c8-4450-aa12-b1516259613b
TA_SUFFIX := .ta

ifeq ($(PLATFORM_TDK_VERSION), 38)
PLATFORM_TDK_PATH := $(BOARD_AML_VENDOR_PATH)/tdk_v3
	ifeq ($(filter A311D2 POP1 S905C2 S905C2ENG S905X4 S805X2 S805X2G S905Y4, $(BOARD_AML_SOC_TYPE)),)
		LOCAL_TA := v3/$(TA_UUID)$(TA_SUFFIX)
	else
		LOCAL_TA := v3/dev/$(BOARD_AML_SOC_TYPE)/$(TA_UUID)$(TA_SUFFIX)
	endif
else
PLATFORM_TDK_PATH := $(BOARD_AML_VENDOR_PATH)/tdk
LOCAL_TA := $(TA_UUID)$(TA_SUFFIX)
endif

ifeq ($(TARGET_ENABLE_TA_ENCRYPT), true)
ENCRYPT := 1
else
ENCRYPT := 0
endif

include $(CLEAR_VARS)
LOCAL_SRC_FILES := $(LOCAL_TA)
LOCAL_MODULE := $(TA_UUID)
LOCAL_MODULE_SUFFIX := $(TA_SUFFIX)
LOCAL_STRIP_MODULE := false
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
LOCAL_MODULE_PATH := $(TARGET_OUT_VENDOR)/lib/teetz
ifeq ($(TARGET_ENABLE_TA_SIGN), true)
LOCAL_POST_INSTALL_CMD = $(PLATFORM_TDK_PATH)/ta_export/scripts/sign_ta_auto.py \
		--in=$(shell pwd)/$(LOCAL_MODULE_PATH)/$(TA_UUID)$(LOCAL_MODULE_SUFFIX) \
		--keydir=$(shell pwd)/$(BOARD_AML_TDK_KEY_PATH) \
		--encrypt=$(ENCRYPT)
endif
include $(BUILD_PREBUILT)

include $(CLEAR_VARS)
LOCAL_MODULE := tee_provision_ta
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
LOCAL_REQUIRED_MODULES := $(TA_UUID)
include $(BUILD_PHONY_PACKAGE)
