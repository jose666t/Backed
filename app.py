from flask import Flask, request, jsonify
from flask_cors import CORS
from yt_dlp import YoutubeDL

app = Flask(__name__)
CORS(app)  # Permite solicitudes desde cualquier origen (frontend)

@app.route('/')
def home():
    return 'Backend corriendo, bro!'

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

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            video = info['entries'][0]

            audio_url = video.get('url', '')
            title = video.get('title', '')
            thumbnail = video.get('thumbnail', '')

            return jsonify({
                'title': title,
                'thumbnail': thumbnail,
                'url': audio_url
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
