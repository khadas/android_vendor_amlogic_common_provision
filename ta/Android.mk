LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
ifeq ($(TARGET_ENABLE_TA_SIGN), true)
ifeq ($(TARGET_ENABLE_TA_ENCRYPT), true)
ENCRYPT := --encrypt=1
else
ENCRYPT := --encrypt=0
endif
$(info $(shell mkdir $(ANDROID_BUILD_TOP)/$(LOCAL_PATH)/signed))
$(info $(shell $(ANDROID_BUILD_TOP)/vendor/amlogic/tdk/ta_export/scripts/sign_ta_auto.py \
		--in=$(ANDROID_BUILD_TOP)/$(LOCAL_PATH)/e92a43ab-b4c8-4450-aa12b1516259613b.ta \
		--out=$(ANDROID_BUILD_TOP)/$(LOCAL_PATH)/signed/e92a43ab-b4c8-4450-aa12b1516259613b.ta \
		$(ENCRYPT)))
LOCAL_SRC_FILES := signed/e92a43ab-b4c8-4450-aa12b1516259613b.ta
else
LOCAL_SRC_FILES := e92a43ab-b4c8-4450-aa12b1516259613b.ta
endif

LOCAL_MODULE := e92a43ab-b4c8-4450-aa12b1516259613b
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
LOCAL_MODULE_SUFFIX := .ta
LOCAL_MODULE_PATH := $(PRODUCT_OUT)/system/lib/teetz
LOCAL_STRIP_MODULE := false
include $(BUILD_PREBUILT)

include $(CLEAR_VARS)
LOCAL_MODULE := tee_provision_ta
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
LOCAL_REQUIRED_MODULES := e92a43ab-b4c8-4450-aa12b1516259613b
include $(BUILD_PHONY_PACKAGE)
