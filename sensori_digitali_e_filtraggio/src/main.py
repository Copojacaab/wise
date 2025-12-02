# file che gestisce il flusso

import time
from collections import deque
from dsp_filter import MovingAverageFilter 
from sensor_interface import simulate_accell_raw_read, normalize_accell_data

# --- Parametri di acquisizione ---
SAMPLING_FREQUENCY = 100 #Hz
SAMPLING_PERIOD = 1 / SAMPLING_FREQUENCY #10ms
MOVING_AVG_WINDOW_SIZE = 10 

# --- Inizializzazione temporale ---
start_time = time.time()
last_sample_time = start_time
sample_counter = 0

accell_filter = MovingAverageFilter(window_size=MOVING_AVG_WINDOW_SIZE) 

raw_history = deque(maxlen=200)       # Buffer per la visualizzazione
filtered_history = deque(maxlen=200) # Buffer per la visualizzazione

# Intestazione della tabella di output
print(f"Inizio acquisizione a {SAMPLING_FREQUENCY} Hz.")
print("==================================================================")
print("Tempo (s) | Raw Count | Accel (g) NON Filtrata | Accel (g) Filtrata")
print("----------|-----------|------------------------|--------------------")

# loop principale
try: 
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if(current_time - last_sample_time >= SAMPLING_PERIOD):
            last_sample_time = current_time
            sample_counter += 1

            # lettura e normalizzazione
            raw_data = simulate_accell_raw_read(elapsed_time)
            accell_g_unfiltered = normalize_accell_data(raw_data)

            # filtraggio tramite modulo filtro
            accell_g_filtered = accell_filter.filter(accell_g_unfiltered)

            # output
            print(f"{elapsed_time:.3f}   | {raw_data: 9d} | {accell_g_unfiltered: 21.6f} | {accell_g_filtered: 17.6f}")

            # salvataggio dati per eventuale plot
            raw_history.append(accell_g_unfiltered)
            filtered_history.append(accell_g_filtered)
        
        # controllo del flusso
        time.sleep(0.001)

except KeyboardInterrupt:
    print("\n Simulazione interrotta")
