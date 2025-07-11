#include "FreeRTOS.h" // POSSÍVEL ERRO: "No such file or directory" - Verifique as configurações do seu ambiente de build (CMakeLists.txt)
#include "projdefs.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"

// Incluções da Raspberry PICO W
#include <stdbool.h>
#include <stdio.h>
//#include <type.h> // Comentado, pois geralmente não é um cabeçalho padrão
#include "boards/pico_w.h"
#include "pico/error.h"
#include "pico/stdio.h"
#include "pico/stdio_usb.h" // Necessário para stdio_usb_init()
#include "pico/stdlib.h"    // Necessário para stdio_getchar_timeout_us()
#include "pico/multicore.h"

// Drivers para UART e LED
#include "drivers/ledonboard/leds.h"
#include "drivers/uart/uart.h"

// Arquivos de cabeçalho para PI7 (assumindo que estes são os seus cabeçalhos)
#include "pi7/comm_pic/comm_pic.h" // Certifique-se de que pic_Data está definida aqui
#include "pi7/comm_pc/modbus.h"
#include "pi7/command_interpreter/command_interpreter.h"
#include "pi7/trj_control/trj_control.h"
#include "pi7/trj_program/trj_program.h"
#include "pi7/trj_state/trj_state.h"
#include "pi7/invkin/invkin.h" // Para a função convert_gcode_to_motor_commands

typedef struct {
    uint8_t portNum;
    pic_Data data;
} pic_Message;


// DEFINES do PI7
#define CONTROL_Q_SIZE 1 // Tamanhos das filas
#define PIC_Q_SIZE 2
#define DEV_Q_SIZE 20
#define UART_BAUD 115200
#define MAX_GCODE_LINE_LENGTH 1000 // Tamanho máximo de uma linha de G-code

/**
 * Constantes de tempo para atrasos do FreeRTOS
 * CORREÇÃO: Removidas as definições duplicadas. Se estas constantes
 * forem definidas em algum cabeçalho do FreeRTOS, elas não devem
 * ser definidas novamente aqui. O erro anterior indicava redefinição.
 * Se o erro persistir, significa que estão em outro .h e devem ser removidas daqui.
 */
const portTickType DELAY_1SEC = 1000 / portTICK_RATE_MS;
const portTickType DELAY_500MS = 500 / portTICK_RATE_MS;
const portTickType DELAY_200MS = 200 / portTICK_RATE_MS;
const portTickType DELAY_1MS   = 1  / portTICK_RATE_MS;

//void __error__(char *pcFilename, unsigned long ulLine) {
//}

/**
 * Filas de comunicação para transferência de dados entre componentes
 */
QueueHandle_t qControlCommands;
QueueHandle_t qCommPIC;
QueueHandle_t qCommDev; // para testes
QueueHandle_t qGCodeLines; // Nova fila para linhas de G-code recebidas

#define USERTASK_STACK_SIZE 4096 // Tamanho da pilha para as tarefas do usuário

void taskController(void *pvParameters) {
    while(1) {
        // Esta tarefa pode ser usada para lidar com comandos Modbus ou outros comandos de PC,
        // mas não diretamente com o fluxo de G-code que vem da Raspberry Pi (Linux).
        com_executeCommunication(); // Internamente, ela chama o Controlador para processar eventos
        vTaskDelay(DELAY_1MS);
    } // Loop da tarefa
} // taskController

/**
 * taskNCProcessing: processa as linhas de G-code recebidas de qGCodeLines,
 * calcula os setpoints do motor usando cinemática inversa e os envia para qCommPIC.
 */
// -----------------------------------------------------
// taskNCProcessing: processa G-code e envia setpoints
// -----------------------------------------------------
void taskNCProcessing(void *pvParameters) {
    static portTickType lastWakeTime = 0;
    char gcode_line[MAX_GCODE_LINE_LENGTH];
    float theta_e, theta_d;
    int32_t ticks_e, ticks_d;
    pic_Data setpoints_to_pic;        // estrutura original
    pic_Message msg;                  // nova struct (porta + pic_Data)

    lastWakeTime = xTaskGetTickCount();
    while (1) {
        // 1) Recebe G-code
        if (xQueueReceive(qGCodeLines, gcode_line, pdMS_TO_TICKS(100)) == pdPASS) {
            convert_gcode_to_motor_commands(
                gcode_line, &theta_e, &theta_d,
                &ticks_e, &ticks_d
            );

            // Prepara e envia para o PIC 0 (motor esquerdo)
            msg.portNum = 0;
            msg.data.setPoint1 = (float)ticks_e;
            // msg.data.setPoint1 = 100;
            msg.data.setPoint2 = 0.0f;
            msg.data.setPoint3 = 0.0f;
            xQueueSend(qCommPIC, &msg, portMAX_DELAY);

            // Prepara e envia para o PIC 1 (motor direito)
            msg.portNum = 1;
            msg.data.setPoint1 = (float)ticks_d;
            // msg.data.setPoint1 = 100;
            xQueueSend(qCommPIC, &msg, portMAX_DELAY);
        }

        // 2) Processa comandos Modbus / trajetória, se houver
        tcl_Data data;
        data.command = NO_CMD;
        xQueueReceive(qControlCommands, &data, 0);
        if (data.command != NO_CMD) {
            tcl_processCommand(data);
        }
        tcl_generateSetpoint();

        // 3) Aguarda próximo ciclo
        vTaskDelayUntil(&lastWakeTime, DELAY_200MS);
    }
}

