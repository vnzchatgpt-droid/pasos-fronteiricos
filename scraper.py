import json
import requests

# URL dos dados brutos do mapa oficial do governo argentino
API_URL = "https://www.argentina.gob.ar/seguridad/pasosinternacionales"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x86) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def extrair_pasos():
    try:
        # Tenta obter a lista diretamente
        response = requests.get(API_URL, headers=headers, timeout=15)
        response.raise_for_status()

        pasos = []

        # Lista completa dos pasos entre Argentina e Chile para garantir a cobertura total
        pasos_chile = [
            {"nome": "Paso Cristo Redentor", "regiao": "Mendoza / Valparaíso"},
            {
                "nome": "Paso Cardenal Samoré",
                "regiao": "Neuquén / Los Lagos",
            },
            {"nome": "Paso Pino Hachado", "regiao": "Neuquén / Araucanía"},
            {"nome": "Paso Agua Negra", "regiao": "San Juan / Coquimbo"},
            {
                "nome": "Paso Mamuil Malal",
                "regiao": "Neuquén / Araucanía",
            },
            {"nome": "Paso Pehuenche", "regiao": "Mendoza / Maule"},
            {"nome": "Paso Futaleufú", "regiao": "Chubut / Los Lagos"},
            {
                "nome": "Paso Huemules",
                "regiao": "Chubut / Aysén",
            },
            {
                "nome": "Paso Integración Austral",
                "regiao": "Santa Cruz / Magallanes",
            },
            {
                "nome": "Paso San Francisco",
                "regiao": "Catamarca / Atacama",
            },
            {
                "nome": "Paso Pircas Negras",
                "regiao": "La Rioja / Atacama",
            },
            {
                "nome": "Paso Jama",
                "regiao": "Jujuy / Antofagasta",
            },
            {
                "nome": "Paso Sico",
                "regiao": "Salta / Antofagasta",
            },
            {
                "nome": "Paso Socompa",
                "regiao": "Salta / Antofagasta",
            },
            {
                "nome": "Paso Vergara",
                "regiao": "Mendoza / Maule",
            },
            {
                "nome": "Paso Pichachen",
                "regiao": "Neuquén / Biobío",
            },
            {
                "nome": "Paso Icalma",
                "regiao": "Neuquén / Araucanía",
            },
            {
                "nome": "Paso Carirriñe",
                "regiao": "Neuquén / Los Ríos",
            },
            {
                "nome": "Paso Hua Hum",
                "regiao": "Neuquén / Los Ríos",
            },
            {
                "nome": "Paso Pérez Rosales",
                "regiao": "Río Negro / Los Lagos",
            },
            {
                "nome": "Paso Río Encuentro",
                "regiao": "Chubut / Los Lagos",
            },
            {"nome": "Paso Coyhaique", "regiao": "Chubut / Aysén"},
            {
                "nome": "Paso Jeinimeni",
                "regiao": "Santa Cruz / Aysén",
            },
            {
                "nome": "Paso Rodolfo Roballos",
                "regiao": "Santa Cruz / Aysén",
            },
            {
                "nome": "Paso Río Don Guillermo",
                "regiao": "Santa Cruz / Magallanes",
            },
            {
                "nome": "Paso Laurita / Casas Viejas",
                "regiao": "Santa Cruz / Magallanes",
            },
            {
                "nome": "Paso San Sebastián",
                "regiao": "Tierra del Fuego / Magallanes",
            },
        ]

        # Mapeia os dados extraídos
        texto_pagina = response.text

        for paso in pasos_chile:
            nome = paso["nome"]
            status = "Sin información"

            # Busca ocorrências do nome e status na página
            if nome in texto_pagina:
                subtexto = texto_pagina[
                    texto_pagina.find(nome) : texto_pagina.find(nome) + 200
                ]
                if "HABILITADO" in subtexto or "Abierto" in subtexto:
                    status = "Abierto"
                elif "INHABILITADO" in subtexto or "Cerrado" in subtexto:
                    status = "Cerrado"

            pasos.append(
                {
                    "nome": nome,
                    "regiao": paso["regiao"],
                    "status": status,
                }
            )

        dados_finais = {
            "ultima_atualizacao": response.headers.get("Date", ""),
            "pasos": pasos,
        }

        with open("pasos.json", "w", encoding="utf-8") as f:
            json.dump(dados_finais, f, ensure_ascii=False, indent=2)

        print(f"Salvos {len(pasos)} pasos em pasos.json")

    except Exception as e:
        print(f"Erro ao extrair dados: {e}")


if __name__ == "__main__":
    extrair_pasos()
