import time
import threading
import serial.tools.list_ports

from pymodbus.server.sync import ModbusSerialServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.transaction import ModbusRtuFramer

# Mapeamento de registradores
REGISTER_MAP = {
    'POSICAO_X': 0,
    'POSICAO_Y': 1,
    'VELOCIDADE': 2,
    'COMANDO': 3,
    'STATUS': 4,
    'JOG_STEP': 5,
}

# Dicionário de descrições de comandos
COMANDOS = {
    1: "Mover G00",
    2: "Mover G01",
    10: "Jog Y+",
    11: "Jog Y-",
    12: "Jog X-",
    13: "Jog X+",
    30: "Fim de Programa M30",
    99: "Parada de Emergência"
}

# Mapeamento de código numérico para token G/M correspondente
CODE_TO_TOKEN = {
    1: 'G00',
    2: 'G01',
    30: 'M30',
    10: 'JOG Y+',
    11: 'JOG Y-',
    12: 'JOG X-',
    13: 'JOG X+'
}

def updating_task(context, stop_event):
    """
    Loop que verifica continuamente o registrador COMANDO, lê os outros registradores e imprime a linha completa.
    """
    slave_id = 0  # contexto único
    while not stop_event.is_set():
        comando_atual = context[slave_id].getValues(3, REGISTER_MAP['COMANDO'], 1)[0]
        if comando_atual != 0:
             # Lê registradores
                x = context[slave_id].getValues(3, REGISTER_MAP['POSICAO_X'], 1)[0]
                y = context[slave_id].getValues(3, REGISTER_MAP['POSICAO_Y'], 1)[0]
                f = context[slave_id].getValues(3, REGISTER_MAP['VELOCIDADE'], 1)[0]
                step = context[slave_id].getValues(3, REGISTER_MAP['JOG_STEP'], 1)[0]

                token = CODE_TO_TOKEN.get(comando_atual, f'comando_atual{comando_atual}')

                # Aplica JOG se necessário
                if comando_atual == 10:  # JOG Y+
                    y += step*10
                elif comando_atual == 11:  # JOG Y-
                    y -= step*10
                elif comando_atual == 12:  # JOG X-
                    x -= step*10
                elif comando_atual == 13:  # JOG X+
                    x += step*10

                # Atualiza registradores se houve JOG
                if comando_atual in (10, 11, 12, 13):
                    context[slave_id].setValues(3, REGISTER_MAP['POSICAO_X'], [x])
                    context[slave_id].setValues(3, REGISTER_MAP['POSICAO_Y'], [y])

                # Imprime a linha
                print(f"{token} X{x / 10.0:.1f} Y{y / 10.0:.1f} F{f:.1f}")

                # Reset COMANDO
                context[slave_id].setValues(3, REGISTER_MAP['COMANDO'], [0])
        time.sleep(0.05)


def run_modbus_slave(port='COM5'):
    # Cria contexto de dados com 100 registradores de holding
    store = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [0] * 100))
    context = ModbusServerContext(slaves=store, single=True)

    # Identificação do dispositivo
    identity = ModbusDeviceIdentification()
    identity.VendorName = "Robo Paralelo Sim"
    identity.ProductName = "Servidor Escravo MODBUS"
    identity.Version = "1.0"

    print("--- Servidor Escravo MODBUS ---")

    # Verifica se a porta existe
    available = [p.device for p in serial.tools.list_ports.comports()]
    if port not in available:
        print(f"ERRO: Porta '{port}' não encontrada. Disponíveis: {available}")
        return
    print(f"Iniciando servidor na porta {port}...")

    # Cria servidor RTU com parâmetros alinhados ao cliente
    server = ModbusSerialServer(
        context,
        framer=ModbusRtuFramer,
        identity=identity,
        port=port,
        baudrate=115200,
        parity='N',
        stopbits=1,
        bytesize=8,
        timeout=0.1
    )

    # Thread de lógica de atualização
    stop_event = threading.Event()
    logic_thread = threading.Thread(
        target=updating_task,
        args=(context, stop_event),
        daemon=True
    )
    logic_thread.start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Encerrando servidor...")
        server.server_close()
        stop_event.set()
        logic_thread.join(timeout=1)
        print("Servidor encerrado.")

if __name__ == '__main__':
    run_modbus_slave(port='COM5')
