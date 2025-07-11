/**
 * Modulo: Comunicacao MODBUS (simplificada)
 * Usa a Serial0 para comunicar-se
 * [jo:230927] usa UART0 e UART1 para comunicação
 */

/*
 * FreeRTOS includes
 */
#include "FreeRTOS.h"
#include "queue.h"
#include <stdbool.h>
#include <stdio.h>

// Drivers for UART, LED and Console(debug)
//#include <cr_section_macros.h>
//#include <NXP/crp.h>
//#include "LPC17xx.h"
//#include "type.h"
#include "drivers/uart/uart.h"
#include "hardware/uart.h"

// Header files for PI7
#include "comm_pic.h"

extern QueueHandle_t qCommPIC;


#define PIC_Q_SIZE 2
#define SOT_CHAR ':' // Start of transmission
#define EOT_CHAR ';' // End of transmission

void pic_init(void){
    // Cria fila para envio de dados para PIC, se ainda não criada
    if (qCommPIC == NULL) {
        qCommPIC = xQueueCreate(PIC_Q_SIZE, sizeof(pic_Data));
    }

    // Se houver inicialização de hardware UART exclusiva para PIC, colocar aqui
    // UARTInit(0, UART_BAUD); // já feito no main, geralmente não repetir aqui

    // Inicializar variáveis internas, flags ou buffers se houver
    // Por enquanto, nada mais necessário

}// pic_init

void pic_sendToPIC(uint8_t portNum, pic_Data data) {
    uart_inst_t *uart = (portNum == 0) ? uart0 : uart1;
    char address = '0' + portNum;

    int32_t ticks = (int32_t)data.setPoint1;

    char buffer[32];
    snprintf(buffer, sizeof(buffer), ":%cp%ld;", address, ticks);

    printf("[ENVIO PIC%c] %s\n", address, buffer);

    for (int i = 0; buffer[i] != '\0'; i++) {
        uart_putc(uart, buffer[i]);
        vTaskDelay(pdMS_TO_TICKS(20));
    }
}


extern uint8_t pic_receiveCharFromPIC(uint8_t portNum) {
  return UARTGetChar(portNum, false);
} // pic_receiveFromPIC
