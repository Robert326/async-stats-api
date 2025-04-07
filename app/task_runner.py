from queue import Queue
from threading import Thread, Event
import time
from app.data_ingestor import DataIngestor
from app.ManagerJobs import jobManager
import pandas as pd
import os


class ThreadPool:
    def __init__(self, data_ingestor):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        # Note: the TP_NUM_OF_THREADS env var will be defined by the checker
        self.data_ingestor = data_ingestor
        self.threads = []

        if "TP_NUM_OF_THREADS" in os.environ:
            num_threads = int(os.environ["TP_NUM_OF_THREADS"])
        else: 
            num_threads = os.cpu_count()
    
        for _ in range(num_threads):
            thread = TaskRunner(self.data_ingestor)
            thread.start()
            self.threads.append(thread)



        pass

class TaskRunner(Thread):
    def __init__(self, data_ingestor):
        # TODO: init necessary data structures
        super.__init__()
        self.data_ingestor = data_ingestor 
        pass

    def run(self):
        while True:
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            job = jobManager.job_queue.get()

            job_type = job["jobType"]
            data = job["data"]
            job_id = job["id"]

            pass
