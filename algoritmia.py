import sys
from antlr4 import InputStream, CommonTokenStream
from AlgoritmiaLexer import AlgoritmiaLexer
from AlgoritmiaParser import AlgoritmiaParser
from AlgoritmiaInterpreter import AlgoritmiaInterpreter


def main():
    print(">>> Iniciando Intérprete de Algoritmia <<<")

    # Determinar el archivo de entrada y el procedimiento inicial
    if len(sys.argv) < 2:
        print("Uso: python algoritmia.py <archivo.alg> [procedimiento_inicial]")
        return

    filename = sys.argv[1]
    if not filename.endswith('.alg'):
        print("Error: El archivo debe tener la extensión .alg")
        return

    start_proc = 'Main'
    if len(sys.argv) > 2:
        start_proc = sys.argv[2]

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo: {filename}")
        return

    # 1. Crear el stream de entrada
    input_stream = InputStream(text)

    # 2. Crear Lexer y Parser
    lexer = AlgoritmiaLexer(input_stream)
    stream_tokens = CommonTokenStream(lexer)
    parser = AlgoritmiaParser(stream_tokens)

    print(f"Analizando {filename}, comenzando desde '{start_proc}'...")

    # 3. Obtener el árbol
    tree = parser.program()

    # 4. Crear e iniciar el Visitor (Intérprete)
    base_name = filename[:-4]  # quita ".alg"

    interpreter = AlgoritmiaInterpreter(start_proc)
    interpreter.output_base_name = base_name

    interpreter.visit(tree)

    print(f"\n>>> Ejecución finalizada. Revisa los archivos {base_name}.pdf, {base_name}.midi y {base_name}.wav <<<")


if __name__ == "__main__":
    main()