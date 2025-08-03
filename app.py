from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/buscar', methods=['GET'])
def buscar():
    artista = request.args.get('artista')
    if not artista:
        return jsonify({"error": "Falta parámetro 'artista'"}), 400

    url = f"https://api.audius.co/v1/tracks/search?query={artista}&app_name=tuApp"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()

        resultados = []
        for track in data.get('data', [])[:10]:  # Limitar a 10 resultados
            resultados.append({
                "titulo": track.get('title'),
                "artista": track.get('user', {}).get('name'),
                "url_stream": track.get('streamUrl'),
                "portada": track.get('artwork', {}).get('url')
            })

        return jsonify(resultados)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
