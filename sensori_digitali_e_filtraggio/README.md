# Progetto 2: sensori digitalizzati e filtraggio

Catena completa di un sensore digitale: dalla lettura del bus (I2C e SPI) all'ottenimento di un valore fisico pulito.

## Interfaccia con l'Accellerometro (I2C/SPI)

Sono i due protocolli che il microntrollore (MCU) usaper leggere i dati grezzi dall'accellerometro(MPU6050)

### I2C (Integer-Integrated Circuit)

    Il principio di funzionamento e' un bus seriale a due fili:
        1. SDA(Serial Data Line): utilizzato per trasferire i dati:
            - comandi: MCU --> MPU6050
            - letture: MPU6050 --> MCU
    
    RUOLI: 
        - Master (MCU): invia i comandi (es. "scrivi l'indirizzo di questo registro" oppure "leggi 8 bit di dati")
        - Slave (MPU6050): risponde alle richieste del Master. Ogni slave ha un suo indirizzo univoco a 7 bit
    
    FUNZIONAMENTO:
        Per leggere l'accellerazione l'MCU invia all'accelleromentro l'indirizzo del registro contenente l'asse X, attende l'ACK e poi legge il dato.

### SPI (Seril Peripheral Interface)

    In pratica e' un bus seriale sincrono full-duplex (trasmissione e ricezione non bloccanti)
    E' tipicamente piu veloce dell'I2C ed e' composto da 4 fili principali:
        1. MOSI (Master Out Slave In): dati dal master allo slave
        2. MISO (Master In Slave Out): indovina 
        3. SCK (Serial Clock): orologio, generato dal Master
        4. SS/CS (Slave Select/Chip Select): linea che il master usa per selezionare uno slave specifico

## Normalizzazione e Conversione in unita fisiche

Dal registro del sensore noi leggiamo il **raw-count**, cioe' solamente un numero intero 
che deve essere prima normalizzato per rappresentare un unita fisica come *g* o *$m/s^2$*.

### Dati grezzi

    I sensori come l'MPU6050 (16 bit) restituiscono un numero intero tra -32768 e +32767, questo
    e' un valore dipendente dalla sensibilita' impostata sul sensore (*full-scale range*)

### Sensibilita e Scale Factor
    
    - Sensibilita (full-scale range): i sensori come l'MPU6050 permettono di scegliere il 
        *range di accellerazione* ($\pm 2g, \pm 4g, \pm 8g, \pm 16g$)
    - Scale factor (LSB/g): ogni range corrisponde a un fattore di scalatura diverso definito nel datasheet 
        (es. 16384 LSB/g per il range $\pm 2g$) (LSB: Least Significant Bit)
    - Formula di Conversione:
        $$\text{Accelerazione (in } g) = \frac{\text{Raw Count}}{\text{Fattore di Scalatura (LSB/g)}}$$

        - Conversione finale: se ci serve avere la misura in $m\s^2$, moltiplichiamo per l'accellerazione
            gravitazionale

## Filtraggio Digitale (Media Mobile)

    Tutti i sensori generano del rumore. Il filtro digitale e' un algoritmo matematico utilizzato per 
    rimuovere le componenti indesiderate e lasciare il segnale utile.

### Rumore e segnale
    
    - Rumore: sono delle fluttuazioni rapide e casualidel segnale, principalmente causate da 
        disturbi o jitter del sensore
    - Segnale: la parte che ci interessa, cioe' la variaizonevariazione lenta e significativa 
        che vogliamo misurare 
    
### FIltro a Media Mobile (MA)

    E' un filtro FIR (*Finite Impulse Response*) computazionalmente economico.
    
    - Funzionamento: ad ogni nuovo campione il filtro calcola la media degli ultimi 
        N campioni e restisuisce quella come valore del nuovo campione.
    - Formula:
        $$\text{Filtered}_k = \frac{1}{N} \sum_{i=0}^{N-1} \text{Sample}_{k-i}$$
        N e' la dimensione della "finestra" del filtro
    
    E' un low-pass filter, di conseguenza attenua i picchi di frequenza (solitamente il rumore) e 
    lascia passare le basse frequenze. Maggiore e' N e piu' liscio sara il segnale, ma cresce anche 
    il costo computazionale.

    
