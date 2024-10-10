import numpy as np
from threading import Lock


class Buffer:
    def __init__(
            self
        ):
        self.value_seq = list()
        self.values_counter = 0

        self.values_to_send = None

        self.period_counter = 0
        self.period = []
        self.values_mean = 0
        self.zero_passage_count = 0

        self.first_period = True
        self.last_period = None

        self.mutex = Lock()
    
    def put_read(self, value) -> None:
        with self.mutex:
            if len(self.value_seq) and \
                self.value_seq[-1] < self.values_mean and \
                value >= self.values_mean:
                self.zero_passage_count += 1
                self.period.append(self.period_counter)
                self.period_counter = 0

            self.value_seq.append(value)
            self.values_counter += 1
            self.period_counter += 1

            if self.first_period:
                self.values_mean = sum(self.value_seq) / self.values_counter
    
    def flush(self):
        with self.mutex:
            self.values_mean = sum(self.value_seq) / self.values_counter

            self.value_seq = list()
            self.values_counter = 0

            self.period_counter = 0
            self.period = []
            self.zero_passage_count = 0

            self.first_period = False
    
    def get_sequence(self):
        with self.mutex:
            if len(self.period) > 0:
                period = sum(self.period) / len(self.period)
            else:
                period = 0

            self.last_period = period

            return self.value_seq, period
        
    def can_send(self, limit: int = 0):
        with self.mutex:
            if limit == -1 and self.last_period is not None:
                limit = self.last_period
            
            if self.period_counter > limit and limit != 0:
                return True
            
            return self.zero_passage_count >= 2

if __name__ == "__main__":
    from datetime import datetime
