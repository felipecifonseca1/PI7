#ifndef __invkin_h

#define __invkin_h
#include <math.h> // Necessário para M_PI
#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

void convert_gcode_to_motor_commands(const char* gcode_line, float* theta_e, float* theta_d, int32_t* ticks_e, int32_t* ticks_d);

#endif
