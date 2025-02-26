#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "diffbot_description::diffbot_description" for configuration ""
set_property(TARGET diffbot_description::diffbot_description APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(diffbot_description::diffbot_description PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libdiffbot_description.so"
  IMPORTED_SONAME_NOCONFIG "libdiffbot_description.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS diffbot_description::diffbot_description )
list(APPEND _IMPORT_CHECK_FILES_FOR_diffbot_description::diffbot_description "${_IMPORT_PREFIX}/lib/libdiffbot_description.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
