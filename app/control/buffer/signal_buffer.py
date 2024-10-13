from threading import Lock


class Buffer:
    def __init__(
            self
        ):
        self.__value_seq = list()
        self.__values_counter = 0

        self.__values_to_send = None

        self.__period_counter = 0
        self.__period = []
        self.__values_mean = 0
        self.__zero_passage_count = 0

        self.__first_period = True
        self.__last_period = None

        self.__mutex = Lock()
    
    def put_read(self, value) -> None:
        with self.__mutex:
            if len(self.__value_seq) and \
                self.__value_seq[-1] < self.__values_mean and \
                value >= self.__values_mean:
                self.__zero_passage_count += 1
                self.__period.append(self.__period_counter)
                self.__period_counter = 0

            self.__value_seq.append(value)
            self.__values_counter += 1
            self.__period_counter += 1

            if self.__first_period:
                self.__values_mean = sum(self.__value_seq) / self.__values_counter
    
    def flush(self):
        with self.__mutex:
            self.__values_mean = sum(self.__value_seq) / self.__values_counter

            self.__value_seq = list()
            self.__values_counter = 0

            self.__period_counter = 0
            self.__period = []
            self.__zero_passage_count = 0

            self.__first_period = False
    
    def get_sequence(self):
        with self.__mutex:
            if len(self.__period) > 0:
                period = sum(self.__period) / len(self.__period)
            else:
                period = 0

            self.__last_period = period

            return self.__value_seq, period
        
    def can_send(self, limit: int = 0):
        with self.__mutex:
            if limit == -1 and self.__last_period is not None:
                limit = self.__last_period
            
            if self.__period_counter > limit and limit != 0:
                return True
            
            return self.__zero_passage_count >= 2
