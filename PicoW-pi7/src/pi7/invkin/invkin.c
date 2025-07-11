
#include "invkin.h"

// ==================================================================================
// PARÂMETROS FÍSICOS EXTRAÍDOS DO SEU SCRIPT PYTHON
// Certifique-se de que estes valores correspondem exatamente aos da sua máquina.
// ==================================================================================

// Parâmetros geométricos do robô 
#define H_ROBOT                 240.0f
#define L_ROBOT                 240.0f
#define OFFSET_ROBOT            0.0f
#define R_CARRETEL_MOTOR        10.0f   // Raio do carretel em mm
#define PI_F 3.14159265358979323846f

// Coordenadas dos pontos de ancoragem (calculadas como no script)
#define ANCHOR_EX               (0.0f + OFFSET_ROBOT)
#define ANCHOR_EY               H_ROBOT
#define ANCHOR_DX               (L_ROBOT - OFFSET_ROBOT)
#define ANCHOR_DY               H_ROBOT
#define GC
#define TICKS_PER_REVOLUTION    1852.0f

void convert_gcode_to_motor_commands(
    const char* gcode_line,
    float*      theta_e,
    float*      theta_d,
    int32_t*    ticks_e,
    int32_t*    ticks_d
) {
    // 1) Parse "X;Y;Z;" — só dois floats no início
    float x_mm = 0.0f, y_mm = 0.0f;
    sscanf(gcode_line, "%f;%f;", &x_mm, &y_mm);

    // 2) Comprimento dos cabos
    float dx_e = ANCHOR_EX - x_mm, dy_e = ANCHOR_EY - y_mm;
    float dx_d = ANCHOR_DX - x_mm, dy_d = ANCHOR_DY - y_mm;
    float l_e = sqrtf(dx_e*dx_e + dy_e*dy_e);
    float l_d = sqrtf(dx_d*dx_d + dy_d*dy_d);

    // 3) Posição inicial (na 1a chamada)
    static float initial_l_e = 0.0f, initial_l_d = 0.0f;
    static bool  first_run = true;
    if (first_run) {
        initial_l_e = l_e;
        initial_l_d = l_d;
        first_run   = false;
    }

    // 4) Comprimento → ângulo (graus), usando PI_F
    *theta_e = (l_e - initial_l_e) * 180.0f / (PI_F * R_CARRETEL_MOTOR);
    *theta_d = (l_d - initial_l_d) * 180.0f / (PI_F * R_CARRETEL_MOTOR);

    // 5) Ângulo → ticks
    *ticks_e = (int32_t)(*theta_e * (TICKS_PER_REVOLUTION / 360.0f));
    *ticks_d = (int32_t)(*theta_d * (TICKS_PER_REVOLUTION / 360.0f));
}
