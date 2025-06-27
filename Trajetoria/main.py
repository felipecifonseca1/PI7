import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import serial.tools.list_ports
from antlr4 import *

# Import Modbus client (RTU)
try:
    from pymodbus.client.sync import ModbusSerialClient
except ImportError:
    from pymodbus.client import ModbusSerialClient

# Mapeamento de registradores
REGISTER_MAP = {
    'POSICAO_X': 0,
    'POSICAO_Y': 1,
    'VELOCIDADE': 2,
    'COMANDO': 3,
    'STATUS': 4,
    'JOG_STEP': 5,
}
# Códigos de comando para G/M codes
GCODE_COMMANDS = {
    'G00': 1,
    'G01': 2,
    'M30': 30
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interface de Controle MODBUS - Robô Paralelo")
        self.geometry("1000x600")
        
        self.client = None
        self.connected = False
        self.gcode_filepath = ""
        self.processing_thread = None
        self.stop_processing = threading.Event()

        self._create_widgets()
        self.update_serial_ports()

    def _create_widgets(self):
        # Serial Connection Frame
        serial_frame = ttk.LabelFrame(self, text="Conexão Serial", padding=10)
        serial_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        serial_frame.columnconfigure(0, weight=1)

        self.ports_cbox = ttk.Combobox(serial_frame, state="readonly")
        self.ports_cbox.grid(row=0, column=0, sticky="ew")
        ttk.Button(serial_frame, text="Atualizar Portas", command=self.update_serial_ports).grid(row=0, column=1, padx=5)
        self.connect_button = ttk.Button(serial_frame, text="Conectar", command=self.toggle_connection)
        self.connect_button.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        # GCode Frame
        gcode_frame = ttk.LabelFrame(self, text="Controle G-Code", padding=10)
        gcode_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        gcode_frame.columnconfigure(0, weight=1)

        file_frame = ttk.Frame(gcode_frame)
        file_frame.grid(row=0, column=0, sticky="ew")
        self.gcode_entry = ttk.Entry(file_frame)
        self.gcode_entry.grid(row=0, column=0, sticky="ew")
        ttk.Button(file_frame, text="Selecionar Arquivo", command=self.open_gcode_file).grid(row=0, column=1, padx=5)

        btn_frame = ttk.Frame(gcode_frame)
        btn_frame.grid(row=1, column=0, pady=5)
        self.send_gcode_button = ttk.Button(btn_frame, text="Enviar GCode", command=self.start_gcode_processing)
        self.send_gcode_button.grid(row=0, column=0, padx=5)
        self.stop_gcode_button = ttk.Button(btn_frame, text="Parar", command=self.stop_gcode_file, state=tk.DISABLED)
        self.stop_gcode_button.grid(row=0, column=1, padx=5)

        # Jog Frame
        jog_frame = ttk.LabelFrame(self, text="Movimento Manual (JOG)", padding=10)
        jog_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        jog_frame.columnconfigure(1, weight=1)

        ttk.Label(jog_frame, text="Passo:").grid(row=0, column=0)
        self.jog_step = ttk.Entry(jog_frame, width=10)
        self.jog_step.insert(0, "1")
        self.jog_step.grid(row=0, column=1)
        ttk.Label(jog_frame, text="Feed:").grid(row=1, column=0)
        self.jog_feed = ttk.Entry(jog_frame, width=10)
        self.jog_feed.insert(0, "100")
        self.jog_feed.grid(row=1, column=1)

        for i, m in enumerate(["Y+", "Y-", "X-", "X+"]):
            ttk.Button(jog_frame, text=m, command=lambda m=m: self.manual_move(m)).grid(row=2, column=i, padx=3)

        # Log Frame
        log_frame = ttk.LabelFrame(self, text="Log de Eventos", padding=10)
        log_frame.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=5, pady=5)
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        self.log_text = scrolledtext.ScrolledText(log_frame, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky="nsew")

    def update_serial_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        if not ports:
            ports = ["Nenhuma"]
        self.ports_cbox['values'] = ports
        self.ports_cbox.current(0)

    def toggle_connection(self):
        if self.connected:
            self.client.close()
            self.connect_button.config(text="Conectar")
            self.log("Desconectado.")
            self.client = None
            self.connected = False
        else:
            port = self.ports_cbox.get()
            if not port or port.startswith("Nenhuma"):
                messagebox.showwarning("Seleção de Porta", "Nenhuma porta serial válida selecionada.")
                return
            try:
                client = ModbusSerialClient(
                    method='rtu', port=port, baudrate=115200,
                    parity='N', stopbits=1, bytesize=8, timeout=0.1
                )
                if client.connect():
                    self.client = client
                    self.connected = True
                    self.connect_button.config(text="Desconectar")
                    self.log(f"Conectado a {port} via MODBUS RTU.")
                else:
                    messagebox.showerror("Erro de Conexão", f"Não foi possível conectar à porta {port}.")
            except Exception as e:
                messagebox.showerror("Erro de Conexão", f"Ocorreu um erro: {e}")

    def open_gcode_file(self):
        path = filedialog.askopenfilename(
            title="Selecione G-Code", filetypes=[("G-Code", "*.gcode"), ("Todos", "*")]
        )
        if path:
            self.gcode_filepath = path
            self.gcode_entry.delete(0, tk.END)
            self.gcode_entry.insert(0, path)
            self.log(f"Arquivo G-Code selecionado: {path}")

    def start_gcode_processing(self):
        if self.processing_thread and self.processing_thread.is_alive():
            messagebox.showwarning("Envio em Andamento", "Um envio de G-Code já está em execução.")
            return
        if not self.gcode_filepath:
            messagebox.showwarning("Nenhum Arquivo", "Selecione um Arquivo G-Code.")
            return
        if not self.connected:
            messagebox.showwarning("Não Conectado", "Conecte-se via MODBUS.")
            return
        self.send_gcode_button.config(state=tk.DISABLED)
        self.stop_gcode_button.config(state=tk.NORMAL)
        self.stop_processing.clear()
        self.processing_thread = threading.Thread(
            target=self._process_gcode_in_thread, daemon=True
        )
        self.processing_thread.start()

    def stop_gcode_file(self):
        if self.processing_thread and self.processing_thread.is_alive():
            self.stop_processing.set()
            self.stop_gcode_button.config(state=tk.DISABLED)
            self.log("Parando envio de G-Code...")

    def _process_gcode_in_thread(self):
        """
        Processa o arquivo G-Code em background, enviando cada linha
        como um bloco único de registradores (X, Y, Feed e COMANDO).
        """
        # Variáveis para armazenar os últimos valores lidos
        last_x = 0
        last_y = 0
        last_feed = 0

        try:
            with open(self.gcode_filepath, 'r') as f:
                for line in f:
                    if self.stop_processing.is_set():
                        break

                    line = line.strip()
                    if not line or line.startswith(';'):
                        continue

                    parts = line.split()
                    # encontra o token Gxx ou Mxx
                    cmd_token = next((p for p in parts if p.startswith(('G', 'M'))), None)
                    if cmd_token in GCODE_COMMANDS:
                        # extrai X, Y e F, se presentes
                        x = last_x
                        y = last_y
                        feed = last_feed

                        for p in parts[1:]:
                            if p.startswith('X'):
                                try:
                                    x = int(float(p[1:]) * 10)
                                except ValueError:
                                    pass
                            elif p.startswith('Y'):
                                try:
                                    y = int(float(p[1:]) * 10)
                                except ValueError:
                                    pass
                            elif p.startswith('F'):
                                try:
                                    feed = int(float(p[1:]))
                                except ValueError:
                                    pass

                        # obtém o código numérico do comando
                        cmd = GCODE_COMMANDS[cmd_token]

                        # envia todos os quatro valores em um único bloco:
                        start_addr = 0
                        values = [x, y, feed, cmd]
                        self.client.write_registers(start_addr, values, unit=1)

                        # log para interface
                        self.log(f"Modbus Bloco → X:{x/10} Y:{y/10} F:{feed} CMD:{cmd}")

                        # atualiza últimos
                        last_x, last_y, last_feed = x, y, feed

                    # pequeno delay para não saturar a linha serial
                    time.sleep(0.05)

        finally:
            # reativa os botões na interface e sinaliza fim
            self.send_gcode_button.config(state=tk.NORMAL)
            self.stop_gcode_button.config(state=tk.DISABLED)
            self.log("Envio de G-Code concluído.")

    def send_modbus_command(self, address, value):
        try:
            self.log(f"MODBUS Write: Endereço={address}, Valor={value}")
            self.client.write_register(address, int(value), unit=1)
            return True
        except Exception as e:
            self.log(f"Erro no envio MODBUS: {e}")
            return False

    def manual_move(self, move_type):
        try:
            step = int(self.jog_step.get())
            feed = int(self.jog_feed.get())
        except ValueError:
            messagebox.showerror("Entrada Inválida", "O passo e a velocidade devem ser números inteiros.")
            return
        self.send_modbus_command(REGISTER_MAP['JOG_STEP'], step)
        self.send_modbus_command(REGISTER_MAP['VELOCIDADE'], feed)
        jog_codes = {"Y+": 10, "Y-": 11, "X-": 12, "X+": 13}
        if move_type in jog_codes:
            self.send_modbus_command(REGISTER_MAP['COMANDO'], jog_codes[move_type])

    def log(self, message):
        timestamp = time.strftime('%H:%M:%S')
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

if __name__ == '__main__':
    app = App()
    app.mainloop()
