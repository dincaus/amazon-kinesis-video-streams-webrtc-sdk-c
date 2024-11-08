import os
import subprocess
import sys
import time

def run_webrtc_to_kinesis(channel_name, rtsp_uri):
    # Get the root directory of the project
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Set the path to the executable in the build directory
    executable_path = os.path.join(root_dir, 'build', 'services', 'webrtc-to-kinesis')

    # Check if the executable exists
    if not os.path.isfile(executable_path):
        print(f"Executable '{executable_path}' not found. Please ensure the build is completed.")
        sys.exit(1)

    # Run the webrtc-to-kinesis service with the channel name and RTSP URI arguments
    while True:
        print(f"Starting webrtc-to-kinesis on channel '{channel_name}' with RTSP URI '{rtsp_uri}'...")
        process = subprocess.Popen([executable_path, channel_name, "rtspsrc", rtsp_uri])

        # Wait for the process to exit and restart if needed
        try:
            process.wait()
        except KeyboardInterrupt:
            print("Process interrupted. Exiting.")
            process.terminate()
            break

        print("webrtc-to-kinesis exited. Restarting in 5 seconds...")
        time.sleep(5)

if __name__ == "__main__":
    # Check if the channel name and RTSP URI are provided as command-line arguments
    if len(sys.argv) < 3:
        print("Usage: python run_webrtc.py <channel_name> <rtsp_uri>")
        sys.exit(1)

    channel_name = sys.argv[1]
    rtsp_uri = sys.argv[2]
    run_webrtc_to_kinesis(channel_name, rtsp_uri)