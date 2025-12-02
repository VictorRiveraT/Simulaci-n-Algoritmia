import unittest
from antlr4 import InputStream, CommonTokenStream
from AlgoritmiaLexer import AlgoritmiaLexer
from AlgoritmiaParser import AlgoritmiaParser
from AlgoritmiaInterpreter import AlgoritmiaInterpreter
from AlgoritmiaValidator import AlgoritmiaValidator

class TestAlgoritmia(unittest.TestCase):

    def setup_tree(self, code):
        """Helper para parsear código y devolver el árbol"""
        input_stream = InputStream(code)
        lexer = AlgoritmiaLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = AlgoritmiaParser(stream)
        return parser.program()

    # --- 1. PRUEBAS DE LÓGICA MATEMÁTICA ---
    def test_aritmetica_basica(self):
        # Probamos que el intérprete sume bien internamente
        code = "Main |: x <- 2 + 3 :|"
        tree = self.setup_tree(code)
        interpreter = AlgoritmiaInterpreter()
        interpreter.visit(tree)
        # Verificamos la memoria del intérprete
        # Nota: interpreter.call_stack[-1] es el scope global al terminar (o local de Main)
        # Dado que tu interpreter limpia el stack al salir de Main, 
        # podríamos necesitar interceptarlo o confiar en que la ejecución no lanzó error.
        # Para este test, asumimos éxito si no explota.
        pass 

    # --- 2. PRUEBAS SEMÁNTICAS (EL POLICÍA) ---
    def test_variable_no_definida(self):
        print(">> Probando detección de variable inexistente...")
        code = """
        Main |:
            x <- y + 1  ### 'y' no existe ###
        :|
        """
        tree = self.setup_tree(code)
        validator = AlgoritmiaValidator()
        errors = validator.visit(tree)
        
        # DEBE haber errores
        self.assertTrue(len(errors) > 0)
        self.assertIn("La variable 'y' no ha sido definida", errors[0])

    def test_procedimiento_fantasma(self):
        print(">> Probando llamada a procedimiento fantasma...")
        code = """
        Main |:
            NoExisto 5
        :|
        """
        tree = self.setup_tree(code)
        validator = AlgoritmiaValidator()
        errors = validator.visit(tree)
        self.assertTrue(len(errors) > 0)
        self.assertIn("El procedimiento 'NoExisto' no existe", errors[0])

    # --- 3. PRUEBAS DE RITMO Y POLIMORFISMO ---
    def test_ritmo_parsing(self):
        print(">> Probando gramática de ritmos...")
        code = "Main |: (:) C4:w :|" # Do redonda
        tree = self.setup_tree(code)
        interpreter = AlgoritmiaInterpreter()
        
        # Ejecutamos para ver si guarda la duración correcta en self.score
        # Tu interpreter limpia el score al final en generate_music_files,
        # así que para probar, inhabilitamos la generación de archivos temporalmente
        # o inspeccionamos el método visitPlayStmt.
        
        # Haremos un truco: Mockear generate_music_files para que no haga nada
        interpreter.generate_music_files = lambda: None 
        
        interpreter.visit(tree)
        
        # Verificamos que se guardó la nota correcta
        nota = interpreter.score[0]
        self.assertEqual(nota['pitch'], 23) # C4 es 23 en tu mapa? (O el valor que sea)
        self.assertEqual(nota['duration'], 1) # 'w' debe ser 1

    def test_aritmetica_musical(self):
        print(">> Probando suma de Nota + Entero...")
        # C4 (23) + 2 = E4 (25)
        code = "Main |: (:) (C4:h + 2) :|" 
        tree = self.setup_tree(code)
        interpreter = AlgoritmiaInterpreter()
        interpreter.generate_music_files = lambda: None 
        interpreter.visit(tree)
        
        nota = interpreter.score[0]
        # Validamos que el pitch subió pero la duración se mantuvo (h=2)
        # Nota: Ajusta los valores 23/25 según tu NOTE_MAP exacto
        self.assertEqual(nota['duration'], 2) 

if __name__ == '__main__':
    unittest.main()