from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import re

app = Flask(__name__)

@app.route('/buscar')
def buscar():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Falta parámetro q'}), 400

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'quiet': True,
        'default_search': 'ytsearch1',
        'noplaylist': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        video = info['entries'][0]

        # Filtrar el stream de audio directo
        audio_url = video.get('url', '')
        title = video.get('title', '')
        thumbnail = video.get('thumbnail', '')

        return jsonify({
            'title': title,
            'thumbnail': thumbnail,
            'url': audio_url
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
