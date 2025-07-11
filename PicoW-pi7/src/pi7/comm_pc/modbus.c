/**
 * Modulo: Comunicacao MODBUS (simplificada)
 * Usa a Serial0 para comunicar-se
 */

/*
 * FreeRTOS includes
 */
#include "FreeRTOS.h"
#include "portmacro.h"
#include "queue.h"
#include "projdefs.h"

// std includes
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>

// PICO W include
//#include "hardware/uart.h"
#include "pico/stdio.h"

#define byte uint8_t

// Drivers for UART, LED and Console(debug)
// #include <cr_section_macros.h>
// #include <NXP/crp.h>
// #include "LPC17xx.h"
// #include "type.h"
// #include "drivers/uart/uart.h"
// #include "drivers/console/basic_io.h"
// #include "drivers/ledonboard/leds.h"

// Includes for PI7
#include "modbus.h"
#include "../command_interpreter/command_interpreter.h"

// CommModes: Dev_mode para debug; escreve na console
//            Real_mode para execucao real escreve nas UARTs
#define DEVELOPMENT_MODE 0
#define REAL_MODE 1

// *** Configuracao da serial (_mode = REAL_MODE)
#define BAUD 115200 // 9600
#define MAX_RX_SIZE 1000

// *** endereco deste node
#define MY_ADDRESS 0x01

// Function Codes
#define READ_REGISTER 0x03
#define WRITE_REGISTER 0x06
#define WRITE_FILE 0x15

// Defines de uso geral
#define MB_NO_CHAR 0xff

// Estados do canal de recepcao
#define HUNTING_FOR_START_OF_MESSAGE 0
#define HUNTING_FOR_END_OF_MESSAGE 1
#define IDLE 3
#define MESSAGE_READY 4

int _state;
int _mode;
byte rxBuffer[MAX_RX_SIZE];
int idxRxBuffer;
byte txBuffer[1024];
int idxTxBuffer;
// extern xQueueHandle qCommDev;


/* Funções com lógica original mantida (com_init, sendTxBufferToSerialUSB, etc.)... */
void com_init() {
  _state = HUNTING_FOR_START_OF_MESSAGE;
  _mode = DEVELOPMENT_MODE;
}
void sendTxBufferToSerialUSB(void) {
  printf("%s\r", txBuffer); 
}

byte decode(byte high, byte low) {
  byte x, y;
  if (low < 'A') {
    x = (low & 0x0f);
  } else {
    x = (low & 0x0f) + 0x09;
  }
  if ( high < 'A') {
    y = (high & 0x0f);
  } else {
    y = (high & 0x0f) + 0x09;
  }
  return ( x | ( y << 4) );
}

byte encodeLow(byte value) {
  byte x = value & 0x0f;
  if ( x < 10) { return (0x30 + x); } else { return (0x41 + (x-10)); }
}

byte encodeHigh(byte value) {
  byte x = ((value & 0xf0) >> 4);
  if ( x < 10) { return (0x30 + x); } else { return (0x41 + (x-10)); }
}

byte calculateLRC(byte* frame, int start, int end) {
  byte accum = 0;
  for (int i = start; i < end; i++) {
    accum += frame[i];
  }
  accum = (byte) (0xFF - accum);
  accum += 1;
  return accum;
}

int checkLRC() {
    // No modo de desenvolvimento, pulamos a verificação para facilitar testes.
    if (_mode == DEVELOPMENT_MODE) {
        return true;
    }

    byte receivedLRC = decode(rxBuffer[idxRxBuffer - 4], rxBuffer[idxRxBuffer - 3]);
    
    byte decoded_message_for_lrc[MAX_RX_SIZE / 2];
    int decoded_len = 0;
    for (int i = 1; i < idxRxBuffer - 4; i += 2) {
        decoded_message_for_lrc[decoded_len++] = decode(rxBuffer[i], rxBuffer[i+1]);
    }

    byte calculatedLRC = calculateLRC(decoded_message_for_lrc, 0, decoded_len);
    
    // printf("LRC Recebido: 0x%02X, LRC Calculado: 0x%02X\n", receivedLRC, calculatedLRC);
    
    return (receivedLRC == calculatedLRC);
}

void sendExceptionResponse(byte functionCode, byte exceptionCode) {
    byte pdu_to_send[3];
    pdu_to_send[0] = MY_ADDRESS;
    pdu_to_send[1] = functionCode | 0x80;
    pdu_to_send[2] = exceptionCode;
    byte lrc = calculateLRC(pdu_to_send, 0, 3);
    sprintf((char*)txBuffer, ":%02X%02X%02X%02X\r\n", pdu_to_send[0], pdu_to_send[1], pdu_to_send[2], lrc);
    sendTxBufferToSerialUSB();
}