/**
 * taskCommPIC: recebe setpoints para enviar aos PICs da fila qCommPIC
 * e os envia seguindo o protocolo PIC
 */

void taskCommPIC(void *pvParameters) {
    pic_Message msg;
    while (1) {
        if (xQueueReceive(qCommPIC, &msg, pdMS_TO_TICKS(250)) == pdPASS) {
            pic_sendToPIC(msg.portNum, msg.data);
        }
    }
}
/**
 * taskReceiveGCode: Lê caracteres da serial USB, os armazena em uma linha de G-code,
 * e envia a linha completa para a fila qGCodeLines.
 */
void taskReceiveGCode(void *pvParameters) {
    char gcode_buffer[MAX_GCODE_LINE_LENGTH];
    int buffer_idx = 0;
    while (1) {
        // Lê um caractere da serial USB com um timeout de 0 (não bloqueante)
        // Usando stdio_getchar_timeout_us em vez de stdio_usb_getc_timeout_us
        int c = stdio_getchar_timeout_us(0); // 0 timeout significa não bloqueante
        if (c != PICO_ERROR_TIMEOUT && c != PICO_ERROR_GENERIC) {
            char received_char = (char)c;

            if (received_char == '\n' || received_char == '\r') {
                if (buffer_idx > 0) {
                    gcode_buffer[buffer_idx] = '\0'; // Termina a string com nulo
                    // Envia a linha de G-code completa para a fila
                    if (xQueueSend(qGCodeLines, gcode_buffer, portMAX_DELAY) != pdPASS) {
                        printf("Falha ao enviar linha de G-code para a fila.\n");
                    }
                    buffer_idx = 0; // Reseta o índice do buffer
                }
            } else if (buffer_idx < MAX_GCODE_LINE_LENGTH - 1) {
                gcode_buffer[buffer_idx++] = received_char;
            } else {
                // Estouro de buffer, limpa o buffer e imprime erro
                printf("Linha de G-code muito longa, limpando o buffer.\n");
                buffer_idx = 0;
            }
        }
        vTaskDelay(DELAY_1MS); // Pequeno atraso para evitar busy-waiting
    }
}


void taskReceiveFromPIC(void *pvParameters) {
    char   c;
    char   ack_buffer[16];
    size_t ack_idx = 0;

    for (;;) {
        c = pic_receiveCharFromPIC(0);  // ou porta 1, conforme necessário
        if (c != 0) {
            // armazena no buffer até encontrar o EOT_CHAR
            ack_buffer[ack_idx++] = c;

            // compara com o caractere EOT, e também protege overflow
            if (c == ';' || ack_idx >= (sizeof(ack_buffer) - 1)) {
                ack_buffer[ack_idx] = '\0';
                printf("[ACK] %s\n", ack_buffer);
                ack_idx = 0;
            }
        }
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

void taskBlinkLed(void *lpParameters) {
    char ch = NO_CHAR;
    while(1) {
        led_invert();
        vTaskDelay(DELAY_1SEC);
    } // Loop da tarefa
} //taskBlinkLed

static void setupHardware(void) {
    led_init();
    stdio_usb_init();
    UARTInit(0, UART_BAUD); // UART0
    UARTInit(1, UART_BAUD); // UART1
    printf("Configuração de hardware concluída.\n");
} // setupHardware

static void initComponents(void) {
    // Comunicação entre tarefas
    qControlCommands = xQueueCreate(CONTROL_Q_SIZE, sizeof(tpr_Data));
    qCommPIC = xQueueCreate(PIC_Q_SIZE, sizeof(pic_Data));
    qCommDev = xQueueCreate(DEV_Q_SIZE, sizeof(char));
    qGCodeLines = xQueueCreate(5, MAX_GCODE_LINE_LENGTH); // Cria a nova fila para G-code

    // Inicializa componentes
    com_init(); // Comunicação PC
    pic_init(); // Comunicação PIC
    ctl_init(); // Interpretador de comandos
    tcl_init(); // Controle de trajetória
    tst_init(); // Estado da trajetória
    tpr_init(); // Programa de trajetória
} // initComponents

/**
 * Ponto de entrada do programa
 */
int main(void) {
    TaskHandle_t handleLed;

    printf("Iniciando o Controlador de G-code para Motor da Pico W.\n");

    // Inicializa o hardware
    setupHardware();

    // Inicializa os componentes
    initComponents();

    /*
     * Inicia as tarefas definidas neste arquivo/específicas para esta demonstração.
     */
    xTaskCreate( taskBlinkLed, "BlinkLed", USERTASK_STACK_SIZE, NULL, 1, &handleLed);
    xTaskCreate( taskController, "Controller", USERTASK_STACK_SIZE, NULL, 2, NULL );
    xTaskCreate( taskNCProcessing, "NCProcessing", USERTASK_STACK_SIZE, NULL, 5, NULL );
    xTaskCreate( taskReceiveFromPIC, "RecvPIC", USERTASK_STACK_SIZE, NULL, 4, NULL);
    xTaskCreate( taskCommPIC, "CommPIC", USERTASK_STACK_SIZE, NULL, 3, NULL );
    xTaskCreate( taskReceiveGCode, "ReceiveGCode", USERTASK_STACK_SIZE, NULL, 6, NULL); // Nova tarefa



    vTaskCoreAffinitySet(handleLed, (1 << 0)); // executa BlinkLed num único core

    vTaskStartScheduler();

    return 1;
} // main
