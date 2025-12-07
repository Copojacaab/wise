# Analisi di frequenza su gateway simulato

L'obbiettivo e' trasformare una serie di campioni nel tempo (dominio temporale) in una rappresentazione delle frequenze contenute nel segnale (dominio della frequenza)

## 1. Preparazione dei dati per la FFT

La prima cosa che dobbiamo fare e' isolare la sequenza di campioni sulla quale vogliamo effettuare la trasformata. Nel nostro caso prendiamo il contenuto del 
`buffer_snapshot` (contiene gli ultimi 50 valori ricevuti dal sensore).
Visto che il segnale e' simulato per un ADC con un offset di 2048, e' buona pratica rimuovere l'offset prima di effettuare la FFT. In modo da poterci concentrare sulla componente AC del segnale.

## 2. Parametri chiave per l'analisi di frequenza

La correttezza della nostra FFT si basa su due parametri principali:

    1. $F_S$: la frequenza di campionamento con cui sono stati raccolti i dati nel buffer. Dalla quale possiamo ricavare la Frequenza di Nyquist ($F_{Nyquist} = 1/F_S$) che 
        rappresenta il massimo compomponente di frequenza che l'analisi puo' rilevare
    2. $N$: il numero di campioni nel mio array di dati

