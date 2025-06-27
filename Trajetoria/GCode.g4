// Define que esta é uma gramática ANTLR 4 chamada 'GCode'
// O nome do ficheiro deve ser GCode.g4
grammar GCode;

/*
 * =============================================================================
 * REGRAS DO PARSER (ANALISADOR SINTÁTICO) - Versão Corrigida
 * =============================================================================
 */

// A regra inicial: um programa é uma ou mais linhas, seguidas pelo fim.
prog: linha+ fimPrograma EOF;

// Uma linha pode ter um número de linha, DEVE ter um comando G,
// e pode ter ZERO OU MAIS parâmetros em qualquer ordem.
linha: numeroLinha? gcode parametro* EOL;

// A regra de fim de programa.
fimPrograma: numeroLinha? comandoFim EOL;

// Define os códigos G aceites.
gcode: G00 | G01;

// Define o que é um PARÂMETRO. Pode ser uma coordenada X, Y ou um comando F.
parametro: x_coord | y_coord | fcode;

// Define a estrutura de cada parâmetro.
x_coord: X valor;
y_coord: Y valor;
fcode: F valor; // O comando F agora é tratado como um parâmetro.

// Define a estrutura de um número de linha.
numeroLinha: N INT;

// Define um valor numérico (inteiro ou float, com sinal opcional).
valor: (PLUS | MINUS)? (INT | FLOAT);

// Define o comando de fim de programa.
comandoFim: M30;


/*
 * =============================================================================
 * REGRAS DO LEXER (ANALISADOR LÉXICO) - Sem alterações
 * =============================================================================
 */

// Códigos G
G00: 'G00' | 'G0';
G01: 'G01' | 'G1';

// Códigos M
M30: 'M30';

// Letras dos eixos e parâmetros
N: 'N';
X: 'X';
Y: 'Y';
F: 'F';

// Símbolos
PLUS: '+';
MINUS: '-';

// Tipos de dados numéricos
FLOAT: [0-9]+ '.' [0-9]* | '.' [0-9]+;
INT: [0-9]+;

// Fim de linha
EOL: ('\r'? '\n') | '\r';

// Espaços em branco a serem ignorados
WS: [ \t]+ -> skip;
