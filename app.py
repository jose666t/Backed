from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route("/search", methods=["POST"])
def buscar():
    data = request.get_json()
    query = data.get("search")

    if not query:
        return jsonify({"error": "Falta el término de búsqueda"}), 400

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "extract_flat": True,  # Solo info, sin descargar
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch15:{query}", download=False)
            resultados = []

            for video in info["entries"]:
                resultados.append({
                    "titulo": video.get("title"),
                    "url": f"https://www.youtube.com/watch?v={video.get('id')}",
                    "portada": video.get("thumbnails", [{}])[0].get("url", ""),
                    "artista": video.get("uploader")
                })

            return jsonify(resultados)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
