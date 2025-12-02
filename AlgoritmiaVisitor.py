# Generated from Algoritmia.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .AlgoritmiaParser import AlgoritmiaParser
else:
    from AlgoritmiaParser import AlgoritmiaParser

# This class defines a complete generic visitor for a parse tree produced by AlgoritmiaParser.

class AlgoritmiaVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by AlgoritmiaParser#program.
    def visitProgram(self, ctx:AlgoritmiaParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#procDecl.
    def visitProcDecl(self, ctx:AlgoritmiaParser.ProcDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#statement.
    def visitStatement(self, ctx:AlgoritmiaParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#ifStmt.
    def visitIfStmt(self, ctx:AlgoritmiaParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#whileStmt.
    def visitWhileStmt(self, ctx:AlgoritmiaParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#assignStmt.
    def visitAssignStmt(self, ctx:AlgoritmiaParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#readStmt.
    def visitReadStmt(self, ctx:AlgoritmiaParser.ReadStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#writeStmt.
    def visitWriteStmt(self, ctx:AlgoritmiaParser.WriteStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#playStmt.
    def visitPlayStmt(self, ctx:AlgoritmiaParser.PlayStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#procCallStmt.
    def visitProcCallStmt(self, ctx:AlgoritmiaParser.ProcCallStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#listAppendStmt.
    def visitListAppendStmt(self, ctx:AlgoritmiaParser.ListAppendStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#listCutStmt.
    def visitListCutStmt(self, ctx:AlgoritmiaParser.ListCutStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#expression.
    def visitExpression(self, ctx:AlgoritmiaParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#relExpr.
    def visitRelExpr(self, ctx:AlgoritmiaParser.RelExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#addExpr.
    def visitAddExpr(self, ctx:AlgoritmiaParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#multExpr.
    def visitMultExpr(self, ctx:AlgoritmiaParser.MultExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#term.
    def visitTerm(self, ctx:AlgoritmiaParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#listLiteral.
    def visitListLiteral(self, ctx:AlgoritmiaParser.ListLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#listAccessExpr.
    def visitListAccessExpr(self, ctx:AlgoritmiaParser.ListAccessExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlgoritmiaParser#lengthExpr.
    def visitLengthExpr(self, ctx:AlgoritmiaParser.LengthExprContext):
        return self.visitChildren(ctx)



del AlgoritmiaParser