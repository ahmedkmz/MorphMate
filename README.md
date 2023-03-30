<h1>MorphMate</h1>

<p>MorphMate is a Python script that compresses video files in a media library while maintaining their quality. It uses the FFmpeg library to reduce the file size of video files in .mp4, .mkv, and .avi formats.</p>

<h2>Features</h2>

<ul>
  <li>Compression of media files using the FFmpeg library</li>
  <li>Maintains quality of compressed video files</li>
  <li>Supports two video codecs for compression: libx265 and libx264</li>
  <li>Processes all video files in a specified media library folder and its subfolders</li>
  <li>Provides user prompts for compression type, CRF option, media library folder path, and GPU acceleration preference</li>
  <li>Handles detailed error handling, including file skipping and progress updates during compression</li>
  <li>Skips files that do not start converting after 30 seconds due to errors in the media file</li>
  <li>Replaces the original file with the compressed version after a successful compression</li>
  <li>Can be used with large media libraries, such as those used in Plex</li>
</ul>

<h2>Requirements</h2>

<ul>
  <li>Python 3.x</li>
  <li>FFmpeg</li>
</ul>

<h2>Installation</h2>

<p>Before using MorphMate, you need to install the FFmpeg library on your system. Here are the installation steps:</p>

<h3>Windows</h3>

<p>Download a build of FFmpeg from the official website: <a href="https://ffmpeg.org/download.html#build-windows">https://ffmpeg.org/download.html#build-windows</a></p>
<p>Extract the contents of the downloaded archive to a folder of your choice.</p>
<p>Add the FFmpeg bin folder to your system's PATH environment variable.</p>

<h3>macOS</h3>

<p>Install FFmpeg using Homebrew by running the following command:</p>
<p><code>brew install ffmpeg</code></p>

<h3>Linux (Ubuntu)</h3>

<p>Install FFmpeg using apt-get by running the following command:</p>
<p><code>sudo apt-get install ffmpeg</code></p>



<h2>Usage</h2>

<ol>
  <li>Clone the MorphMate repository: <code>git clone https://github.com/yourusername/MorphMate.git</code></li>
  <li>Navigate to the MorphMate directory: <code>cd MorphMate</code></li>
  <li>Run the script: <code>python morphmate.py</code></li>
  <li>Follow the prompts to select the compression type, CRF option, media library folder path, and GPU acceleration preference</li>
  <li>Wait for the script to finish processing all video files in the specified media library folder and its subfolders</li>
  <li>If a file does not start converting for 30 seconds, the script will skip to the next file.<b>or press ENTER</b> to skip</li>
</ol>

<h2>Error Handling</h2>

<p>MorphMate handles detailed error handling during the compression process. If an error occurs during the compression of a file, the script will skip that file and move on to the next file. Additionally, the script provides progress updates during the compression process to keep the user informed. If a file does not start converting for 30 seconds due to an error in the media file, the script will skip to the next file.</p>

<h2>License</h2>

<p>MorphMate is licensed under the MIT License with Non-Commercial/Attribution Clause. See the <code>LICENSE</code> file for details.</p>


<h2>Contributing</h2>

<p>Contributions are welcome! If you would like to contribute to this project, please create a new branch and submit a pull request with your changes. Please ensure that your changes adhere to the project's code style.</p>


<h2>Credits</h2>

<p>MorphMate was created by Ahmedkmz.</p>
