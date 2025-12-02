# Clases generadas por ANTLR
from AlgoritmiaParser import AlgoritmiaParser
from AlgoritmiaVisitor import AlgoritmiaVisitor
import subprocess
import os

# Mapeo de notas a valores (solo teclas blancas)
NOTE_MAP = {
    'A0': 0, 'B0': 1, 'C1': 2, 'D1': 3, 'E1': 4, 'F1': 5, 'G1': 6, 'A1': 7, 'B1': 8,
    'C2': 9, 'D2': 10, 'E2': 11, 'F2': 12, 'G2': 13, 'A2': 14, 'B2': 15,
    'C3': 16, 'D3': 17, 'E3': 18, 'F3': 19, 'G3': 20, 'A3': 21, 'B3': 22,
    'C4': 23, 'D4': 24, 'E4': 25, 'F4': 26, 'G4': 27, 'A4': 28, 'B4': 29,
    'C5': 30, 'D5': 31, 'E5': 32, 'F5': 33, 'G5': 34, 'A5': 35, 'B5': 36,
    'C6': 37, 'D6': 38, 'E6': 39, 'F6': 40, 'G6': 41, 'A6': 42, 'B6': 43,
    'C7': 44, 'D7': 45, 'E7': 46, 'F7': 47, 'G7': 48, 'A7': 49, 'B7': 50,
    'C8': 51
}

# Mapeo de sufijos a valores de LilyPond
# w=1 (redonda), h=2 (blanca), q=4 (negra), e=8 (corchea), s=16 (semicorchea)
DURATION_MAP = {'w': 1, 'h': 2, 'q': 4, 'e': 8, 's': 16}

# Notas sin número = registro central (octava 4)
NOTE_MAP.update({
    'C': NOTE_MAP['C4'], 'D': NOTE_MAP['D4'], 'E': NOTE_MAP['E4'],
    'F': NOTE_MAP['F4'], 'G': NOTE_MAP['G4'], 'A': NOTE_MAP['A4'], 'B': NOTE_MAP['B4']
})


