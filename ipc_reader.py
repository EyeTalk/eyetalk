import sysv_ipc
import posix_ipc
import ctypes
import struct


class IPCReader:
    elements_in_vector = 31
    sizeofdouble = ctypes.sizeof(ctypes.c_double)

    def __enter__(self):
        # Connect to existing shared memory
        self.memory = sysv_ipc.SharedMemory(123456)
        # Connect to existing semaphore
        self.sem = posix_ipc.Semaphore("/capstone")
        return self

    def bytes_to_floats(self, bstr):
        tmp = [struct.unpack('<d', bstr[i * self.sizeofdouble:(i + 1) * self.sizeofdouble])[0]
               for i in range(self.elements_in_vector)]
        return tmp

    def read(self):
        self.sem.acquire()
        memory_value = self.memory.read()
        self.sem.release()
        facial_features_list = self.bytes_to_floats(memory_value)
        return facial_features_list

    def clean(self):
        self.sem.unlink()
        self.memory.remove()

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean up Semaphore
        self.sem.close()
        # Clean up shared memory
        try:
            self.memory.detach()
        except:
            pass

