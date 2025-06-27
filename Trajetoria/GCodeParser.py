# Generated from GCode.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,13,75,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,1,0,4,0,24,8,0,11,0,12,0,25,
        1,0,1,0,1,0,1,1,3,1,32,8,1,1,1,1,1,5,1,36,8,1,10,1,12,1,39,9,1,1,
        1,1,1,1,2,3,2,44,8,2,1,2,1,2,1,2,1,3,1,3,1,4,1,4,1,4,3,4,54,8,4,
        1,5,1,5,1,5,1,6,1,6,1,6,1,7,1,7,1,7,1,8,1,8,1,8,1,9,3,9,69,8,9,1,
        9,1,9,1,10,1,10,1,10,0,0,11,0,2,4,6,8,10,12,14,16,18,20,0,3,1,0,
        1,2,1,0,8,9,1,0,10,11,70,0,23,1,0,0,0,2,31,1,0,0,0,4,43,1,0,0,0,
        6,48,1,0,0,0,8,53,1,0,0,0,10,55,1,0,0,0,12,58,1,0,0,0,14,61,1,0,
        0,0,16,64,1,0,0,0,18,68,1,0,0,0,20,72,1,0,0,0,22,24,3,2,1,0,23,22,
        1,0,0,0,24,25,1,0,0,0,25,23,1,0,0,0,25,26,1,0,0,0,26,27,1,0,0,0,
        27,28,3,4,2,0,28,29,5,0,0,1,29,1,1,0,0,0,30,32,3,16,8,0,31,30,1,
        0,0,0,31,32,1,0,0,0,32,33,1,0,0,0,33,37,3,6,3,0,34,36,3,8,4,0,35,
        34,1,0,0,0,36,39,1,0,0,0,37,35,1,0,0,0,37,38,1,0,0,0,38,40,1,0,0,
        0,39,37,1,0,0,0,40,41,5,12,0,0,41,3,1,0,0,0,42,44,3,16,8,0,43,42,
        1,0,0,0,43,44,1,0,0,0,44,45,1,0,0,0,45,46,3,20,10,0,46,47,5,12,0,
        0,47,5,1,0,0,0,48,49,7,0,0,0,49,7,1,0,0,0,50,54,3,10,5,0,51,54,3,
        12,6,0,52,54,3,14,7,0,53,50,1,0,0,0,53,51,1,0,0,0,53,52,1,0,0,0,
        54,9,1,0,0,0,55,56,5,5,0,0,56,57,3,18,9,0,57,11,1,0,0,0,58,59,5,
        6,0,0,59,60,3,18,9,0,60,13,1,0,0,0,61,62,5,7,0,0,62,63,3,18,9,0,
        63,15,1,0,0,0,64,65,5,4,0,0,65,66,5,11,0,0,66,17,1,0,0,0,67,69,7,
        1,0,0,68,67,1,0,0,0,68,69,1,0,0,0,69,70,1,0,0,0,70,71,7,2,0,0,71,
        19,1,0,0,0,72,73,5,3,0,0,73,21,1,0,0,0,6,25,31,37,43,53,68
    ]

