import numpy as np
import time
from collections import deque
import matplotlib.pyplot as plt
import scipy.signal # per il windowing

from acquisizione_dati_e_buffer_micro.project1_wireless import (
    simulate_sensor_packet,
    RECEIVE_FREQUENCY,
    RECEIVE_PERIOD,
    BUFFER_SIZE,
    OUTPUT_PERIOD_S
)

# costante per il detranding (tolgo la componente DC)
ADC_OFFSET = 2048 # valore centrale ADC a 12 bit

# ======== FUNZIONE DI ANALISI FFT ===================
def analyze_fft(detrendend_signal, fs, N):
    pass

# ======= MAIN LOOP(simulazione del micro gateway) =============

# -- Inizializzazione --
data_buffer = deque(maxlen=BUFFER_SIZE)
start_time = time.time()
last_receive_time = start_time
last_output_time = start_time
packet_counter = 0

print(f"Inizio simulazione FFT... Fs: {RECEIVE_FREQUENCY} Hz, Buffer max: {BUFFER_SIZE}")

try:
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        # 1. RICEZIONE (Task ad altra frequenza)
        if(current_time - last_receive_time >= RECEIVE_PERIOD):
            last_receive_time = current_time

            # genera il pacchetto di dati simulato
            simulated_packet = simulate_sensor_packet(elapsed_time)
            data_buffer.append(simulate_sensor_packet)
            packet_counter += 1
        
        # 2. ANALISI FFT (Task a bassa frequenza)
        if(current_time - last_output_time >= OUTPUT_PERIOD_S):
            last_output_time = current_time

            # esegue l'analisi solamente se il buffer e' pieno
            if(len(data_buffer) == BUFFER_SIZE):
                #  A. estrazione e detrending
                raw_values = np.array(p['value'] for p in data_buffer)
                detendrend_signal = raw_values - ADC_OFFSET

                # B. esecuzione analisi FFT
                frequencies, power_spectrum = analyze_fft(
                    detendrend_signal, RECEIVE_FREQUENCY, BUFFER_SIZE
                )

                # C. interpretazione del risultato
                # trovo l'indice della frequenza con il picco massimo nello spettro di potenza
                max_index= np.argmax(power_spectrum)
                # calcola la frequenza corrispondente al picco
                dominant_freq = frequencies[max_index]

                print("\n" + "="*50)
                print(f"[{elapsed_time: .3f} s] Risultato analisi FFT")
                print(f"Frequenza dominante rilevata: {dominant_freq: .3f}")

            else # se il buffer non e' ancora pieno
                print(f"[{elapsed_time: .3f} s] Buffer non ancora pieno. Dati presenti: {len(data_buffer)}")

except KeyboardInterrupt:
    print("Interruzione utente")