from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route("/buscar", methods=["GET"])
def buscar_musica():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Parámetro 'q' requerido"}), 400

    try:
        ydl_opts = {
            "quiet": True,
            "extract_flat": True,
            "forcejson": True,
            "skip_download": True,
            "default_search": "ytsearch10",  # Busca los 10 primeros resultados
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(query, download=False)

        resultados = []
        for entry in result.get("entries", []):
            if "title" in entry:
                resultados.append({
                    "titulo": entry.get("title"),
                    "url": f"https://www.youtube.com/watch?v={entry.get('id')}",
                    "canal": entry.get("uploader"),
                    "id": entry.get("id"),
                    "thumbnail": entry.get("thumbnail")
                })

        return jsonify(resultados)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
