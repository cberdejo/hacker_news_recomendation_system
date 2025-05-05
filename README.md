[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)


[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
# 📰 Hacker News Recommender System

Este proyecto implementa un **sistema de recomendación de noticias** usando técnicas de **procesamiento del lenguaje natural (NLP)** y **almacenamiento vectorial** en **Qdrant**. Utiliza **web scraping** para extraer noticias de [Hacker News (Algolia)](https://hn.algolia.com) y recomienda artículos a los usuarios según su historial de lectura simulado.

## 🚀 Tecnologías y modelos utilizados

- **Web scraping**: Selenium para extraer noticias desde la web.
- **NLP**: spaCy para extracción de palabras clave (sustantivos relevantes).
- **Embeddings**: Modelo `average_word_embeddings_komninos` de `sentence-transformers`.
- **Base vectorial**: Qdrant (almacenamiento local en disco).
- **Lenguaje**: Python 3.11+

## 🧠 ¿Cómo funciona el sistema?

1. **Scraping de títulos**: Se recorre automáticamente Hacker News y se extraen títulos de noticias.
2. **Procesamiento de texto**:
   - Se utilizan embeddings con `SentenceTransformer`.
   - Se extraen 2-4 *keywords* por noticia con spaCy.
3. **Vectorización y almacenamiento**: Los títulos y sus keywords se almacenan como vectores en Qdrant.
4. **Simulación de usuario**:
   - Se generan keywords y un embedding promedio a partir del historial de lectura ficticio del usuario.
5. **Recomendación**:
   - Se consultan los vectores más cercanos en Qdrant, filtrando por las *keywords* predominantes del usuario.

## 📦 Instalación

En caso de no tener uv, se puede instalar siguiendo el siguiente proceso:

1. Crea un venv
```bash
python -m venv .venv
source .venv/Scripts/activate
```
2. Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

3. Asegúrate de tener instalado Chrome y su [driver compatible](https://chromedriver.chromium.org/downloads).

## ⚙️ Ejecución
En caso de usar uv:
```bash
uv run src/main.py
```
En cualquier otro caso
```bash
python src/main.py
```


Este script:
- Scrapea noticias si la colección en Qdrant está vacía.
- Procesa los títulos y extrae embeddings y keywords.
- Simula un historial de usuario.
- Genera recomendaciones personalizadas basadas en la similitud semántica y las keywords.

## 📁 Separación en módulos

Este proyecto puede separarse en dos partes:
- **scraper.py**: Contendrá toda la lógica de scraping y procesamiento.
- **recommender.py**: Contendrá la lógica de interacciones con qdrant, preprocesamiento, algoritmo de recomendación,...
- **main.py**: Ejemplo de un programa usando las funciones de scraper.py y recommender.py

## 📌 Notas

- El modelo de embeddings utilizado (`komninos`) tiene tamaño 300 y está optimizado para eficiencia.
- El filtro por *keywords* permite que la recomendación sea más relevante y dirigida temáticamente.
- El almacenamiento en Qdrant es persistente (carpeta `./data`).
