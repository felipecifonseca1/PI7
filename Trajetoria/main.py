import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import serial
from serial.tools.list_ports import comports

# Dicionários de registradores e comandos
REGISTER_MAP = {'COMANDO': 0}
COMMAND_CODES = {'START': 1, 'ABORT': 4, 'JOG_X_MAIS': 5, 'JOG_Y_MAIS': 6, 'JOG_X_MENOS': 7, 'JOG_Y_MENOS': 8}

# Funções auxiliares para construir os frames Modbus ASCII
def calculate_lrc(data_bytes):
    s = sum(data_bytes)
    return (s ^ 0xFF) + 1

def build_write_register_frame(slave_id, address, value):
    function_code = 6
    pdu = bytearray([function_code, (address >> 8) & 0xFF, address & 0xFF, (value >> 8) & 0xFF, value & 0xFF])
    adu_for_lrc = bytearray([slave_id])
    adu_for_lrc.extend(pdu)
    lrc = calculate_lrc(adu_for_lrc) & 0xFF
    hex_string_pdu = ''.join(f'{byte:02X}' for byte in pdu)
    final_frame = f":{slave_id:02X}{hex_string_pdu}{lrc:02X}\r\n"
    return final_frame.encode('ascii')

def build_write_file_frame(slave_id, file_num, record_num, record_data_bytes):
    function_code = 0x15
    ref_type = 0x06
    record_len_words = (len(record_data_bytes) + 1) // 2
    sub_request = bytearray([ref_type])
    sub_request.extend(file_num.to_bytes(2, 'big'))
    sub_request.extend(record_num.to_bytes(2, 'big'))
    sub_request.extend(record_len_words.to_bytes(2, 'big'))
    sub_request.extend(record_data_bytes)
    request_data_len = len(sub_request)
    pdu = bytearray([function_code, request_data_len])
    pdu.extend(sub_request)
    adu_for_lrc = bytearray([slave_id])
    adu_for_lrc.extend(pdu)
    lrc = calculate_lrc(adu_for_lrc) & 0xFF
    hex_string_pdu = ''.join(f'{byte:02X}' for byte in pdu)
    final_frame = f":{slave_id:02X}{hex_string_pdu}{lrc:02X}\r\n"
    return final_frame.encode('ascii')

