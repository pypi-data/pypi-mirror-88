import threading
import time


class ptthreads:
    def __init__(self):
        self.threads_list = []
        self.free_threads = []
        self.returns = []
        self.lock = threading.Lock()

    def threads (self, items, function, threads):
        self.free_threads.clear()
        self.threads_list.clear()
        self.returns.clear()
        for i in range(threads):
            self.free_threads.append(i)
            self.threads_list.append("")
        for item in items:
            while not self.free_threads:
                time.sleep(0.01)
            thread_no = self.free_threads.pop()
            self.threads_list[thread_no] = threading.Thread(
                target = self.wrapper_worker,
                args = (item, function, thread_no)
            )
            result = self.threads_list[thread_no].start()
        while len(self.free_threads) < threads:
            time.sleep(0.1)
        return self.returns

    def wrapper_worker(self, item, function, thread_no):
        self.returns.append(function(item))
        self.free_threads.append(thread_no)


class ptoutput:
    def __init__(self):
        self.output_string = ""
        self.lock = threading.Lock()

    def add_string_to_output(self, string="", condition=True, end="\n", silent=False, trim=False):
        if condition and not silent:
            if trim:
                string = string.strip()
            self.output_string +=  string + end

    def get_output_string(self):
        return self.output_string

    def print_output(self, condition=True, end="\n", flush=True):
        if condition:
            print(self.output_string, end=end, flush=flush)

    def lock_print_output(self, condition=True, end="\n", flush=True):
        if condition:
            self.lock.acquire()
            print(self.output_string, end=end, flush=flush)
            self.lock.release()