class AlgoritmiaInterpreter(AlgoritmiaVisitor):
    def __init__(self, start_proc='Main'):
        self.procs = {}  # {nombre_proc: nodo_del_arbol}
        self.call_stack = []  # pila de scopes (variables locales)
        self.score = []  # lista de dicts {'pitch': int, 'duration': int}
        self.start_proc = start_proc
        self.output_base_name = "alg"  # nombre base para .pdf/.midi/.wav

    def get_current_scope(self):
        if not self.call_stack:
            self.call_stack.append({})
        return self.call_stack[-1]

    def resolve_var(self, name):
        return self.get_current_scope().get(name, 0)

    # --- Programa principal ---
    def visitProgram(self, ctx: AlgoritmiaParser.ProgramContext):
        for proc in ctx.procDecl():
            self.visit(proc)

        if self.start_proc not in self.procs:
            print(f"Error: No se encontró el procedimiento '{self.start_proc}'")
            return

        main_proc_node = self.procs[self.start_proc]
        new_scope = {}
        self.call_stack.append(new_scope)

        for stmt in main_proc_node.statement():
            self.visit(stmt)

        self.call_stack.pop()
        self.generate_music_files()

    # --- Procedimientos ---
    def visitProcDecl(self, ctx: AlgoritmiaParser.ProcDeclContext):
        proc_name = ctx.ID(0).getText()
        self.procs[proc_name] = ctx

    def visitProcCallStmt(self, ctx: AlgoritmiaParser.ProcCallStmtContext):
        proc_name = ctx.ID().getText()
        if proc_name not in self.procs:
            print(f"Error: Procedimiento '{proc_name}' no definido.")
            return

        proc_node = self.procs[proc_name]
        formal_params = [id_node.getText() for id_node in proc_node.ID()[1:]]
        argument_exprs = ctx.expression()

        if len(formal_params) != len(argument_exprs):
            print(f"Error en llamada: args incorrectos")
            return

        argument_values = [self.visit(expr) for expr in argument_exprs]
        new_scope = {}

        for name, value in zip(formal_params, argument_values):
            if isinstance(value, list):
                new_scope[name] = value 
            else:
                new_scope[name] = value

        self.call_stack.append(new_scope)
        for stmt in proc_node.statement():
            self.visit(stmt)
        self.call_stack.pop()

    # --- Instrucciones básicas ---
    def visitPlayStmt(self, ctx: AlgoritmiaParser.PlayStmtContext):
        item = self.visit(ctx.expression())

        def add_note_to_score(val):
            # Si es tupla (pitch, duracion), úsala. Si es solo int, usa default 4.
            if isinstance(val, tuple):
                p, d = val
                self.score.append({'pitch': p, 'duration': d})
            else:
                self.score.append({'pitch': val, 'duration': 4})

        if isinstance(item, list):
            for x in item:
                add_note_to_score(x)
        else:
            add_note_to_score(item)

    def visitAssignStmt(self, ctx: AlgoritmiaParser.AssignStmtContext):
        var_name = ctx.ID().getText()
        value = self.visit(ctx.expression())
        scope = self.get_current_scope()
        if isinstance(value, list):
            scope[var_name] = list(value)
        else:
            scope[var_name] = value

    def visitWriteStmt(self, ctx: AlgoritmiaParser.WriteStmtContext):
        texts_to_print = []
        for expr in ctx.expression():
            value = self.visit(expr)
            if isinstance(value, list):
                list_str = f"[{' '.join(map(str, value))}]"
                texts_to_print.append(list_str)
            else:
                texts_to_print.append(str(value))
        print(' '.join(texts_to_print))

    # --- Control de flujo ---
    def visitIfStmt(self, ctx: AlgoritmiaParser.IfStmtContext):
        condition = self.visit(ctx.expression())
        all_statements = ctx.statement()
        else_node = ctx.ELSE()
        then_statements = []
        else_statements = []

        if else_node:
            else_token_index = else_node.getSymbol().tokenIndex
            for stmt in all_statements:
                if stmt.start.tokenIndex < else_token_index:
                    then_statements.append(stmt)
                else:
                    else_statements.append(stmt)
        else:
            then_statements = all_statements

        if condition == 1:
            for stmt in then_statements:
                self.visit(stmt)
        else:
            if else_node:
                for stmt in else_statements:
                    self.visit(stmt)

    def visitWhileStmt(self, ctx: AlgoritmiaParser.WhileStmtContext):
        condition = self.visit(ctx.expression())
        while condition == 1:
            for stmt in ctx.statement():
                self.visit(stmt)
            condition = self.visit(ctx.expression())

    # --- Listas ---
    def visitListAppendStmt(self, ctx: AlgoritmiaParser.ListAppendStmtContext):
        var_name = ctx.ID().getText()
        value_to_append = self.visit(ctx.expression())
        scope = self.get_current_scope()
        list_var = scope.get(var_name)
        if list_var is None or list_var == 0:
            list_var = []
            scope[var_name] = list_var
        if isinstance(list_var, list):
            list_var.append(value_to_append)

    def visitListCutStmt(self, ctx: AlgoritmiaParser.ListCutStmtContext):
        var_name = ctx.listAccessExpr().ID().getText()
        index_val = self.visit(ctx.listAccessExpr().expression())
        scope = self.get_current_scope()
        list_var = scope.get(var_name)
        if isinstance(list_var, list):
            py_index = index_val - 1
            if 0 <= py_index < len(list_var):
                list_var.pop(py_index)
            else:
                print(f"Error: '8<' índice {index_val} fuera de rango para lista '{var_name}'")

    def visitLengthExpr(self, ctx: AlgoritmiaParser.LengthExprContext):
        target = self.visit(ctx.expression())
        if isinstance(target, list):
            return len(target)
        return 0

    def visitListAccessExpr(self, ctx: AlgoritmiaParser.ListAccessExprContext):
        var_name = ctx.ID().getText()
        index_val = self.visit(ctx.expression())
        scope = self.get_current_scope()
        list_var = scope.get(var_name)
        if isinstance(list_var, list):
            py_index = index_val - 1
            if 0 <= py_index < len(list_var):
                return list_var[py_index]
            else:
                print(f"Error: Índice {index_val} fuera de rango para lista '{var_name}'")
                return 0
        return 0
    
    # --- Helper para manejar Tuplas (Nota, Duracion) vs Enteros ---
    def _get_val(self, item):
        """Devuelve el valor numérico (pitch o entero) de un item."""
        if isinstance(item, tuple):
            return int(item[0]) # Retorna el pitch
        return int(item)

    # --- Expresiones ---
    def visitMultExpr(self, ctx: AlgoritmiaParser.MultExprContext):
        # Visitamos el primer término
        left = self.visit(ctx.term(0))
        
        for i in range(1, len(ctx.term())):
            op = ctx.getChild(2 * i - 1).getText()
            right = self.visit(ctx.term(i))
            
            # 1. Extraemos valores numéricos para la matemática
            val_l = self._get_val(left)
            val_r = self._get_val(right)
            
            # 2. Realizamos la operación
            res = 0
            if op == '*':
                res = val_l * val_r
            elif op == '/':
                res = val_l // val_r
            elif op == '%':
                res = val_l % val_r
                
            # 3. Reconstrucción inteligente:
            # Si 'left' era una nota con duración, el resultado conserva esa duración.
            if isinstance(left, tuple):
                left = (res, left[1])
            # Si 'right' era nota y 'left' numero, heredamos la duración de 'right'
            elif isinstance(right, tuple):
                left = (res, right[1])
            else:
                left = res
                
        return left

    def visitAddExpr(self, ctx: AlgoritmiaParser.AddExprContext):
        left = self.visit(ctx.multExpr(0))
        
        for i in range(1, len(ctx.multExpr())):
            op = ctx.getChild(2 * i - 1).getText()
            right = self.visit(ctx.multExpr(i))
            
            # 1. Extraemos valores
            val_l = self._get_val(left)
            val_r = self._get_val(right)
            
            # 2. Operación
            res = 0
            if op == '+':
                res = val_l + val_r
            elif op == '-':
                res = val_l - val_r
                
            # 3. Reconstrucción (Mantener duración)
            if isinstance(left, tuple):
                left = (res, left[1]) # Mantiene duración original
            elif isinstance(right, tuple):
                left = (res, right[1])
            else:
                left = res
                
        return left

    def visitRelExpr(self, ctx: AlgoritmiaParser.RelExprContext):
        left = self.visit(ctx.addExpr(0))
        
        for i in range(1, len(ctx.addExpr())):
            op = ctx.getChild(2 * i - 1).getText()
            right = self.visit(ctx.addExpr(i))
            
            # Usamos el helper para comparar solo los valores numéricos/pitches
            val_l = self._get_val(left)
            val_r = self._get_val(right)
            
            result_bool = 0
            
            if op == '=':
                result_bool = 1 if val_l == val_r else 0
            elif op == '/=':
                result_bool = 1 if val_l != val_r else 0
            elif op == '<':
                result_bool = 1 if val_l < val_r else 0
            elif op == '>':
                result_bool = 1 if val_l > val_r else 0
            elif op == '<=':
                result_bool = 1 if val_l <= val_r else 0
            elif op == '>=':
                result_bool = 1 if val_l >= val_r else 0
            
            # El resultado de una comparación siempre es un entero (1 o 0), nunca una nota
            left = result_bool
            
        return left

    def visitTerm(self, ctx: AlgoritmiaParser.TermContext):
        if ctx.ID(): return self.resolve_var(ctx.ID().getText())
        if ctx.INT(): return int(ctx.INT().getText())
        
        # --- NUEVA LÓGICA PARA NOTAS ---
        if ctx.NOTE(): 
            text = ctx.NOTE().getText()
            duration_val = 4  # Default: Negra (q)
            
            if ':' in text:
                parts = text.split(':')
                note_part = parts[0]
                dur_char = parts[1]
                duration_val = DURATION_MAP.get(dur_char, 4)
                pitch_val = NOTE_MAP.get(note_part, 0)
            else:
                pitch_val = NOTE_MAP.get(text, 0)
            
            # Devolvemos una TUPLA para no perder la info: (pitch, duracion)
            return (pitch_val, duration_val)
        # -------------------------------

        if ctx.listLiteral(): return self.visit(ctx.listLiteral())
        if ctx.STRING(): return ctx.STRING().getText()[1:-1]
        if ctx.expression(): return self.visit(ctx.expression())
        if ctx.lengthExpr(): return self.visit(ctx.lengthExpr())
        if ctx.listAccessExpr(): return self.visit(ctx.listAccessExpr())
        return 0

    def visitListLiteral(self, ctx: AlgoritmiaParser.ListLiteralContext):
        elements = []
        for expr in ctx.expression():
            elements.append(self.visit(expr))
        return elements

    def generate_music_files(self):
        if not self.score:
            print("No se tocaron notas.")
            return

        # --- 1. DEFINICIÓN DE VARIABLES (Esto es lo que faltaba) ---
        base_path = os.path.abspath(self.output_base_name)
        file_dir = os.path.dirname(base_path)
        ly_file = os.path.join(file_dir, f"{self.output_base_name}.ly")
        wav_file = os.path.join(file_dir, f"{self.output_base_name}.wav")

        # --- 2. ESCRITURA DEL ARCHIVO LILYPOND ---
        with open(ly_file, 'w', encoding='utf-8') as f:
            f.write(self.create_lilypond_string())

        # --- 3. LÓGICA MULTIPLATAFORMA ---
        import platform
        sistema = platform.system() # Detecta 'Windows' o 'Linux'

        if sistema == 'Windows':
            # Rutas para TU computadora (Windows)
            # Asegúrate de que esta ruta sea la correcta en tu PC
            lilypond_cmd = [r"C:\Users\jande\Downloads\lilypond-2.24.4-mingw-x86_64\lilypond-2.24.4\bin\lilypond.exe"]
            timidity_cmd = ['timidity'] 
            # Ruta al SoundFont en Windows
            sf2_path = r"C:\Timidity\FluidR3_GM.sf2"
            extra_timidity_args = ['-x', f'soundfont "{sf2_path}"']
        else:
            # Rutas para DOCKER / LINUX (Estándar)
            # En Linux/Docker usamos los comandos globales directos
            lilypond_cmd = ['lilypond'] 
            timidity_cmd = ['timidity']
            # En Docker el soundfont se configura automáticamente o por defecto
            extra_timidity_args = [] 

        try:
            print(f"Generando partitura en {sistema}...")
            # Ejecutar LilyPond
            cmd_lily = lilypond_cmd + ['-o', base_path, ly_file]
            subprocess.run(cmd_lily, check=True, capture_output=True)
            
            # --- DETECCIÓN DEL MIDI (.mid o .midi) ---
            posible_midi_1 = os.path.join(file_dir, f"{self.output_base_name}.midi")
            posible_midi_2 = os.path.join(file_dir, f"{self.output_base_name}.mid")
            
            midi_real = None
            if os.path.exists(posible_midi_1):
                midi_real = posible_midi_1
            elif os.path.exists(posible_midi_2):
                midi_real = posible_midi_2
            
            if not midi_real:
                print("Error: LilyPond no generó ningún archivo MIDI.")
                return

            print(f"Convirtiendo audio en {sistema}...")
            # Ejecutar Timidity
            cmd_timidity = timidity_cmd + [midi_real, '-Ow', '-o', wav_file] + extra_timidity_args
            
            subprocess.run(cmd_timidity, check=True, capture_output=True)
            
            print(f"¡Éxito! WAV generado.")

        except Exception as e:
            print(f"Error generando música: {e}")
    
    def convert_to_lilypond(self, pitch_val, duration_val):
        if pitch_val < 0 or pitch_val > 51: return f"r{duration_val}"
        note_name = None
        for name, val in NOTE_MAP.items():
            if val == pitch_val and name[-1].isdigit():
                note_name = name
                break
        if note_name is None: return f"r{duration_val}"

        letter = note_name[0].lower()
        octave = int(note_name[1:])
        octave_suffix = {0: ",,,", 1: ",,", 2: ",", 3: "", 4: "'", 5: "''", 6: "'''", 7: "''''", 8: "'''''"}
        return f"{letter}{octave_suffix.get(octave, '')}{duration_val}"

    def create_lilypond_string(self):
        notes_str_list = []
        for note in self.score:
            notes_str_list.append(self.convert_to_lilypond(note['pitch'], note['duration']))

        notes_str = " ".join(notes_str_list)

        # --- PLANTILLA LILYPOND ---
        return (
            '\\version "2.24.0"\n'
            '\\score {\n'
            '  \\new Staff {\n'
            '    \\clef treble\n'
            '    \\tempo 4 = 120\n'
            f'    {{ {notes_str} }}\n'
            '  }\n'
            '  \\layout { }\n'
            '  \\midi { }\n'
            '}\n'
        )
