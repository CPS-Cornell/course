import time

class Timeout:
    def __init__(self, timeout: float):
        """
        Starts a timer that will expire after the given timeout.

        :param timeout: The timeout, in seconds
        :type timeout: float
        """
        if timeout: 
            self.timeout = timeout*1000
        else:
            self.timeout = None
        self.start_time = time.ticks_ms()
    
    def is_done(self):
        """
        :return: True if the timeout has expired, False otherwise
        """
        if self.timeout is None:
            return False
        return time.ticks_ms() - self.start_time > self.timeout