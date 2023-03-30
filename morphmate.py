import os
import sys
import subprocess
from pathlib import Path
import threading
import time
from queue import Queue

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def try_import(module_name, package_name=None):
    if package_name is None:
        package_name = module_name

    try:
        return __import__(module_name)
    except ImportError:
        print(f"Installing {package_name}...")
        install_package(package_name)
        return __import__(module_name)

ffmpeg = try_import("ffmpeg", "ffmpeg-python")
pyfiglet = try_import("pyfiglet")
termcolor = try_import("termcolor")
tqdm_module = try_import("tqdm")

from termcolor import colored
from tqdm import tqdm
import ffmpeg
import pyfiglet

def print_colored(text, color):
    print(colored(text, color))

banner = pyfiglet.figlet_format("MorphMate v1.0")
print_colored(banner, 'cyan')

welcome_message = r"""
Welcome to MorphMate - the Media File Compressor!

||| Written by AhmedKmz |||

This Python script helps you compress video files in your media library using the FFmpeg library.
The purpose of this script is to reduce the file size of your media files while maintaining their quality.

The script supports two video codecs for compression:

1. libx265 - H.265/HEVC (Higher compression rate, slower encoding, smaller file size)

2. libx264 - H.264/AVC (Lower compression rate, faster encoding, larger file size)

You can choose the desired compression type and the script will process all video files in the specified
media library folder and its subfolders. It supports .mp4, .mkv, and .avi video formats.

After compressing each file, the script will delete the original file and replace it with the compressed version.



"""

print_colored(welcome_message, 'yellow')

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def get_duration(file_path):
    try:
        probe = ffmpeg.probe(file_path)
        duration = float(probe['format']['duration'])
        return duration
    except Exception as e:
        print(f"Error getting duration for {file_path}: {e}")
        return None

def compress_video(input_file, output_file, compression_type, crf, use_gpu):
    if compression_type == 'libx265':
        codec = 'hevc_nvenc' if use_gpu else 'libx265'
    elif compression_type == 'libx264':
        codec = 'h264_nvenc' if use_gpu else 'libx264'
    else:
        raise ValueError("Invalid compression type")

    duration = get_duration(input_file)
    if duration is None:
        print(f"Skipping file {input_file} due to ffprobe error.")
        return

    with tqdm(total=duration, unit='s', desc=f'Compressing {os.path.basename(input_file)}') as progress_bar:
        def update_progressbar(processed_sec):
            progress_bar.update(float(processed_sec))

        try:
            args = (
                ffmpeg
                .input(input_file)
                .output(output_file, vcodec=codec, acodec='copy', crf=crf, map_metadata=0)
                .global_args('-loglevel', 'info', '-stats')
                .compile()
            )

            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            previous_time = 0
            time_zero_count = 0
            for line in process.stderr:
                if "time=" in line:
                    time_str = line.split("time=")[1].split(" ")[0]
                    time_parts = time_str.split(':')
                    processed_sec = (int(time_parts[0]) * 3600) + (int(time_parts[1]) * 60) + float(time_parts[2])
                    delta = processed_sec - previous_time
                    if delta >= 1:
                        update_progressbar(delta)
                        previous_time = processed_sec
                        time_zero_count = 0
                    else:
                        time_zero_count += delta
                        if time_zero_count >= 15:
                            print(f"Compression of file {input_file} failed due to timeout.")
                            process.kill()
                            os.remove(output_file)
                            return
                elif "error" in line.lower():
                    print(f"Compression of file {input_file} failed: {line}")
                    os.remove(output_file)
                    return

            process.wait()

            if process.returncode == 0:
                if os.path.isfile(output_file):
                    print(f"Completed {input_file} compression process.")
                    os.rename(input_file, input_file + '.bak')
                    os.rename(output_file, input_file)
                    os.remove(input_file + '.bak')
                else:
                    print(f"Compression of file {input_file} failed. Output file not found.")
                    return
            else:
                print(f"Compression of file {input_file} failed. Return code: {process.returncode}")
                os.remove(output_file)
                return

        except (ffmpeg.Error, subprocess.CalledProcessError) as e:
            print(f'Error compressing file {input_file}: {e}')
            os.remove(output_file)
            return
        except FileNotFoundError:
            print(f'Compression of file {input_file} failed due to output file not found error.')
            return

def process_directory(directory, compression_type, crf, use_gpu):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.mp4', '.mkv', '.avi')):
                input_file = os.path.join(root, file)
                temp_output_file = os.path.join(root, f'temp_compressed_{file}')
                print(f"Compressing {input_file}...")
                compress_video(input_file, temp_output_file, compression_type, crf, use_gpu)
                print(f"Compression of {input_file} complete.")


if __name__ == "__main__":
    print("Choose the compression type:")
    print("1. libx265 (Higher compression rate, slower encoding, smaller file size)")
    print("2. libx264 (Lower compression rate, faster encoding, larger file size)")

    compression_type = input("Enter the number corresponding to your choice: ")
    if compression_type == "1":
        compression_type = 'libx265'
    elif compression_type == "2":
        compression_type = 'libx264'
    else:
        print("Invalid choice.")
        sys.exit(1)

    print("\nChoose the CRF (Constant Rate Factor) option:")
    print("1. Lower quality  (Higher CRF value, smaller file size)")
    print("2. Optimal quality (Balanced CRF value, medium file size)")
    print("3. Higher quality (Lower CRF value, larger file size)")

    crf_option = input("Enter the number corresponding to your choice: ")

    if compression_type == 'libx265':
        if crf_option == "1":
            crf = '29'
        elif crf_option == "2":
            crf = '20'
        elif crf_option == "3":
            crf = '15'
        else:
            print("Invalid choice.")
            sys.exit(1)
    elif compression_type == 'libx264':
        if crf_option == "1":
            crf = '25'
        elif crf_option == "2":
            crf = '19'
        elif crf_option == "3":
            crf = '12'
        else:
            print("Invalid choice.")
            sys.exit(1)

    directory = input("\nEnter the path of the media library folder: ")

    use_gpu = input("Do you want to use GPU acceleration for compression? (yes/no): ")
    use_gpu = use_gpu.strip().lower() == "yes"

    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist. Please check the path and try again.")
        sys.exit(1)

    process_directory(directory, compression_type, crf, use_gpu)
    print("All files have been processed. Exiting the program.")

    """
MIT License with Non-Commercial/Attribution Clause

Copyright (c) 2023 Ahmedkmz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), MorphMate, to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included
   in all copies or substantial portions of the Software.

2. Commercial use of the Software is not permitted without explicit permission
   from the author. Any commercial use must include a reference to the author as
   the original author of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