class GCodeParser ( Parser ):

    grammarFileName = "GCode.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "'M30'", "'N'", 
                     "'X'", "'Y'", "'F'", "'+'", "'-'" ]

    symbolicNames = [ "<INVALID>", "G00", "G01", "M30", "N", "X", "Y", "F", 
                      "PLUS", "MINUS", "FLOAT", "INT", "EOL", "WS" ]

    RULE_prog = 0
    RULE_linha = 1
    RULE_fimPrograma = 2
    RULE_gcode = 3
    RULE_parametro = 4
    RULE_x_coord = 5
    RULE_y_coord = 6
    RULE_fcode = 7
    RULE_numeroLinha = 8
    RULE_valor = 9
    RULE_comandoFim = 10

    ruleNames =  [ "prog", "linha", "fimPrograma", "gcode", "parametro", 
                   "x_coord", "y_coord", "fcode", "numeroLinha", "valor", 
                   "comandoFim" ]

    EOF = Token.EOF
    G00=1
    G01=2
    M30=3
    N=4
    X=5
    Y=6
    F=7
    PLUS=8
    MINUS=9
    FLOAT=10
    INT=11
    EOL=12
    WS=13

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def fimPrograma(self):
            return self.getTypedRuleContext(GCodeParser.FimProgramaContext,0)


        def EOF(self):
            return self.getToken(GCodeParser.EOF, 0)

        def linha(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GCodeParser.LinhaContext)
            else:
                return self.getTypedRuleContext(GCodeParser.LinhaContext,i)


        def getRuleIndex(self):
            return GCodeParser.RULE_prog

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProg" ):
                listener.enterProg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProg" ):
                listener.exitProg(self)




    def prog(self):

        localctx = GCodeParser.ProgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_prog)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 22
                    self.linha()

                else:
                    raise NoViableAltException(self)
                self.state = 25 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

            self.state = 27
            self.fimPrograma()
            self.state = 28
            self.match(GCodeParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LinhaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def gcode(self):
            return self.getTypedRuleContext(GCodeParser.GcodeContext,0)


        def EOL(self):
            return self.getToken(GCodeParser.EOL, 0)

        def numeroLinha(self):
            return self.getTypedRuleContext(GCodeParser.NumeroLinhaContext,0)


        def parametro(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GCodeParser.ParametroContext)
            else:
                return self.getTypedRuleContext(GCodeParser.ParametroContext,i)


        def getRuleIndex(self):
            return GCodeParser.RULE_linha

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLinha" ):
                listener.enterLinha(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLinha" ):
                listener.exitLinha(self)




    def linha(self):

        localctx = GCodeParser.LinhaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_linha)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 30
                self.numeroLinha()


            self.state = 33
            self.gcode()
            self.state = 37
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 224) != 0):
                self.state = 34
                self.parametro()
                self.state = 39
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 40
            self.match(GCodeParser.EOL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FimProgramaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def comandoFim(self):
            return self.getTypedRuleContext(GCodeParser.ComandoFimContext,0)


        def EOL(self):
            return self.getToken(GCodeParser.EOL, 0)

        def numeroLinha(self):
            return self.getTypedRuleContext(GCodeParser.NumeroLinhaContext,0)


        def getRuleIndex(self):
            return GCodeParser.RULE_fimPrograma

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFimPrograma" ):
                listener.enterFimPrograma(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFimPrograma" ):
                listener.exitFimPrograma(self)




    def fimPrograma(self):

        localctx = GCodeParser.FimProgramaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_fimPrograma)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 42
                self.numeroLinha()


            self.state = 45
            self.comandoFim()
            self.state = 46
            self.match(GCodeParser.EOL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GcodeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def G00(self):
            return self.getToken(GCodeParser.G00, 0)

        def G01(self):
            return self.getToken(GCodeParser.G01, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_gcode

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGcode" ):
                listener.enterGcode(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGcode" ):
                listener.exitGcode(self)




    def gcode(self):

        localctx = GCodeParser.GcodeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_gcode)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 48
            _la = self._input.LA(1)
            if not(_la==1 or _la==2):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParametroContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def x_coord(self):
            return self.getTypedRuleContext(GCodeParser.X_coordContext,0)


        def y_coord(self):
            return self.getTypedRuleContext(GCodeParser.Y_coordContext,0)


        def fcode(self):
            return self.getTypedRuleContext(GCodeParser.FcodeContext,0)


        def getRuleIndex(self):
            return GCodeParser.RULE_parametro

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParametro" ):
                listener.enterParametro(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParametro" ):
                listener.exitParametro(self)




    def parametro(self):

        localctx = GCodeParser.ParametroContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_parametro)
        try:
            self.state = 53
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 50
                self.x_coord()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 51
                self.y_coord()
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 3)
                self.state = 52
                self.fcode()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class X_coordContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def X(self):
            return self.getToken(GCodeParser.X, 0)

        def valor(self):
            return self.getTypedRuleContext(GCodeParser.ValorContext,0)


        def getRuleIndex(self):
            return GCodeParser.RULE_x_coord

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterX_coord" ):
                listener.enterX_coord(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitX_coord" ):
                listener.exitX_coord(self)




    def x_coord(self):

        localctx = GCodeParser.X_coordContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_x_coord)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
            self.match(GCodeParser.X)
            self.state = 56
            self.valor()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Y_coordContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Y(self):
            return self.getToken(GCodeParser.Y, 0)

        def valor(self):
            return self.getTypedRuleContext(GCodeParser.ValorContext,0)


        def getRuleIndex(self):
            return GCodeParser.RULE_y_coord

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterY_coord" ):
                listener.enterY_coord(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitY_coord" ):
                listener.exitY_coord(self)




    def y_coord(self):

        localctx = GCodeParser.Y_coordContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_y_coord)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self.match(GCodeParser.Y)
            self.state = 59
            self.valor()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FcodeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def F(self):
            return self.getToken(GCodeParser.F, 0)

        def valor(self):
            return self.getTypedRuleContext(GCodeParser.ValorContext,0)


        def getRuleIndex(self):
            return GCodeParser.RULE_fcode

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFcode" ):
                listener.enterFcode(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFcode" ):
                listener.exitFcode(self)




    def fcode(self):

        localctx = GCodeParser.FcodeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_fcode)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self.match(GCodeParser.F)
            self.state = 62
            self.valor()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumeroLinhaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def N(self):
            return self.getToken(GCodeParser.N, 0)

        def INT(self):
            return self.getToken(GCodeParser.INT, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_numeroLinha

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumeroLinha" ):
                listener.enterNumeroLinha(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumeroLinha" ):
                listener.exitNumeroLinha(self)




    def numeroLinha(self):

        localctx = GCodeParser.NumeroLinhaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_numeroLinha)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self.match(GCodeParser.N)
            self.state = 65
            self.match(GCodeParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(GCodeParser.INT, 0)

        def FLOAT(self):
            return self.getToken(GCodeParser.FLOAT, 0)

        def PLUS(self):
            return self.getToken(GCodeParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(GCodeParser.MINUS, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_valor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValor" ):
                listener.enterValor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValor" ):
                listener.exitValor(self)




    def valor(self):

        localctx = GCodeParser.ValorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_valor)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 68
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8 or _la==9:
                self.state = 67
                _la = self._input.LA(1)
                if not(_la==8 or _la==9):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 70
            _la = self._input.LA(1)
            if not(_la==10 or _la==11):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComandoFimContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def M30(self):
            return self.getToken(GCodeParser.M30, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_comandoFim

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComandoFim" ):
                listener.enterComandoFim(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComandoFim" ):
                listener.exitComandoFim(self)




    def comandoFim(self):

        localctx = GCodeParser.ComandoFimContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_comandoFim)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self.match(GCodeParser.M30)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





