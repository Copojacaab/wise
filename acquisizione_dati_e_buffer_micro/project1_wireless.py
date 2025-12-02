import numpy as np
import time
from collections import deque
import matplotlib.pyplot as plt

def simulate_sensor_packet(t, sensor_id=1):
    """
    Simula la lettura e la pacchettizzazione di un sensore.
    Genera una sinusoide rumorosa(simula segnale elettrico del sensore ad esempio un trasformatore di corrente) e
    la formatta con timestamp e ID

    params: 
        t (float): tempo corrente in sec
        sensor_id (int): ID del sensore simulato

    return:
        dict: un pacchetto dati pronto da inserire nel buffer
    """
    # frequenza fondamentale del segnale misurato
    signal_frequency = 50.0 #50 Hz(tipico in wireless)

    # 1. Generazione del segnale(simulazione lettura ADC 12 bit)
    sinusoidal_part = 1000 * np.sin(2 * np.pi * signal_frequency * t);

    # 2. simulazione rumore
    noise = np.random.normal(0, 50)

    # 3. valore finale scalato per un ADC con range 0-4098 (traslo il segnale in modo che la sinuisoide sia centrata sul valore a meta del range dell'ADC unipolare)
    # ADC unipolare misurano solamente tensioni positive (0V a 3.3V)
    raw_value = int(sinusoidal_part + noise + 2048)

    # 4. creazione struttura dati
    packet = {
        'timestamp_s': t, #istante di acquisizio dati sensore
        'sensor_id': sensor_id, #id del sensore
        'value': raw_value #valore letto dal sens
    }

    return packet





# --- 1. Parametri di configurazione (Simulazione)

# parametri di acquisizione del sensore (frequenza ADC alta 1000 Hz)
SENSOR_SAMPLING_FREQUENCY = 1000 #f_s = 1 kHz       
SENSOR_SAMPLING_PERIOD = 1 / SENSOR_SAMPLING_FREQUENCY # T_s = 1ms

# parametri di ricezione wirelesse(frequenza a cui il micro riceve pacchetti dal sensore)
# ricezione di un pacchetto ogni 100 ms(10hz)
RECEIVE_FREQUENCY = 10
RECEIVE_PERIOD = 1 / RECEIVE_FREQUENCY #T_rx = 100 ms

# dimensione del buffer cirocolare sul micro
# memorizziamo 5 secondi di dati (5 * 10 pacchetti/secondo)
BUFFER_SIZE = 50

# periodo di output dal buffer del micro
OUTPUT_PERIOD_S = 2.0


# --- 2. Inizializzazione

# ring buffer centrale che memorizza i pacchetti che arrivano al micro
# ogni pacchetto dati e' un dict
data_buffer = deque(maxlen=BUFFER_SIZE)

# variabili per la simulazione del tempo
start_time = time.time()
last_receive_time = start_time
last_output_time = start_time
packet_counter = 0

print(f"Inizio simulazione... (Ricezione): {RECEIVE_FREQUENCY} Hz, Buffer max: {BUFFER_SIZE} pacchetti")


# --- 3. Loop principale (simulazione loop del micro)

try: 
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        # 1. RICEZIONE pacchetti (simulazione interrupt wireless e timer)
        # controllo se e' il momento di ricevere un nuovo pacchetto
        if(current_time - last_receive_time >=  RECEIVE_PERIOD):
            last_receive_time = current_time

            # genera pacchetto dati simulato
            simulated_packet = simulate_sensor_packet(elapsed_time)
            packet_counter += 1
            # inserisco il pacchetto nel buffer simulato
            data_buffer.append(simulated_packet)

            print(f"[{elapsed_time: .3f} s] Ricevuto pacchetto: {packet_counter}, Valore {simulated_packet['value']} ")

        # 2. OUTPUT periodico (simulazione trasmissione UART)
        # controllo se e' il momento di inviare il buffer al pc
        if(current_time - last_output_time >= OUTPUT_PERIOD_S):
            last_output_time = current_time

            # copio i dati dal buffer per l'invio
            buffer_snapshot = list(data_buffer)
            print("\n" + "="*50)
            print(f"[{elapsed_time: .3f} s] INVIO SERIALE (UART) - {len(buffer_snapshot)} pacchetti")
            print("="*50)

            # serializzazione e stampa (simulazione invio)
            print("ID | Timestamp(s) | Valore(ADC)")
            print("-- | ------------ | -----------")

            for i, packet in enumerate(buffer_snapshot):
                # formattazione stile CSV
                output_line = {
                    f"{packet['sensor_id']} | "
                    f"{packet['timestamp_s']:3f} |"
                    f"{packet['value']}"
                }
                print(output_line)

                # stampo solo gli ultimi 1-
                if(len(buffer_snapshot) > 20 and i==len(buffer_snapshot)-20):
                    print("... (altri pacchetti omessi per brevita)")
                    break

            print("="*50 + "\n")

            # al posto di timer interrupt 
            time.sleep(0.001)

except KeyboardInterrupt:
    print("\nSimulazione interrotta dall'utente.")
    print(f"Totale pacchetti processati: {packet_counter}")
