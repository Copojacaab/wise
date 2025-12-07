import numpy as np
import time
from collections import deque
import matplotlib.pyplot as plt
import scipy.signal # per il windowing

from acquisizione_dati_e_buffer_micro.project1_wireless import (
    simulate_senso_packet,
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

# ======= MAIN LOOP =============
