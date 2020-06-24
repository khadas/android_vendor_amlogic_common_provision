LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_SRC_FILES_32 := lib/libprovision.so
LOCAL_SRC_FILES_64 := lib64/libprovision.so
LOCAL_MODULE := libprovision
LOCAL_MULTILIB := both
LOCAL_MODULE_SUFFIX := .so
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
LOCAL_PROPRIETARY_MODULE := true
LOCAL_SHARED_LIBRARIES := libteec
include $(BUILD_PREBUILT)

include $(CLEAR_VARS)
LOCAL_SRC_FILES_32 := bin/tee_provision
LOCAL_SRC_FILES_64 := bin64/tee_provision
LOCAL_MODULE := tee_provision
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_MODULE_TAGS := optional
LOCAL_PROPRIETARY_MODULE := true
LOCAL_SHARED_LIBRARIES := libteec libprovision
include $(BUILD_PREBUILT)

include $(CLEAR_VARS)
LOCAL_SRC_FILES_32 := bin/tee_key_inject
LOCAL_SRC_FILES_64 := bin64/tee_key_inject
LOCAL_INIT_RC := tee_key_inject.rc
LOCAL_MODULE := tee_key_inject
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_MODULE_TAGS := optional
LOCAL_PROPRIETARY_MODULE := true
LOCAL_SHARED_LIBRARIES := libteec libprovision
include $(BUILD_PREBUILT)
