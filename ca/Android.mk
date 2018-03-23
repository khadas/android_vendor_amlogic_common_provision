LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_SRC_FILES_32 := lib/libprovision.so
LOCAL_SRC_FILES_64 := lib64/libprovision.so
LOCAL_MODULE := libprovision
LOCAL_MULTILIB := both
LOCAL_MODULE_SUFFIX := .so
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
include $(BUILD_PREBUILT)

include $(CLEAR_VARS)
LOCAL_MODULE_TAGS := optional

ifeq ($(TARGET_ARCH), arm)
LOCAL_SRC_FILES := bin/tee_provision
else
LOCAL_SRC_FILES := bin64/tee_provision
endif

LOCAL_MODULE := tee_provision
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_MODULE_PATH := $(PRODUCT_OUT)/vendor/bin
include $(BUILD_PREBUILT)
