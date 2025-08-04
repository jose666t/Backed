from fastapi import FastAPI from fastapi.responses import JSONResponse from playwright.sync_api import sync_playwright import uvicorn

app = FastAPI()

ligas_paises = { "Premier League": {"pais": "Inglaterra", "bandera": "🇬🇧"}, "LaLiga": {"pais": "España", "bandera": "🇪🇸"}, "Serie A": {"pais": "Italia", "bandera": "🇮🇹"}, "Bundesliga": {"pais": "Alemania", "bandera": "🇩🇪"}, "Ligue 1": {"pais": "Francia", "bandera": "🇫🇷"}, "MLS": {"pais": "Estados Unidos", "bandera": "🇺🇸"}, "Liga MX": {"pais": "México", "bandera": "🇲🇽"}, "Brasileir\u00e3o": {"pais": "Brasil", "bandera": "🇧🇷"} }

@app.get("/partidos") def obtener_partidos(): with sync_playwright() as p: navegador = p.chromium.launch(headless=True) pagina = navegador.new_page() pagina.goto("https://www.livescore.com/en/football/live/") pagina.wait_for_timeout(5000)

partidos = []

    elementos_partido = pagina.locator("[data-testid='match-row']")
    total = elementos_partido.count()

    for i in range(total):
        item = elementos_partido.nth(i)
        equipo_local = item.locator("[data-testid='team-home']").inner_text()
        equipo_visitante = item.locator("[data-testid='team-away']").inner_text()
        hora_estado = item.locator("[data-testid='match-status']").inner_text()
        liga = item.locator("xpath=../../../../../../../../..//preceding-sibling::div[1]//h2").first.inner_text()

        info_liga = ligas_paises.get(liga, {"pais": "Desconocido", "bandera": "🏳️"})

        partidos.append({
            "equipo_local": equipo_local,
            "equipo_visitante": equipo_visitante,
            "hora_estado": hora_estado,
            "liga": liga,
            "pais": info_liga["pais"],
            "bandera": info_liga["bandera"]
        })

    navegador.close()
    return JSONResponse(content=partidos)

if name == "main": uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
