from flask import Flask, request, jsonify
import subprocess
import os
import tempfile

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # Using yt-dlp to download the video
        with tempfile.TemporaryDirectory() as tmpdirname:
            output_path = os.path.join(tmpdirname, '%(title)s.%(ext)s')
            result = subprocess.run(
                ["yt-dlp", "-o", output_path, url],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                return jsonify({"error": result.stderr}), 500

            # Get the output video file (first video file found)
            downloaded_files = os.listdir(tmpdirname)
            if not downloaded_files:
                return jsonify({"error": "No video found"}), 404

            video_file = downloaded_files[0]
            return jsonify({"message": "Download successful", "file": video_file})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
