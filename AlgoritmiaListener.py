# Generated from Algoritmia.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .AlgoritmiaParser import AlgoritmiaParser
else:
    from AlgoritmiaParser import AlgoritmiaParser

# This class defines a complete listener for a parse tree produced by AlgoritmiaParser.
class AlgoritmiaListener(ParseTreeListener):

    # Enter a parse tree produced by AlgoritmiaParser#program.
    def enterProgram(self, ctx:AlgoritmiaParser.ProgramContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#program.
    def exitProgram(self, ctx:AlgoritmiaParser.ProgramContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#procDecl.
    def enterProcDecl(self, ctx:AlgoritmiaParser.ProcDeclContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#procDecl.
    def exitProcDecl(self, ctx:AlgoritmiaParser.ProcDeclContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#statement.
    def enterStatement(self, ctx:AlgoritmiaParser.StatementContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#statement.
    def exitStatement(self, ctx:AlgoritmiaParser.StatementContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#ifStmt.
    def enterIfStmt(self, ctx:AlgoritmiaParser.IfStmtContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#ifStmt.
    def exitIfStmt(self, ctx:AlgoritmiaParser.IfStmtContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#whileStmt.
    def enterWhileStmt(self, ctx:AlgoritmiaParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#whileStmt.
    def exitWhileStmt(self, ctx:AlgoritmiaParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#assignStmt.
    def enterAssignStmt(self, ctx:AlgoritmiaParser.AssignStmtContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#assignStmt.
    def exitAssignStmt(self, ctx:AlgoritmiaParser.AssignStmtContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#readStmt.
    def enterReadStmt(self, ctx:AlgoritmiaParser.ReadStmtContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#readStmt.
    def exitReadStmt(self, ctx:AlgoritmiaParser.ReadStmtContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#writeStmt.
    def enterWriteStmt(self, ctx:AlgoritmiaParser.WriteStmtContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#writeStmt.
    def exitWriteStmt(self, ctx:AlgoritmiaParser.WriteStmtContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#playStmt.
    def enterPlayStmt(self, ctx:AlgoritmiaParser.PlayStmtContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#playStmt.
    def exitPlayStmt(self, ctx:AlgoritmiaParser.PlayStmtContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#procCallStmt.
    def enterProcCallStmt(self, ctx:AlgoritmiaParser.ProcCallStmtContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#procCallStmt.
    def exitProcCallStmt(self, ctx:AlgoritmiaParser.ProcCallStmtContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#listAppendStmt.
    def enterListAppendStmt(self, ctx:AlgoritmiaParser.ListAppendStmtContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#listAppendStmt.
    def exitListAppendStmt(self, ctx:AlgoritmiaParser.ListAppendStmtContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#listCutStmt.
    def enterListCutStmt(self, ctx:AlgoritmiaParser.ListCutStmtContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#listCutStmt.
    def exitListCutStmt(self, ctx:AlgoritmiaParser.ListCutStmtContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#expression.
    def enterExpression(self, ctx:AlgoritmiaParser.ExpressionContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#expression.
    def exitExpression(self, ctx:AlgoritmiaParser.ExpressionContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#relExpr.
    def enterRelExpr(self, ctx:AlgoritmiaParser.RelExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#relExpr.
    def exitRelExpr(self, ctx:AlgoritmiaParser.RelExprContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#addExpr.
    def enterAddExpr(self, ctx:AlgoritmiaParser.AddExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#addExpr.
    def exitAddExpr(self, ctx:AlgoritmiaParser.AddExprContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#multExpr.
    def enterMultExpr(self, ctx:AlgoritmiaParser.MultExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#multExpr.
    def exitMultExpr(self, ctx:AlgoritmiaParser.MultExprContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#term.
    def enterTerm(self, ctx:AlgoritmiaParser.TermContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#term.
    def exitTerm(self, ctx:AlgoritmiaParser.TermContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#listLiteral.
    def enterListLiteral(self, ctx:AlgoritmiaParser.ListLiteralContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#listLiteral.
    def exitListLiteral(self, ctx:AlgoritmiaParser.ListLiteralContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#listAccessExpr.
    def enterListAccessExpr(self, ctx:AlgoritmiaParser.ListAccessExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#listAccessExpr.
    def exitListAccessExpr(self, ctx:AlgoritmiaParser.ListAccessExprContext):
        pass


    # Enter a parse tree produced by AlgoritmiaParser#lengthExpr.
    def enterLengthExpr(self, ctx:AlgoritmiaParser.LengthExprContext):
        pass

    # Exit a parse tree produced by AlgoritmiaParser#lengthExpr.
    def exitLengthExpr(self, ctx:AlgoritmiaParser.LengthExprContext):
        pass



del AlgoritmiaParser