class App(tk.Tk):
    # As funções __init__ e _create_widgets não mudam.
    def __init__(self):
        super().__init__()
        self.title("Interface de Controle Final - Handshake")
        self.geometry("1000x600")
        self.serial_port = None
        self.connected = False
        self.gcode_filepath = ""
        self.processing_thread = None
        self.stop_processing = threading.Event()
        self._create_widgets()
        self.update_serial_ports()

    def _create_widgets(self):
        # O código dos widgets é o mesmo da versão anterior. Omitido para brevidade.
        serial_frame = ttk.LabelFrame(self, text="Conexão Serial", padding=10); serial_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5); serial_frame.columnconfigure(0, weight=1); self.ports_cbox = ttk.Combobox(serial_frame, state="readonly"); self.ports_cbox.grid(row=0, column=0, sticky="ew"); ttk.Button(serial_frame, text="Atualizar Portas", command=self.update_serial_ports).grid(row=0, column=1, padx=5); self.connect_button = ttk.Button(serial_frame, text="Conectar", command=self.toggle_connection); self.connect_button.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")
        gcode_frame = ttk.LabelFrame(self, text="Controle G-Code", padding=10); gcode_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5); gcode_frame.columnconfigure(0, weight=1); file_frame = ttk.Frame(gcode_frame); file_frame.grid(row=0, column=0, sticky="ew", columnspan=2); self.gcode_entry = ttk.Entry(file_frame); self.gcode_entry.grid(row=0, column=0, sticky="ew"); ttk.Button(file_frame, text="Selecionar Arquivo", command=self.open_gcode_file).grid(row=0, column=1, padx=5)
        btn_frame = ttk.Frame(gcode_frame); btn_frame.grid(row=1, column=0, pady=5); self.send_gcode_button = ttk.Button(btn_frame, text="Enviar GCode", command=self.start_gcode_processing); self.send_gcode_button.grid(row=0, column=0, padx=5); self.stop_gcode_button = ttk.Button(btn_frame, text="Parar", command=self.stop_gcode_file, state=tk.DISABLED); self.stop_gcode_button.grid(row=0, column=1, padx=5)
        jog_frame = ttk.LabelFrame(self, text="Movimento Manual (JOG)", padding=10); jog_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5); jog_frame.columnconfigure(1, weight=1); ttk.Label(jog_frame, text="Passo (definido no Pico):").grid(row=0, column=0); self.jog_step = ttk.Entry(jog_frame, width=10, state='disabled'); self.jog_step.grid(row=0, column=1);
        for i, m in enumerate(["Y+", "Y-", "X-", "X+"]): ttk.Button(jog_frame, text=m, command=lambda m=m: self.manual_move(m)).grid(row=2, column=i, padx=3)
        log_frame = ttk.LabelFrame(self, text="Log de Eventos", padding=10); log_frame.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=5, pady=5); log_frame.rowconfigure(0, weight=1); log_frame.columnconfigure(0, weight=1); self.log_text = scrolledtext.ScrolledText(log_frame, state=tk.DISABLED); self.log_text.grid(row=0, column=0, sticky="nsew")

    def toggle_connection(self):
        if self.connected:
            self.serial_port.close(); self.connect_button.config(text="Conectar"); self.log("Desconectado.")
            self.serial_port = None; self.connected = False
        else:
            port = self.ports_cbox.get()
            if not port or port.startswith("Nenhuma"): return
            try:
                self.serial_port = serial.Serial(port=port, timeout=1, baudrate=115200) # Timeout de 1 segundo
                if self.serial_port.is_open:
                    self.connected = True; self.connect_button.config(text="Desconectar")
                    self.log(f"Conectado diretamente à porta {port}.")
                else: messagebox.showerror("Erro", f"Não foi possível abrir a porta {port}.")
            except Exception as e: messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def open_gcode_file(self):
        path = filedialog.askopenfilename(title="Selecione G-Code", filetypes=[("G-Code", "*.gcode"), ("Todos", "*")])
        if path:
            self.gcode_filepath = path; self.gcode_entry.config(state='normal'); self.gcode_entry.delete(0, tk.END)
            self.gcode_entry.insert(0, path); self.gcode_entry.config(state='disabled'); self.log(f"Arquivo G-Code selecionado: {path}")

    def start_gcode_processing(self):
        if self.processing_thread and self.processing_thread.is_alive(): messagebox.showwarning("Envio em Andamento", "Um envio de G-Code já está em execução."); return
        if not self.gcode_filepath: messagebox.showwarning("Nenhum Arquivo", "Selecione um Arquivo G-Code."); return
        if not self.connected: messagebox.showwarning("Não Conectado", "Conecte-se via MODBUS."); return
        self.send_gcode_button.config(state=tk.DISABLED); self.stop_gcode_button.config(state=tk.NORMAL); self.stop_processing.clear()
        self.processing_thread = threading.Thread(target=self._process_gcode_file_in_thread, daemon=True)
        self.processing_thread.start()

    def stop_gcode_file(self):
        if self.processing_thread and self.processing_thread.is_alive():
            self.stop_processing.set(); self.log("Sinal de parada enviado...")

    def _process_gcode_file_in_thread(self):
        try:
            self.log(f"Iniciando envio com handshake do arquivo: {self.gcode_filepath}")
            with open(self.gcode_filepath, 'r') as f:
                for line_num, line in enumerate(f):
                    if self.stop_processing.is_set():
                        self.log("Processo cancelado pelo usuário.")
                        break
                    
                    line = line.strip().upper()
                    if not line or line.startswith(';'): continue

                    # Formata a string para o padrão "X;Y;Z;"
                    parts = line.split()
                    x_val, y_val, z_val = 0.0, 0.0, 0.0
                    for part in parts:
                        if part.startswith('X'): x_val = float(part[1:])
                        elif part.startswith('Y'): y_val = float(part[1:])
                        elif part.startswith('Z'): z_val = float(part[1:])
                    
                    formatted_line = f"{x_val};{y_val};{z_val};"
                    gcode_bytes = formatted_line.encode('utf-8')

                    self.log(f"Enviando Linha {line_num + 1}: '{formatted_line}'")
                    
                    # Monta o frame WRITE_FILE
                    frame = build_write_file_frame(
                        slave_id=1, file_num=1, record_num=line_num,
                        record_data_bytes=gcode_bytes
                    )
                    
                    # Envia e ESPERA pela resposta de eco do Pico
                    self.serial_port.write(frame)
                    time.sleep(0.02) 
                    response = self.serial_port.readline() # Bloqueia até receber resposta ou dar timeout
                    
                    if not response:
                        self.log("ERRO: Pico não respondeu (timeout). Abortando.")
                        break # Sai do loop se o Pico não responder
                    
                    self.log(f"Pico confirmou recebimento.", to_console=False)

                else: # Executado se o loop terminar sem 'break'
                    self.log("Envio do arquivo G-Code concluído.")
                    self.log("Enviando comando START final...")
                    self.send_modbus_command(REGISTER_MAP['COMANDO'], COMMAND_CODES['START'])


        except Exception as e:
            self.log(f"Erro durante o envio do G-Code: {e}")
        finally:
            self.send_gcode_button.config(state=tk.NORMAL)
            self.stop_gcode_button.config(state=tk.DISABLED)

    def send_modbus_command(self, address, value):
        if not self.connected: messagebox.showwarning("Não Conectado", "Conecte-se."); return False
        try:
            frame_to_send = build_write_register_frame(1, address, value)
            self.serial_port.write(frame_to_send)
            self.serial_port.readline() # Espera o eco do comando simples também
            return True
        except Exception as e: self.log(f"Erro no envio do comando: {e}"); return False

    def manual_move(self, move_type):
        jog_map = { "X+": 5, "X-": 7, "Y+": 6, "Y-": 8 }
        if move_type in jog_map:
            self.log(f"Enviando comando JOG {move_type}"); self.send_modbus_command(REGISTER_MAP['COMANDO'], jog_map[move_type])

    def update_serial_ports(self):
        ports = [p.device for p in comports()]; self.ports_cbox['values'] = ports if ports else ["Nenhuma"]; self.ports_cbox.current(0)
    
    def log(self, message, to_console=True):
        if to_console:
            timestamp = time.strftime('%H:%M:%S'); self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n"); self.log_text.see(tk.END); self.log_text.config(state=tk.DISABLED)

if __name__ == '__main__':
    app = App()
    app.mainloop()