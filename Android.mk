LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_SRC_FILES_32 := ca/lib/libprovision.so
LOCAL_SRC_FILES_64 := ca/lib64/libprovision.so
LOCAL_MODULE := libprovision
LOCAL_MULTILIB := both
LOCAL_MODULE_SUFFIX := .so
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
include $(BUILD_PREBUILT)

include $(CLEAR_VARS)
ifeq ($(TARGET_ENABLE_TA_SIGN), true)
ifeq ($(TARGET_ENABLE_TA_ENCRYPT), true)
ENCRYPT := --encrypt=1
else
ENCRYPT := --encrypt=0
endif
$(info $(shell mkdir $(ANDROID_BUILD_TOP)/$(LOCAL_PATH)/ta/signed))
$(info $(shell $(ANDROID_BUILD_TOP)/vendor/amlogic/tdk/ta_export/scripts/sign_ta_auto.py \
		--in=$(ANDROID_BUILD_TOP)/$(LOCAL_PATH)/ta/e92a43ab-b4c8-4450-aa12b1516259613b.ta \
		--out=$(ANDROID_BUILD_TOP)/$(LOCAL_PATH)/ta/signed/e92a43ab-b4c8-4450-aa12b1516259613b.ta \
		$(ENCRYPT)))
LOCAL_SRC_FILES := ta/signed/e92a43ab-b4c8-4450-aa12b1516259613b.ta
else
LOCAL_SRC_FILES := ta/e92a43ab-b4c8-4450-aa12b1516259613b.ta
endif

LOCAL_MODULE := e92a43ab-b4c8-4450-aa12b1516259613b
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
LOCAL_MODULE_SUFFIX := .ta
LOCAL_MODULE_PATH := $(PRODUCT_OUT)/system/lib/teetz
LOCAL_STRIP_MODULE := false
include $(BUILD_PREBUILT)

include $(CLEAR_VARS)
LOCAL_MODULE_TAGS := optional
ifeq ($(TARGET_ARCH),arm)
LOCAL_SRC_FILES := ca/bin/tee_provision
else
LOCAL_SRC_FILES := ca/bin64/tee_provision
endif
LOCAL_MODULE := tee_provision
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_MODULE_PATH := $(PRODUCT_OUT)/system/bin
include $(BUILD_PREBUILT)

include $(CLEAR_VARS)
LOCAL_MODULE := tee_provision_ta
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
LOCAL_REQUIRED_MODULES := e92a43ab-b4c8-4450-aa12b1516259613b
include $(BUILD_PHONY_PACKAGE)
