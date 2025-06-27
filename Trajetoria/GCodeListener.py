# Generated from GCode.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .GCodeParser import GCodeParser
else:
    from GCodeParser import GCodeParser

# This class defines a complete listener for a parse tree produced by GCodeParser.
class GCodeListener(ParseTreeListener):

    # Enter a parse tree produced by GCodeParser#prog.
    def enterProg(self, ctx:GCodeParser.ProgContext):
        pass

    # Exit a parse tree produced by GCodeParser#prog.
    def exitProg(self, ctx:GCodeParser.ProgContext):
        pass


    # Enter a parse tree produced by GCodeParser#linha.
    def enterLinha(self, ctx:GCodeParser.LinhaContext):
        pass

    # Exit a parse tree produced by GCodeParser#linha.
    def exitLinha(self, ctx:GCodeParser.LinhaContext):
        pass


    # Enter a parse tree produced by GCodeParser#fimPrograma.
    def enterFimPrograma(self, ctx:GCodeParser.FimProgramaContext):
        pass

    # Exit a parse tree produced by GCodeParser#fimPrograma.
    def exitFimPrograma(self, ctx:GCodeParser.FimProgramaContext):
        pass


    # Enter a parse tree produced by GCodeParser#gcode.
    def enterGcode(self, ctx:GCodeParser.GcodeContext):
        pass

    # Exit a parse tree produced by GCodeParser#gcode.
    def exitGcode(self, ctx:GCodeParser.GcodeContext):
        pass


    # Enter a parse tree produced by GCodeParser#parametro.
    def enterParametro(self, ctx:GCodeParser.ParametroContext):
        pass

    # Exit a parse tree produced by GCodeParser#parametro.
    def exitParametro(self, ctx:GCodeParser.ParametroContext):
        pass


    # Enter a parse tree produced by GCodeParser#x_coord.
    def enterX_coord(self, ctx:GCodeParser.X_coordContext):
        pass

    # Exit a parse tree produced by GCodeParser#x_coord.
    def exitX_coord(self, ctx:GCodeParser.X_coordContext):
        pass


    # Enter a parse tree produced by GCodeParser#y_coord.
    def enterY_coord(self, ctx:GCodeParser.Y_coordContext):
        pass

    # Exit a parse tree produced by GCodeParser#y_coord.
    def exitY_coord(self, ctx:GCodeParser.Y_coordContext):
        pass


    # Enter a parse tree produced by GCodeParser#fcode.
    def enterFcode(self, ctx:GCodeParser.FcodeContext):
        pass

    # Exit a parse tree produced by GCodeParser#fcode.
    def exitFcode(self, ctx:GCodeParser.FcodeContext):
        pass


    # Enter a parse tree produced by GCodeParser#numeroLinha.
    def enterNumeroLinha(self, ctx:GCodeParser.NumeroLinhaContext):
        pass

    # Exit a parse tree produced by GCodeParser#numeroLinha.
    def exitNumeroLinha(self, ctx:GCodeParser.NumeroLinhaContext):
        pass


    # Enter a parse tree produced by GCodeParser#valor.
    def enterValor(self, ctx:GCodeParser.ValorContext):
        pass

    # Exit a parse tree produced by GCodeParser#valor.
    def exitValor(self, ctx:GCodeParser.ValorContext):
        pass


    # Enter a parse tree produced by GCodeParser#comandoFim.
    def enterComandoFim(self, ctx:GCodeParser.ComandoFimContext):
        pass

    # Exit a parse tree produced by GCodeParser#comandoFim.
    def exitComandoFim(self, ctx:GCodeParser.ComandoFimContext):
        pass



del GCodeParser