# contiene la logica di filtraggio low-pass con Moving Average

from collections import deque

class MovingAverageFilter:
    def __init__(self, window_size):
        self.window_size = window_size
        self.window = deque(maxlen=window_size)
        self.current_sum = 0.0
    
    def filter(self, new_sample):
        # logica filtro media mobile
        if (len(self.window) == self.window_size):
            oldest_sample = self.window.popleft() #tolgo il campione piu vecchio dalla coda
            self.current_sum -= oldest_sample
        
        self.window.append(new_sample)
        self.current_sum += new_sample

        return self.current_sum / len(self.window)
    