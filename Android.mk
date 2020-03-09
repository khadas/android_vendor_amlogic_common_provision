ifeq (,$(filter $(TARGET_DEVICE),sabrina))
  include $(call all-subdir-makefiles)
  #include $(call all-named-subdir-makefiles, ca ta)
endif
