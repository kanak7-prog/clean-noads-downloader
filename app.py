from flask import Flask, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ad-Free Media Downloader</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h2>Ad-Free Media Downloader</h2>
        <form method="POST">
            <input type="text" name="url" placeholder="Paste link here..." style="padding: 10px; width: 300px;" required><br><br>
            <button type="submit" style="padding: 10px 20px; background: green; color: white;">Download</button>
        </form>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def download():
    url = request.form.get('url')
    ydl_opts = {'format': 'best', 'outtmpl': 'downloaded_video.%(ext)s'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
      
