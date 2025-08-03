from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def download_audio():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL faltante'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'cookies': os.path.join(os.path.dirname(__file__), 'cookies.txt'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({'title': info['title'], 'url': info['webpage_url']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