void processReadRegister() {
    int registerToRead = decode(rxBuffer[7], rxBuffer[8]);
    int registerValue = ctl_ReadRegister(registerToRead);

    if (registerValue == CTL_ERR) {
        sendExceptionResponse(READ_REGISTER, 0x02); return;
    }

    byte pdu_response[5];
    pdu_response[0] = MY_ADDRESS;
    pdu_response[1] = READ_REGISTER;
    pdu_response[2] = 2; // Byte Count: 1 registrador de 16 bits = 2 bytes
    pdu_response[3] = (registerValue >> 8) & 0xFF; // Valor High
    pdu_response[4] = registerValue & 0xFF;        // Valor Low
    byte lrc = calculateLRC(pdu_response, 0, 5);

    // Formata a string de resposta ASCII final
    sprintf((char*)txBuffer, ":%02X%02X%02X%04X%02X\r\n", 
            pdu_response[0], pdu_response[1], pdu_response[2], registerValue, lrc);

    sendTxBufferToSerialUSB();
}

void processWriteRegister() {
    int registerToWrite = decode(rxBuffer[7], rxBuffer[8]);
    int value = decode(rxBuffer[9], rxBuffer[10]);

    if (ctl_WriteRegister(registerToWrite, value) == CTL_ERR) {
        sendExceptionResponse(WRITE_REGISTER, 0x04); return;
    }
    
    for (int i = 0; i < idxRxBuffer; i++) {
        txBuffer[i] = rxBuffer[i];
    }
    txBuffer[idxRxBuffer] = '\0';
    sendTxBufferToSerialUSB();
}

void processWriteFile() {

    int ref_type = decode(rxBuffer[5], rxBuffer[6]);
    if (ref_type != 0x06) { sendExceptionResponse(WRITE_FILE, 0x03); return; }
    int record_len_words = (decode(rxBuffer[15], rxBuffer[16]) << 8) | decode(rxBuffer[17], rxBuffer[18]);
    int record_len_bytes = record_len_words * 2;
    if (record_len_bytes < 0 || record_len_bytes > 512) { sendExceptionResponse(WRITE_FILE, 0x03); return; }
    byte program_data[record_len_bytes + 1];
    int i;
    for (i = 0; i < record_len_bytes; i++) { program_data[i] = decode(rxBuffer[19 + i*2], rxBuffer[20 + i*2]); }
    program_data[i] = '\0';
    if (ctl_WriteProgram(program_data) == CTL_ERR) { sendExceptionResponse(WRITE_FILE, 0x04); return; }

    // Resposta de eco
    for (i = 0; i < idxRxBuffer; i++) { txBuffer[i] = rxBuffer[i]; }
    txBuffer[i] = '\0';
    sendTxBufferToSerialUSB();
}

int decodeFunctionCode() {
   return decode(rxBuffer[3], rxBuffer[4]);
} // extractFunctionCode

void processMessage() {
  int functionCode;
  if (checkLRC()) {
    functionCode = decodeFunctionCode();
    switch (functionCode) {
    case READ_REGISTER:
      processReadRegister();
      break;
    case WRITE_REGISTER:
      processWriteRegister();
      break;
    case WRITE_FILE:
      processWriteFile();
      break;
    } // switch on FunctionCode
  }
  _state = HUNTING_FOR_START_OF_MESSAGE;
} // processMessage

void receiveMessage() {
    int ch;
    ch = getchar_timeout_us(0);
    if (ch != PICO_ERROR_TIMEOUT) {
        if (_state == HUNTING_FOR_START_OF_MESSAGE) {
            if (ch == ':') {
                idxRxBuffer = 0;
                rxBuffer[idxRxBuffer++] = ch;
                _state = HUNTING_FOR_END_OF_MESSAGE;
            }
        } else if (_state == HUNTING_FOR_END_OF_MESSAGE) {
            if (idxRxBuffer < MAX_RX_SIZE) {
                rxBuffer[idxRxBuffer++] = ch;
                if (idxRxBuffer > 2 && rxBuffer[idxRxBuffer - 1] == 0x0A && rxBuffer[idxRxBuffer - 2] == 0x0D) {
                    rxBuffer[idxRxBuffer] = '\0'; // Adiciona terminador nulo
                    _state = MESSAGE_READY;
                }
            } else {
                _state = HUNTING_FOR_START_OF_MESSAGE;
            }
        }
    }
}


void com_executeCommunication() {
  receiveMessage();
  if ( _state == MESSAGE_READY ) {
    processMessage();
  }
}