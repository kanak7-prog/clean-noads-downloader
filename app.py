import os
from flask import Flask, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Ad-Free Media Downloader</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f9f9f9;">
    <h2>Ad-Free Media Downloader</h2>
    <form method="POST" style="margin-top: 20px;">
        <input type="text" name="url" placeholder="https://youtube.com/shorts/..." style="width: 80%; max-width: 400px; padding: 10px; font-size: 16px;" required>
        <br><br>
        <button type="submit" style="background: #008000; color: white; padding: 10px 25px; font-size: 16px; border: none; border-radius: 4px; cursor: pointer;">Download</button>
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return "URL missing", 400
        
        download_dir = '/tmp'
        ydl_opts = {
            'format': '18',  # RAM bachane ke liye format 18 (360p) set kiya hai taaki server crash na ho
            'outtmpl': os.path.join(download_dir, 'downloaded_video.%(ext)s'),
            'extractor_args': {'youtube': {'player_client': ['android']}},
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            return send_file(filename, as_attachment=True)
        except Exception as e:
            return f"Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
