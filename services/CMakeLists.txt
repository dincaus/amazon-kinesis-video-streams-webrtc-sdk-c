cmake_minimum_required(VERSION 3.6.3)

project(WebRTCToKinesisService LANGUAGES C)

# Define necessary options or flags based on environment variables or configurations
if(IOT_CORE_ENABLE_CREDENTIALS)
    add_definitions(-DIOT_CORE_ENABLE_CREDENTIALS)
    message("Using IoT credentials in webrtc-to-kinesis sample")
endif()

# Locate necessary libraries and dependencies
find_package(PkgConfig REQUIRED)

# Check for GStreamer and other required packages
pkg_check_modules(GST REQUIRED gstreamer-1.0)
pkg_check_modules(GLIB2 REQUIRED glib-2.0)
pkg_check_modules(GST_APP REQUIRED gstreamer-app-1.0)
pkg_check_modules(GOBJ2 REQUIRED gobject-2.0)

# If GStreamer is found, set the include and library directories
if(GST_FOUND)
    if(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
        set(ENV{PKG_CONFIG_PATH} "$ENV{PKG_CONFIG_PATH}:/usr/local/opt/libffi/lib/pkgconfig")
        find_library(Intl "intl" REQUIRED PATHS "/usr/local/opt/gettext/lib")
        link_directories("/usr/local/opt/gettext/lib")
    endif()

    message("GStreamer found. Proceeding to build webrtc-to-kinesis service.")

    # Include paths for all the required libraries
    set(OPEN_SRC_INCLUDE_DIRS
            ${OPEN_SRC_INCLUDE_DIRS} ${GLIB2_INCLUDE_DIRS} ${GST_INCLUDE_DIRS}
            ${GST_APP_INCLUDE_DIRS} ${GOBJ2_INCLUDE_DIRS})

    # Libraries needed for GStreamer support
    set(GST_SAMPLE_LIBRARIES ${GLIB2_LIBRARIES} ${GST_LIBRARIES}
            ${GST_APP_LIBRARIES} ${GOBJ2_LIBRARIES} ${Intl})

    # Link directories for the libraries
    link_directories(${GLIB2_LIBRARY_DIRS} ${GST_LIBRARY_DIRS} ${GST_APP_LIBRARY_DIRS} ${GOBJ2_LIBRARY_DIRS})
else()
    message(FATAL_ERROR "GStreamer not found. Unable to build webrtc-to-kinesis service.")
endif()

# Include directories for any open-source libraries and the project's common headers
include_directories(${OPEN_SRC_INSTALL_PREFIX}/include)
include_directories(${OPEN_SRC_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}) # Include `services` directory for Samples.h and Common.c

# Add the webrtc-to-kinesis executable target and include Common.c for shared functions
add_executable(
        webrtc-to-kinesis
        webrtc-to-kinesis.c
        Common.c                   # Include Common.c as part of the executable
)

# Link the webrtc-to-kinesis executable with required libraries
target_link_libraries(webrtc-to-kinesis
        kvsWebrtcClient                  # Kinesis WebRTC core client library
        kvsWebrtcSignalingClient         # Kinesis WebRTC signaling library
        kvsCommonLws                     # Common library for Kinesis SDK
        kvspicUtils                      # Utility library for Kinesis SDK
        websockets                       # WebSockets library
        ${GST_SAMPLE_LIBRARIES}          # GStreamer libraries
)

# Install the executable into the bin directory
install(TARGETS webrtc-to-kinesis
        RUNTIME DESTINATION bin
)