import os
import io
import base64
import tempfile
import sys
import zipfile
from flask import Flask, render_template_string, request, jsonify, send_from_directory
from antlr4 import InputStream, CommonTokenStream

# === 1. Lógica de Importación de Algoritmia ===
try:
    from AlgoritmiaLexer import AlgoritmiaLexer
    from AlgoritmiaParser import AlgoritmiaParser
    from AlgoritmiaInterpreter import AlgoritmiaInterpreter
    from AlgoritmiaValidator import AlgoritmiaValidator
except ImportError as e:
    print(f"Advertencia: No se pudieron importar los componentes de ANTLR: {e}")
    AlgoritmiaLexer = None
    AlgoritmiaParser = None
    AlgoritmiaInterpreter = None

app = Flask(__name__)

# --- Funciones Auxiliares ---

def create_zip_archive(base_path, temp_dir, code_text):
    zip_path = os.path.join(temp_dir, 'output_files.zip')
    alg_filename = "source.alg"
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.writestr(alg_filename, code_text)
        for ext, arcname in [('.pdf', 'partitura.pdf'), ('.midi', 'musica.midi'), ('.wav', 'audio.wav')]:
            file_path = f"{base_path}{ext}"
            if os.path.exists(file_path):
                zf.write(file_path, arcname=arcname)
    return os.path.basename(zip_path)

def run_algoritmia_code(code_text, temp_dir, start_proc='Main'):
    # Verificar importaciones
    if not all([AlgoritmiaLexer, AlgoritmiaParser, AlgoritmiaInterpreter, AlgoritmiaValidator]):
        return "Error: Faltan archivos del intérprete o validador.", None, None

    base_name = os.path.join(temp_dir, 'output')
    alg_file_path = f"{base_name}.alg"
    
    # Escribir archivo temporal
    try:
        with open(alg_file_path, 'w', encoding='utf-8') as f:
            f.write(code_text)
    except Exception as e:
        return f"Error escritura: {e}", None, None

    # --- AQUÍ DEFINIMOS original_stdout ANTES DEL TRY ---
    original_stdout = sys.stdout
    console_output = io.StringIO()
    sys.stdout = console_output

    try:
        # 1. Parsing (Análisis Sintáctico)
        input_stream = InputStream(code_text)
        lexer = AlgoritmiaLexer(input_stream)
        stream_tokens = CommonTokenStream(lexer)
        parser = AlgoritmiaParser(stream_tokens)
        tree = parser.program()

        # 2. VALIDACIÓN SEMÁNTICA (El Policía)
        validator = AlgoritmiaValidator()
        errors = validator.visit(tree)

        if errors:
            # Si hay errores, restauramos la consola y devolvemos el reporte
            sys.stdout = original_stdout  # <--- Ahora sí existe esta variable
            error_report = "ERRORES DE COMPILACIÓN:\n\n" + "\n".join(errors)
            # Retornamos sin generar archivos (diccionarios vacíos)
            return error_report, {}, None

        # 3. Interpretación (Ejecución real) - Solo si no hubo errores
        interpreter = AlgoritmiaInterpreter(start_proc)
        interpreter.output_base_name = base_name
        interpreter.visit(tree)

    except Exception as e:
        sys.stdout = original_stdout
        return f"Error Crítico de Ejecución: {e}", None, None
    finally:
        # Asegurarnos de devolver el control a la consola real siempre
        sys.stdout = original_stdout

    # --- Recolección de Resultados (Solo si pasó la validación) ---
    pdf_path = f"{base_name}.pdf"
    midi_path = f"{base_name}.midi"
    if not os.path.exists(midi_path): 
        midi_path = f"{base_name}.mid"
        
    wav_path = f"{base_name}.wav"
    results = {}

    if os.path.exists(pdf_path):
        results['pdf_filename'] = f"{os.path.basename(base_name)}.pdf"

    if os.path.exists(wav_path):
        with open(wav_path, 'rb') as f:
            results['wav'] = base64.b64encode(f.read()).decode('utf-8')

    if os.path.exists(midi_path):
        results['midi_filename'] = os.path.basename(midi_path)

    results['zip_filename'] = create_zip_archive(base_name, temp_dir, code_text)
    
    return console_output.getvalue(), results, temp_dir

