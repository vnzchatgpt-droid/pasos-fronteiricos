import json
import re
import requests
from bs4 import BeautifulSoup

URL = "https://www.argentina.gob.ar/seguridad/pasosinternacionales"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x86) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def extrair_pasos():
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        pasos = []
        elementos = soup.find_all(["div", "tr"], class_=re.compile(r"paso|item"))

        for elem in elementos:
            texto = elem.get_text(separator=" ", strip=True)
            if "Chile" in texto or "CHILE" in texto:
                nome_match = re.search(r"Paso\s+([A-Za-z\s]+)", texto)
                nome = (
                    nome_match.group(0) if nome_match else "Paso Fronteiriço"
                )

                status = "Sin información"
                if "Abierto" in texto or "HABILITADO" in texto:
                    status = "Abierto"
                elif "Cerrado" in texto or "INHABILITADO" in texto:
                    status = "Cerrado"

                pasos.append({"nome": nome, "status": status, "raw_text": texto})

        if not pasos:
            pasos = [
                {"nome": "Paso Cristo Redentor", "status": "Sin información"},
                {"nome": "Paso Cardenal Samoré", "status": "Sin información"},
                {"nome": "Paso Pino Hachado", "status": "Sin información"},
                {"nome": "Paso Agua Negra", "status": "Sin información"},
                {"nome": "Paso Mamuil Malal", "status": "Sin información"},
            ]

        dados_finais = {
            "ultima_atualizacao": response.headers.get("Date", ""),
            "pasos": pasos,
        }

        with open("pasos.json", "w", encoding="utf-8") as f:
            json.dump(dados_finais, f, ensure_ascii=False, indent=2)

        print("Dados salvos com sucesso em pasos.json")

    except Exception as e:
        print(f"Erro ao extrair dados: {e}")


if __name__ == "__main__":
    extrair_pasos()
