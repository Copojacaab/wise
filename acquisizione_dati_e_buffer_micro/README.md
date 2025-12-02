# Acquisizione Dati wireless e Buffering Efficiente

OBBIETTIVO: simulazione di un microcontrollore gateway per sisstemi di monitoraggio energetico

Simulo in ambiente python l'architettura software di un microcontrollore con il ruolo di gateway che 
gestisce la ricezione di dati da un sensore wireless, l'immagazzinamento in un buffer e la trasmissione
periodica per analisi.

## Architettura e Concetti chiave

1. Simulazione del SENSORE Wireless (acquisizione e pacchettizzazione dati)

    - Funzione: `simulate_sensor_packet(t)` 
    - Concetto: si simula l'ADC(Analogic to Digital Converter) che digitalizza un sengnale AC
    - Dettagli:
        - Segnale: viene generata una sinusoide a 50 Hz con l'aggiunta di rumore bianco (tramite numpy)
            per emulare le misurazioni di tensione
        - Conversione ADC: il segnale viene traslato (aggiunta di un offset di 2048) e troncato a un intero per 
            simulare la lettura ADC unipolare a 12 bit
        - Packaging: il dato grezzo viene incapsulato in un pacchetto insieme all'id del sensore e al suo timestamp
            (tracciabilita struttura wireless dei sensori)

2. Gestion dati con Ring Buffer

    - Struttura dati: `collections.deque` con lunghezza massima di 50 pacchetti
    - Concetto: tramite il buffer circolare siamo sicuri che il microcontrollore non esaurisca mai la memoria
        mantiene sempre gli ultimi N=50 pacchetti ricevuti

3. Timing e Priorita:
    
    - `RECEIVE_PERIOD`: il periodo di ricezione del pacchetto da parte del micro
        priorita alta(interrupt) e frequenza veloce
    - `OUTPUT_PERIOD`: il periodo della trasmissione UARD dell'intero buffer al PC
        priorita bassa (main loop) e frequenza veloce
    