# === Rutas Flask ===

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/run', methods=['POST'])
def run_code():
    data = request.json
    code = data.get('code', '')
    temp_dir = tempfile.mkdtemp()

    try:
        console_output, results, _ = run_algoritmia_code(code, temp_dir)
        
        if "Error" in console_output and not results:
            return jsonify({'success': False, 'output': console_output})

        return jsonify({
            'success': True,
            'output': console_output,
            'wav_base64': results.get('wav'),
            'pdf_filename': results.get('pdf_filename'),
            'midi_filename': results.get('midi_filename'),
            'zip_filename': results.get('zip_filename'),
            # AQUÍ ESTÁ LA MAGIA: Enviamos el nombre de la carpeta limpia
            'temp_id': os.path.basename(temp_dir) 
        })
    except Exception as e:
        return jsonify({'success': False, 'output': f"Server Error: {e}"})

# Rutas de Descarga/Vista
@app.route('/download/<type>/<temp_id>/<filename>')
def download_files(type, temp_id, filename):
    # Reconstruimos la ruta segura usando el directorio temporal del sistema
    directory = os.path.join(tempfile.gettempdir(), temp_id)
    
    # Determinamos MIME type
    mimetype = 'application/octet-stream'
    if type == 'pdf': mimetype = 'application/pdf'
    elif type == 'midi': mimetype = 'audio/midi'
    elif type == 'zip': mimetype = 'application/zip'
    
    # 'view' para PDF (inline), 'download' para el resto (attachment)
    as_attachment = (type != 'pdf')
    
    try:
        return send_from_directory(directory, filename, as_attachment=as_attachment, mimetype=mimetype)
    except Exception:
        return "Archivo no encontrado o expirado", 404

