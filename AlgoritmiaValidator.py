from AlgoritmiaVisitor import AlgoritmiaVisitor
from AlgoritmiaParser import AlgoritmiaParser

class AlgoritmiaValidator(AlgoritmiaVisitor):
    def __init__(self):
        self.errors = []              # Lista de errores encontrados
        self.defined_procs = set()    # Conjunto de procedimientos declarados
        self.current_scope = set()    # Variables definidas en el procedimiento actual
        self.global_context = False   # Para saber si estamos escaneando o validando

    def add_error(self, message, ctx):
        # Intentamos obtener la línea del error
        line = ctx.start.line
        self.errors.append(f"Error Semántico en línea {line}: {message}")

    # --- 1. Primera Pasada: Recolectar Procedimientos ---
    def visitProgram(self, ctx: AlgoritmiaParser.ProgramContext):
        # Paso 1: Registrar todos los nombres de procedimientos
        for proc in ctx.procDecl():
            proc_name = proc.ID(0).getText()
            if proc_name in self.defined_procs:
                self.add_error(f"El procedimiento '{proc_name}' ya fue definido.", proc)
            else:
                self.defined_procs.add(proc_name)
        
        # Paso 2: Validar el cuerpo de cada uno
        for proc in ctx.procDecl():
            self.visit(proc)
            
        return self.errors

    # --- 2. Validación de Procedimientos ---
    def visitProcDecl(self, ctx: AlgoritmiaParser.ProcDeclContext):
        proc_name = ctx.ID(0).getText()
        
        # Reiniciar scope para este procedimiento (variables locales)
        self.current_scope = set()
        
        # Registrar parámetros como variables ya definidas
        # (Los parametros empiezan desde el índice 1 del array de IDs)
        for param in ctx.ID()[1:]:
            self.current_scope.add(param.getText())

        # Visitar el cuerpo
        for stmt in ctx.statement():
            self.visit(stmt)

    # --- 3. Validación de Uso de Variables ---
    def visitAssignStmt(self, ctx: AlgoritmiaParser.AssignStmtContext):
        var_name = ctx.ID().getText()
        # Primero validamos la expresión de la derecha (antes de asignar)
        self.visit(ctx.expression())
        # Luego registramos que la variable de la izquierda ya existe
        self.current_scope.add(var_name)

    def visitReadStmt(self, ctx: AlgoritmiaParser.ReadStmtContext):
        var_name = ctx.ID().getText()
        self.current_scope.add(var_name)

    def visitTerm(self, ctx: AlgoritmiaParser.TermContext):
        # Si usamos una variable (ID) dentro de una expresión...
        if ctx.ID():
            var_name = ctx.ID().getText()
            # ...verificamos que exista en el scope actual
            if var_name not in self.current_scope:
                self.add_error(f"La variable '{var_name}' no ha sido definida.", ctx)
        
        # Seguir explorando hacia abajo
        return self.visitChildren(ctx)

    # --- 4. Validación de Llamadas ---
    def visitProcCallStmt(self, ctx: AlgoritmiaParser.ProcCallStmtContext):
        proc_name = ctx.ID().getText()
        if proc_name not in self.defined_procs:
            self.add_error(f"El procedimiento '{proc_name}' no existe.", ctx)
        
        # Validar los argumentos
        for expr in ctx.expression():
            self.visit(expr)