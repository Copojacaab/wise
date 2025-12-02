# contiene la simulazione di I/O e la logica di normalizzazione (conversione fisica)

"""
 - simulate_accel_raw_read(t): simula l'azione del micro che legge i registri grezzi del sensore
    Se l'accellerometro giace su una superficie, l'asse Z misrua costantemente un g (dovuto all'accellerazione di gravita)
    Per simulare l'hw aggiungo una sinusoidale con bassa freq (2 Hz) e ampiezza minima (0.1 g). Rappresenta il segnale utile (vibrazione meccanica lenta)
    Aggiungo una componente casuale di disurbo (jitter), con 50 LSB spostiamo il valore grezzo di +- 50 unita (imprecisione istantanea)
"""
import numpy as np
import random

# parametri di conversione da datasheet MPU6050 (range +- 2g)
ACCEL_SCALE_FACTOR = 16384.0 #LSB per g
GRAVITY_VALUE_G = 9.81

def simulate_accell_raw_read(t):
    """
    Simula la lettura diretta da un registro a 16 bit dell'accelleratore
    """

    # 1. Segnale fondamentale (1g constante sull'asse Z)
    gravity_part = ACCEL_SCALE_FACTOR * 1.0

    # 2. segnale di interesse (vibrazione a bassa freq es. 2Hz)
    vibration_frequency = 2.0 #Hz
    vibration_amplitude = ACCEL_SCALE_FACTOR * 0.1 #0.1 g di vibrazione
    vibration_part = vibration_amplitude * np.sin(2 * np.pi * vibration_frequency)

    # 3. rumore causuale (jitter)
    noise = np.random.normal(0, 50)

    raw_value = int(gravity_part + vibration_part + noise) #dato grezzo, composto dalla forza grav costante, il segnale di interesse e il rumore

    return raw_value


# normalizzazione valore
def normalize_accell_data(raw_count):
    """
    converte il valore grezzo in accellerazione (g)
    """
    return raw_count / ACCEL_SCALE_FACTOR



