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

# ======== FUNZIONE DI ANALISI FFT =================== (dall'array allo spettro)
def analyze_fft(detrendend_signal, fs, N):
    """
    Esegue l'analisi FFT sul segnale  calcola lo spettro di potenza

    Args:
        detrended_signal (np.array): segnale ADC grezzo (senza l'offset DC)
        fs (float): frequenza di campionamento effettiva
        N (int): numero di campioni nel segnale
    
    Returns: 
        tuple(frequenze, spettro_di_potenza_normalizzato)
    """

    # -- 1. Windowing
    # la finestra (Hanning in questo caso) riduce i leakage 
    # causati dal troncamento del segnale a una durata fissa (N=50)
    window = scipy.signal.windows.hanning(N)
    # moltiplichiamo il segnale per la funzione finestra, gli estremi dell'arr
    # vengono pesati verso 0
    windowed_signal = detendrend_signal * window

    # 2. Calcolo della trasformata di Fourier (FFT)
    # applico la FFT al segnale finestrato. l'output e' un arr di N numeri complessi
    fft_output = np.fft.fft(windowed_signal)

    # 3. Mapping delle frequenze
    # calcola  a quale frequenza corrisponde ogni indice dell'arr fft_output
    # d e' il periodo di campionamento
    frequencies = np.fft.fftfreq(N, d=1.0/fs)

    # 4. calcolo dello spettro di potenza e normalizzazione
    # np.abs() => calcoliamo l'ampiezza del numero complesso
    # 2/n => moltiplichiamo per 2/N in modo da normalizzare l'ampiezza in modo che
    # l'altezza del picco corrisponda con l'altezza effettiva della sinusoide
    power_spectrum = np.abs(fft_output) * 2/N

    # 5. Filtro per la meta' positiva (freq di Nyquist)
    N_half = N // 2

    # ritorna solamente le frequenze positive, dalla prima frequenza > 0Hz (indice 1)
    # fino alla frequenza di Nyquist (Fs/2)
    # l'indice 0 (DC component) e la parte negativa dello spettro vengono omessi
    return frequencies[1:N_half], power_spectrum[1:N_half]

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

            else: # se il buffer non e' ancora pieno
                print(f"[{elapsed_time: .3f} s] Buffer non ancora pieno. Dati presenti: {len(data_buffer)}")

except KeyboardInterrupt:
    print("Interruzione utente")