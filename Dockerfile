# 1. Imagen base: Usamos una imagen de Python basada en Debian/Linux
FROM python:3.11-slim

# 2. Instalar binarios del sistema (LilyPond, Timidity y SoundFonts)
# La barra invertida (\) une las líneas para que Docker las lea como un solo comando RUN.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        lilypond \
        timidity \
        fluid-soundfont-gm \
    && rm -rf /var/lib/apt/lists/*

# 3. Preparar el entorno de trabajo
WORKDIR /usr/src/app

# 4. Copiar los archivos de dependencia e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código (incluyendo app.py y tus archivos ANTLR/Intérprete)
COPY . .

# 6. Comando de inicio (CORRECCIÓN CRÍTICA: Usa "sh -c" para que $PORT se expanda)
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]
