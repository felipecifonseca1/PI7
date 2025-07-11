/*
 * Modulo: Programa Trajetoria
 * Armazena o programa da trajetoria a ser executada
 */

// max NC program size
#define MAX_PROGRAM_LINES 800

#include "trj_program.h"
#include <stdio.h>

// structure to store NC program
tpr_Data tpr_program[MAX_PROGRAM_LINES];

void tpr_storeProgram(char* texto) {
    int i = 0;
    int line = 0;
    float x, y, z;

    while (sscanf(&texto[i], "%f;%f;%f;", &x, &y, &z) == 3 && line < MAX_PROGRAM_LINES) {
        tpr_program[line].x = x;
        tpr_program[line].y = y;
        tpr_program[line].z = z;

        // avança para a próxima linha
        while (texto[i] != '\0' && texto[i] != '\n') i++;
        if (texto[i] == '\n') i++;

        line++;
    }
}

tpr_Data tpr_getLine(int line) {
	return tpr_program[line];
} // tpr_getLine

void tpr_init() {
  int i;

  for (i=0; i<MAX_PROGRAM_LINES;i++) {
	  tpr_program[i].x = 0;
	  tpr_program[i].y = 0;
	  tpr_program[i].z = 0;
  }
} //tpr_init
