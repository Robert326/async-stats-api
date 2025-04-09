import json
import threading
from queue import Queue

class ManagerJoburi:
    """
    Managerul de joburi
    """
    def __init__(self):
        """
        Constructorul clasei ManagerJoburi
        """
        self.job_status = {} # Stochez statusul joburilor si ce joburi sunt (ex: states_mean)
        self.job_queue = Queue() # Coada pt joburi
        self.lock = threading.Lock() # Lock pt a nu avea conflicte la accesul datelor
        self.job_counter = 0 # un contor pt a asigna id-uri unice joburilor

    def add_job(self, status, job, data):
        """
        Adaug un job in coada
        """
        with self.lock: # blochez accesul doar pentru un singur thread
            self.job_counter += 1
            job_id = self.job_counter
            self.job_status[job_id] = {
                "status": status, 
                "jobType": job
            }

        # nu mai e necesar lock-ul pentru ca mai multe threaduri pot adauga joburi deodata
        job = {
            "id": job_id,
            "status": status,
            "jobType": job,
            "data": data
        }
        self.job_queue.put(job)
        return job_id

    def update_status(self, job_id, status):
        """
        Updatez statusul unui job
        """
        with self.lock:
            self.job_status[job_id]["status"] = status

    def get_status(self, job_id):
        """
        Returnez statusul unui job
        """
        with self.lock:
            if job_id in self.job_status:
                return self.job_status[job_id]["status"]
        return None

    def get_result(self, job_id):
        """
        Returnez rezultatul unui job
        """
        if self.get_status(int(job_id)) == "done":
            try:
                with open(f"results/{job_id}.json", "r") as f:
                    result = json.load(f)
                    print(f"Result for job {job_id} is {result}")
                return result
            except FileNotFoundError:
                return None

    def get_num_jobs(self):
        """
        Returnez numarul de joburi din coada
        """
        return self.job_queue.qsize()

jobManager = ManagerJoburi() # Creez o instanta a managerului de joburi