# === PLANTILLA HTML/JS (Con la lógica corregida) ===
# === PLANTILLA HTML/JS (DISEÑO MEJORADO v2.0) ===
HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Algoritmia Studio Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="/static/codemirror.css">
    <link rel="stylesheet" href="/static/dracula.css">
    <style>
        body { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #0f172a; color: #e2e8f0; }
        
        /* AUMENTAMOS LA ALTURA DEL EDITOR A 750px PARA VER MÁS CÓDIGO */
        .CodeMirror { 
            height: 750px !important; 
            border: 1px solid #334155; 
            border-bottom-left-radius: 0.75rem;
            border-bottom-right-radius: 0.75rem;
            font-size: 15px; 
            font-family: 'Consolas', 'Fira Code', monospace;
            line-height: 1.6;
        }
        
        /* Scrollbars personalizadas */
        ::-webkit-scrollbar { width: 10px; height: 10px; }
        ::-webkit-scrollbar-track { background: #1e293b; }
        ::-webkit-scrollbar-thumb { background: #475569; border-radius: 5px; }
        ::-webkit-scrollbar-thumb:hover { background: #64748b; }

        /* Colores de Sintaxis */
        .cm-s-dracula span.cm-keyword { color: #ff79c6; font-weight: bold; }
        .cm-s-dracula span.cm-atom { color: #bd93f9; font-weight: bold; text-shadow: 0 0 5px rgba(189, 147, 249, 0.3); }
        .cm-s-dracula span.cm-operator { color: #ffb86c; }
        .cm-s-dracula span.cm-comment { color: #6272a4; font-style: italic; }
        .cm-s-dracula span.cm-string { color: #f1fa8c; }
        .cm-s-dracula span.cm-def { color: #50fa7b; font-weight: bold; }
    </style>
</head>
<body class="h-screen flex flex-col overflow-hidden">

    <nav class="bg-slate-900 border-b border-slate-700 px-6 py-3 flex justify-between items-center shadow-md z-10">
        <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center shadow-lg shadow-purple-500/30">
                <span class="text-white font-bold text-lg">A</span>
            </div>
            <h1 class="text-2xl font-bold tracking-tight text-white">
                Algoritmia <span class="text-purple-400 font-light">Studio</span>
            </h1>
        </div>
        <div class="flex items-center gap-4">
            <div class="text-xs font-mono text-slate-500">v2.0 Stable</div>
            <div class="h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]"></div>
        </div>
    </nav>

    <div class="flex-grow p-6 overflow-y-auto">
        <div class="max-w-[1920px] mx-auto grid grid-cols-1 lg:grid-cols-12 gap-6 h-full">
            
            <div class="lg:col-span-5 flex flex-col gap-4 h-full">
                
                <div class="flex justify-between items-center bg-slate-800 p-2 rounded-t-xl border border-slate-700 border-b-0">
                    <span class="text-sm font-semibold text-slate-300 px-2 flex items-center gap-2">
                        <svg class="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path></svg>
                        Código Fuente
                    </span>
                    <button id="run-btn" onclick="run()" class="px-6 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold rounded-lg shadow-lg shadow-indigo-500/30 transition-all transform hover:scale-105 active:scale-95 flex items-center gap-2">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        COMPILAR
                    </button>
                </div>

                <div class="shadow-2xl rounded-b-xl overflow-hidden flex-grow">
                    <textarea id="alg-code">
### Torres de Hanoi ###

Main |:
    src <- {C D E F G}
    dst <- {}
    aux <- {}
    HanoiRec 5 src dst aux
:|

HanoiRec n src dst aux |:
    if n > 0 |:
        HanoiRec (n - 1) src aux dst
        note <- src[#src]
        8< src[#src]
        dst << note
        (:) note
        HanoiRec (n - 1) aux dst src
    :|
:|</textarea>
                </div>

                <div class="bg-slate-950 rounded-xl border border-slate-800 shadow-inner h-48 flex flex-col shrink-0">
                    <div class="bg-slate-900/50 px-4 py-2 text-xs font-mono text-slate-500 border-b border-slate-800 flex justify-between">
                        <span>TERMINAL OUTPUT</span>
                        <span id="status-ind" class="text-slate-600">● Idle</span>
                    </div>
                    <pre id="console" class="p-4 text-emerald-400 font-mono text-sm overflow-y-auto flex-grow">Esperando ejecución...</pre>
                </div>
            </div>

            <div class="lg:col-span-7 flex flex-col gap-6 h-full">
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    
                    <div class="bg-slate-800 p-5 rounded-2xl border border-slate-700 shadow-xl flex flex-col justify-center">
                        <h3 class="text-slate-300 font-bold mb-3 flex items-center gap-2">
                            <span class="bg-slate-700 p-1 rounded">🔊</span> Reproductor
                        </h3>
                        <audio id="player" controls class="w-full bg-slate-900 rounded-lg shadow-inner"></audio>
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                        <button onclick="dl('midi')" class="group relative bg-slate-800 hover:bg-slate-750 border border-slate-600 hover:border-blue-500 rounded-2xl p-4 flex flex-col items-center justify-center transition-all shadow-lg hover:shadow-blue-500/20">
                            <div class="p-3 bg-blue-500/10 rounded-full mb-2 group-hover:bg-blue-500/20 transition">
                                <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path></svg>
                            </div>
                            <span class="font-bold text-white">Descargar MIDI</span>
                            <span class="text-xs text-slate-400">Formato Digital</span>
                        </button>

                        <button onclick="dl('zip')" class="group relative bg-slate-800 hover:bg-slate-750 border border-slate-600 hover:border-emerald-500 rounded-2xl p-4 flex flex-col items-center justify-center transition-all shadow-lg hover:shadow-emerald-500/20">
                            <div class="p-3 bg-emerald-500/10 rounded-full mb-2 group-hover:bg-emerald-500/20 transition">
                                <svg class="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                            </div>
                            <span class="font-bold text-white">Descargar ZIP</span>
                            <span class="text-xs text-slate-400">Proyecto Completo</span>
                        </button>
                    </div>
                </div>

                <div class="bg-slate-800 rounded-2xl border border-slate-700 shadow-2xl flex-grow flex flex-col overflow-hidden h-[750px]">
                    <div class="bg-slate-900 px-5 py-3 border-b border-slate-700 flex justify-between items-center">
                        <span class="font-bold text-slate-200 flex items-center gap-2">
                            <span class="bg-slate-700 p-1 rounded text-sm">🎼</span> Partitura Generada
                        </span>
                        <a id="pdf-tab" href="#" target="_blank" class="text-xs bg-slate-800 hover:bg-slate-700 text-blue-400 px-3 py-1 rounded border border-slate-600 transition hidden">
                            Abrir en Pestaña Nueva ↗
                        </a>
                    </div>
                    
                    <div class="flex-grow relative bg-slate-700/50 backdrop-blur-sm">
                        <div id="pdf-msg" class="absolute inset-0 flex flex-col items-center justify-center text-slate-500">
                            <svg class="w-20 h-20 mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                            <p class="text-lg font-medium">La partitura aparecerá aquí</p>
                            <p class="text-sm opacity-75">Compila el código para ver el resultado</p>
                        </div>
                        
                        <iframe id="pdf-frame" class="w-full h-full bg-white hidden"></iframe>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <script src="/static/codemirror.js"></script>
    <script src="/static/simple.js"></script>
    <script>
        let editor, currentId = null, currentMidi = null, currentZip = null, currentPdf = null;

        window.onload = function() {
            try {
                CodeMirror.defineSimpleMode("algoritmia", {
                    start: [
                        {regex: /"(?:[^\\]|\\.)*?(?:"|$)/, token: "string"},
                        {regex: /###.*?###/, token: "comment"},
                        {regex: /(?:if|else|while|Main|Hanoi)\b/, token: "keyword"},
                        {regex: /\|:|:\||<-|\(:|:\)/, token: "operator"},
                        {regex: /[A-G][0-8]?(?::[whqes])?/, token: "atom"},
                        {regex: /\d+/, token: "number"},
                        {regex: /[A-Z][\w]*/, token: "def"}, 
                        {regex: /[a-z][\w]*/, token: "variable"}
                    ]
                });
                editor = CodeMirror.fromTextArea(document.getElementById("alg-code"), {
                    mode: "algoritmia", theme: "dracula", lineNumbers: true
                });
            } catch(e) { console.error(e); }
        };

        async function run() {
            const btn = document.getElementById('run-btn');
            const cons = document.getElementById('console');
            const ind = document.getElementById('status-ind');
            
            btn.disabled = true; 
            btn.innerHTML = `<svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Procesando...`;
            
            ind.innerText = "● Compilando...";
            ind.className = "text-yellow-400 animate-pulse";
            cons.innerText = ">> Enviando solicitud al servidor...\n";

            try {
                const res = await fetch('/run', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({code: editor.getValue()})
                });
                const data = await res.json();
                
                cons.innerText = ">> TERMINAL OUTPUT:\n" + (data.output || "");
                
                if(data.success) {
                    ind.innerText = "● Éxito"; ind.className = "text-emerald-400 font-bold";
                    currentId = data.temp_id; 
                    currentMidi = data.midi_filename;
                    currentZip = data.zip_filename;
                    currentPdf = data.pdf_filename;

                    if(data.wav_base64) document.getElementById('player').src = `data:audio/wav;base64,${data.wav_base64}`;
                    
                    if(currentPdf) {
                        const url = `/download/pdf/${currentId}/${currentPdf}`;
                        document.getElementById('pdf-frame').src = url;
                        document.getElementById('pdf-frame').classList.remove('hidden');
                        document.getElementById('pdf-msg').classList.add('hidden');
                        document.getElementById('pdf-tab').href = url;
                        document.getElementById('pdf-tab').classList.remove('hidden');
                    }
                } else {
                    ind.innerText = "● Error"; ind.className = "text-red-500 font-bold";
                }
            } catch(e) {
                cons.innerText += "\nError Crítico: " + e;
                ind.innerText = "● Fallo de Red"; ind.className = "text-red-500";
            }
            // Restaurar botón
            btn.disabled = false; 
            btn.innerHTML = `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg> COMPILAR`;
        }

        function dl(type) {
            if(!currentId) return alert("⚠️ Primero debes compilar el código exitosamente.");
            let file = (type === 'midi') ? currentMidi : currentZip;
            if(!file) return alert("⚠️ El archivo no se generó. Revisa la consola.");
            window.location.href = `/download/${type}/${currentId}/${file}`;
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    print("Servidor listo en http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0')
