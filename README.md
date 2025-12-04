# Algoritmia - Intérprete de Lenguaje de Programación Musical

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![ANTLR](https://img.shields.io/badge/ANTLR-4.13.2-orange.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

**Algoritmia** es un lenguaje de programación diseñado específicamente para la composición algorítmica musical. Combina estructuras de programación tradicionales (condicionales, bucles, recursión) con primitivas musicales, permitiendo generar partituras y archivos de audio mediante código.

**[Demo en Vivo](https://algoritmia-care.onrender.com/)** | **[Repositorio](https://github.com/VictorRiveraT/Simulaci-n-Algoritmia)**

---

## Características Principales

- **Generación de Partituras**: Crea archivos PDF con notación musical profesional
- **Síntesis de Audio**: Genera archivos MIDI y WAV reproducibles
- **Recursividad**: Soporte completo para algoritmos recursivos musicales
- **Sintaxis Clara**: Diseñado para ser intuitivo tanto para músicos como programadores
- **Interfaz Web**: Editor en línea con reproducción inmediata
- **Dockerizado**: Despliegue consistente en cualquier plataforma
- **Intérprete Eficiente**: Construido con ANTLR4 para análisis léxico y sintáctico

---

## Demo Rápido

### Prueba de Ritmo y Polimorfismo ###
```algoritmia
Main |:
    <w> "Iniciando sistema..."
    
    (:) { C4:w }      ### Redonda ###
    (:) { E4:h }      ### Blanca ###
    (:) { G4:q }      ### Negra ###
    (:) { C5:e C5:e } ### Corcheas ###
    
    <w> "Transponiendo..."
    base <- C3:q
    (:) { base (base + 4) (base + 7) }
:|
```

**Salida:**
- Consola: `Prueba de Ritmo y Polimorfismo`
- Genera: `output.pdf`, `output.midi`, `output.wav`
- Audio: Escala de Do mayor (Do, Re, Mi, Fa, Sol, La, Si, Do)

### Torres de Hanoi Musical
```algoritmia
### Hanoi con música ###

Hanoi |:
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
:|
```

Genera una melodía de 31 notas que representa los movimientos de las Torres de Hanoi con 5 discos.

---

## Instalación

### Opción 1: Uso Web (Recomendado)
Accede directamente a: **[algoritmia-care.onrender.com](https://algoritmia-care.onrender.com/)**

No requiere instalación local.

### Opción 2: Instalación Local

#### Requisitos Previos
- Python 3.9 o superior
- LilyPond
- Timidity++

#### Linux/Ubuntu
```bash
# Instalar dependencias del sistema
sudo apt-get update
sudo apt-get install -y lilypond timidity freepats

# Clonar repositorio
git clone https://github.com/VictorRiveraT/Simulaci-n-Algoritmia.git
cd Simulaci-n-Algoritmia

# Instalar dependencias Python
pip install -r requirements.txt
```

#### macOS
```bash
# Instalar dependencias con Homebrew
brew install lilypond timidity

# Clonar y configurar
git clone https://github.com/VictorRiveraT/Simulaci-n-Algoritmia.git
cd Simulaci-n-Algoritmia
pip install -r requirements.txt
```

#### Windows
```bash
# 1. Descargar e instalar LilyPond desde: https://lilypond.org/download.html
# 2. Descargar e instalar Timidity++ desde: https://sourceforge.net/projects/timidity/

# 3. Clonar repositorio
git clone https://github.com/VictorRiveraT/Simulaci-n-Algoritmia.git
cd Simulaci-n-Algoritmia

# 4. Instalar dependencias Python
pip install -r requirements.txt
```

### Opción 3: Docker
```bash
# Construir imagen
docker build -t algoritmia .

# Ejecutar contenedor
docker run -p 5000:5000 algoritmia

# Acceder en: http://localhost:5000
```

---

## Uso

### Línea de Comandos
```bash
# Ejecutar un programa (comienza desde Main)
python algoritmia.py programa.alg

# Ejecutar desde un procedimiento específico
python algoritmia.py programa.alg NombreProcedimiento
```

**Ejemplo:**
```bash
python algoritmia.py ejemplos/hanoi.alg
# Genera: hanoi.pdf, hanoi.midi, hanoi.wav
```

### Aplicación Web

1. Escribe tu código Algoritmia en el editor
2. Haz clic en "Procesar y Componer (Generar Música)"
3. Observa la salida en consola
4. Reproduce el audio generado en el navegador
5. Descarga archivos PDF, MIDI, WAV o ZIP completo

---

## Sintaxis de Algoritmia

### Elementos Básicos

| Elemento | Sintaxis | Ejemplo |
|----------|----------|---------|
| Comentarios | `### texto ###` | `### Esto es un comentario ###` |
| Procedimientos | `Nombre params \|: ... :\|` | `Main \|: <w> "Hola" :\|` |
| Asignación | `var <- expr` | `x <- 10` |
| Lectura | `<?> var` | `<?> n` |
| Escritura | `<w> expr` | `<w> "Resultado:" x` |
| Reproducción | `(:) expr` | `(:) C` o `(:) {C E G}` |
| Condicional | `if expr \|: ... :\| else \|: ... :\|` | `if x > 0 \|: ... :\|` |
| Bucle | `while expr \|: ... :\|` | `while x > 0 \|: ... :\|` |
| Llamada | `Procedimiento arg1 arg2` | `Euclides a b` |

### Operaciones sobre Listas

| Operación | Sintaxis | Descripción |
|-----------|----------|-------------|
| Literal | `{elem1 elem2 ...}` | Crear lista |
| Acceso | `lista[i]` | Acceder al i-ésimo elemento (índice base 1) |
| Añadir | `lista << elem` | Añadir elemento al final |
| Eliminar | `8< lista[i]` | Eliminar i-ésimo elemento |
| Longitud | `#lista` | Obtener tamaño de la lista |

### Operadores

**Aritméticos:** `+`, `-`, `*`, `/`, `%`  
**Relacionales:** `=`, `/=`, `<`, `>`, `<=`, `>=`  
**Precedencia:** Igual que en C (multiplicación/división antes que suma/resta)

### Notas Musicales

Algoritmia utiliza la notación anglosajona:
- **C** = Do, **D** = Re, **E** = Mi, **F** = Fa, **G** = Sol, **A** = La, **B** = Si
- **Rango:** A0 a C8 (52 notas - teclas blancas del piano)
- **Octavas:** Se numeran del 0 al 8
- **Sin número:** Octava central (C = C4, D = D4, etc.)

**Ejemplo:**
```algoritmia
### Escala de Do mayor ###
Main |:
    (:) {C4 D4 E4 F4 G4 A4 B4 C5}
:|
```

---

## Arquitectura del Sistema
```
┌─────────────────────────────────────────┐
│         Interfaz Web (Flask)            │
│  Editor de código + Reproductor audio   │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│      Intérprete Algoritmia (Python)     │
├─────────────────────────────────────────┤
│  • AlgoritmiaLexer  (ANTLR4)            │
│  • AlgoritmiaParser (ANTLR4)            │
│  • AlgoritmiaInterpreter (Visitor)      │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│    Generación de Música                 │
├─────────────────────────────────────────┤
│  • LilyPond → PDF + MIDI                │
│  • Timidity → WAV                       │
└─────────────────────────────────────────┘
```

### Componentes Principales

- **`Algoritmia.g4`**: Especificación de la gramática en formato ANTLR4
- **`AlgoritmiaLexer.py`**: Analizador léxico generado automáticamente
- **`AlgoritmiaParser.py`**: Analizador sintáctico generado automáticamente
- **`AlgoritmiaInterpreter.py`**: Implementación del intérprete usando patrón Visitor
- **`algoritmia.py`**: Interfaz de línea de comandos
- **`app.py`**: Aplicación web Flask
- **`Dockerfile`**: Configuración para contenedorización

### Flujo de Ejecución

1. **Análisis Léxico:** El código fuente se convierte en tokens
2. **Análisis Sintáctico:** Los tokens se organizan en un árbol de sintaxis abstracta (AST)
3. **Interpretación:** El visitor recorre el AST ejecutando instrucciones
4. **Generación Musical:** Las notas se convierten a formato LilyPond
5. **Renderizado:** LilyPond genera PDF y MIDI
6. **Síntesis:** Timidity convierte MIDI a WAV

---

## Tecnologías Utilizadas

### Core
- **Python 3.9+**: Lenguaje de implementación principal
- **ANTLR 4.13.2**: Generador de analizadores léxicos y sintácticos
- **LilyPond 2.24+**: Sistema de tipografía musical profesional
- **Timidity++**: Sintetizador de software para conversión MIDI a WAV

### Web
- **Flask 3.0+**: Framework web minimalista
- **Gunicorn**: Servidor WSGI de producción
- **HTML5**: Estructura de la interfaz web
- **CSS3**: Estilos de la aplicación
- **JavaScript**: Interactividad del cliente

### DevOps
- **Docker**: Plataforma de contenedorización
- **Render**: Servicio de deployment en la nube
- **Git/GitHub**: Control de versiones

---

## Estructura del Proyecto
```
Simulaci-n-Algoritmia/
├── Algoritmia.g4                # Gramática ANTLR del lenguaje
├── Algoritmia.interp            # Archivo de interpretación ANTLR
├── Algoritmia.tokens            # Tokens definidos
├── AlgoritmiaLexer.py           # Analizador léxico generado
├── AlgoritmiaLexer.interp       # Interpretación del lexer
├── AlgoritmiaLexer.tokens       # Tokens del lexer
├── AlgoritmiaParser.py          # Analizador sintáctico generado
├── AlgoritmiaInterpreter.py     # Implementación del intérprete
├── AlgoritmiaVisitor.py         # Clase base para visitors
├── AlgoritmiaListener.py        # Clase base para listeners
├── algoritmia.py                # CLI principal
├── app.py                       # Aplicación web Flask
├── Dockerfile                   # Configuración de Docker
├── requirements.txt             # Dependencias Python
├── templates/                   # Plantillas HTML
│   └── index.html              # Interfaz web principal
├── static/                      # Archivos estáticos
│   ├── css/
│   └── js/
└── README.md                    # Este archivo
```

---

## Ejemplos Adicionales

### Algoritmo de Euclides
```algoritmia
### Calcular MCD usando el algoritmo de Euclides ###

Main |:
    <w> "Escribe dos numeros"
    <?> a
    <?> b
    Euclides a b
:|

Euclides a b |:
    while a /= b |:
        if a > b |:
            a <- a - b
        :| else |:
            b <- b - a
        :|
    :|
    <w> "Su MCD es" a
:|
```

**Entrada:** `48 18`  
**Salida:** `Su MCD es 6`

### Secuencia de Fibonacci Musical
```algoritmia
### Generar secuencia de Fibonacci y tocar notas ###

Main |:
    n <- 10
    Fibonacci n
:|

Fibonacci n |:
    a <- 0
    b <- 1
    contador <- 0
    
    while contador < n |:
        <w> a
        (:) (C + (a % 12))
        temp <- a
        a <- b
        b <- temp + b
        contador <- contador + 1
    :|
:|
```

### Todas las Teclas del Piano
```algoritmia
### Tocar todas las teclas blancas del piano ###

All_Keys |:
    note <- A0
    while note <= C8 |:
        (:) note
        note <- note + 1
    :|
:|
```

Genera una secuencia cromática de 52 notas desde A0 hasta C8.

---

## Equipo de Desarrollo

**Universidad Peruana Cayetano Heredia - 2025**

**Integrantes:**
- Vanesa Doris Rioja Cruz
- Victor Daniel Rivera Torres - [@VictorRiveraT](https://github.com/VictorRiveraT)
- Arny Eliu Salazar Cobian - [@ArnySalazar](https://github.com/ArnySalazar)
- Matias Dario Huerta Cruz
- Jander Huamani Salazar

**Profesor:** Mg. Wilder Nina Choquehuayta  
**Curso:** Implementación de Lenguajes de Programación  
**Facultad:** Ciencias e Ingeniería

---

## Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes, por favor:

1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Realiza commit de tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Haz push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

### Áreas de Contribución
- Mejoras en la gramática del lenguaje
- Optimizaciones del intérprete
- Nuevas funcionalidades musicales
- Corrección de bugs
- Documentación
- Ejemplos adicionales

---

## Problemas Conocidos

### Limitaciones Actuales
- **Rendimiento:** La generación de archivos puede tardar 2-4 segundos en el servidor gratuito de Render debido a recursos limitados
- **Fuentes:** LilyPond requiere fuentes específicas que pueden no estar disponibles en todos los sistemas
- **Índices:** Los índices de listas comienzan en 1 (no en 0), como especificado en el diseño del lenguaje
- **Duraciones:** Actualmente todas las notas tienen la misma duración (corchea)
- **Solo teclas blancas:** No soporta sostenidos ni bemoles

### Reportar Bugs
Para reportar bugs o solicitar nuevas características, utiliza el [issue tracker](https://github.com/VictorRiveraT/Simulaci-n-Algoritmia/issues) de GitHub.

---

## Documentación Técnica

### Especificación de la Gramática
La gramática completa está definida en `Algoritmia.g4`. El lenguaje es libre de contexto y utiliza el algoritmo ALL(*) de ANTLR para parsing.

### Patrón Visitor
El intérprete implementa el patrón Visitor, separando la lógica de interpretación de la estructura del árbol de sintaxis abstracta.

### Gestión de Memoria
- **Variables locales:** Cada invocación de procedimiento tiene su propio scope
- **Listas:** Se pasan por referencia pero se copian en asignaciones
- **Sin garbage collection:** Python maneja automáticamente la memoria

### Formato de Archivos Generados
- **PDF:** Partitura renderizada por LilyPond en formato vectorial
- **MIDI:** Archivo MIDI estándar (formato 0, tempo 120 bpm)
- **WAV:** Audio PCM 44.1kHz, 16-bit, estéreo

---

## Licencia

Este proyecto es software académico desarrollado como parte del curso de Implementación de Lenguajes de Programación en la Universidad Peruana Cayetano Heredia.

---

## Referencias y Enlaces Útiles

### Proyecto
- [Demo en Vivo](https://algoritmia-care.onrender.com/)
- [Repositorio GitHub](https://github.com/VictorRiveraT/Simulaci-n-Algoritmia)

### Tecnologías
- [Documentación de ANTLR4](https://www.antlr.org/)
- [LilyPond - Notation Reference](https://lilypond.org/doc/v2.24/Documentation/notation/)
- [Especificación MIDI 1.0](https://www.midi.org/specifications)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Documentation](https://docs.python.org/3/)

### Inspiración
- [Sonic Pi](https://sonic-pi.net/) - Live coding musical
- [ChucK](https://chuck.cs.princeton.edu/) - Programación concurrente de audio
- [SuperCollider](https://supercollider.github.io/) - Síntesis y composición algorítmica

---

## Agradecimientos

- **Mg. Wilder Nina Choquehuayta** - Por la guía y enseñanza en el curso
- **Universidad Peruana Cayetano Heredia** - Por proporcionar el espacio académico
- **Comunidad ANTLR** - Por las excelentes herramientas y documentación
- **Desarrolladores de LilyPond** - Por el software de tipografía musical
- **Desarrolladores de Timidity++** - Por el sintetizador de software

---

## Contacto

Para consultas académicas o colaboraciones:

- **Repositorio:** [github.com/VictorRiveraT/Simulaci-n-Algoritmia](https://github.com/VictorRiveraT/Simulaci-n-Algoritmia)
- **Issues:** [GitHub Issues](https://github.com/VictorRiveraT/Simulaci-n-Algoritmia/issues)

---

<div align="center">

**Algoritmia**

Desarrollado con dedicación en Lima, Perú - 2025

Universidad Peruana Cayetano Heredia

</div>


