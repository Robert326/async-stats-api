import json
import threading 
from queue import Queue

class ManagerJoburi:
    def __init__(self):
        self.job_status = {} # Stochez statusul joburilor
        self.job_queue = Queue() # Coada pt joburi
        self.lock = threading.Lock() # Lock pt a nu avea conflicte la accesul datelor
        self.job_counter = 0 # un contor pt a asigna id-uri unice joburilor
    
    def addJob(self, status, data):
        with self.lock: # blochez accesul doar pentru un singur thread
            self.job_counter += 1
            job_id = self.job_counter
            self.job_status[job_id] = status
        
        # nu mai e necesar lock-ul pentru ca mai multe threaduri pot adauga joburi deodata
        job = {id: job_id, status: status, data: data}
        self.job_queue.put(job) 
        return job_id
    
    def updateStatus(self, job_id, status):
        with self.lock:
            self.job_status[job_id] = status

    def getStatus(self, job_id):
        with self.lock:
            return self.job_status.get(job_id, None)

jobManager = ManagerJoburi() # Creez o instanta a managerului de joburi

