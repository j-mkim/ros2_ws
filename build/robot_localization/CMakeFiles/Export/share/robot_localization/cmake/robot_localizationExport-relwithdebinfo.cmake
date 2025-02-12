#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "robot_localization::rl_lib" for configuration "RelWithDebInfo"
set_property(TARGET robot_localization::rl_lib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(robot_localization::rl_lib PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/librl_lib.so"
  IMPORTED_SONAME_RELWITHDEBINFO "librl_lib.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS robot_localization::rl_lib )
list(APPEND _IMPORT_CHECK_FILES_FOR_robot_localization::rl_lib "${_IMPORT_PREFIX}/lib/librl_lib.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
