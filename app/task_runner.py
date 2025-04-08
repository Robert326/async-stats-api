from queue import Queue
from threading import Thread, Event
import time
from app.data_ingestor import DataIngestor
from app.ManagerJobs import jobManager
import pandas as pd
import os
import json
from app.functions import states_mean_request, state_mean_request, best5_request
from app.functions import worst5_request, global_mean_request, diff_from_mean_request
from app.functions import state_diff_from_mean_request, mean_by_category_request
from app.functions import state_mean_by_category_request


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

class TaskRunner(Thread):
    def __init__(self, data_ingestor):
        # TODO: init necessary data structures
        super().__init__()
        self.data_ingestor = data_ingestor 
    
    def save_result_to_disk(self, job_id, result):
        result_dir = "results"
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        
        result_path = os.path.join(result_dir, f"{job_id}.json")

        with open(result_path, "w") as f:
            json.dump(result, f)

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
            df = self.data_ingestor.df
            try:
                match job_type:
                    case "states_mean_request":
                        result = states_mean_request(data, df)
                    case "state_mean":
                        result = state_mean_request(data, df)
                    case "best5":
                        result = best5_request(data, df, self.data_ingestor.questions_best_is_min, self.data_ingestor.questions_best_is_max)
                    case "worst5":
                        result = worst5_request(data, df, self.data_ingestor.questions_best_is_min, self.data_ingestor.questions_best_is_max)
                    case "global_mean":
                        result = global_mean_request(data, df)
                    case "diff_from_mean":
                        result = diff_from_mean_request(data, df)
                    case "state_diff_from_mean_request":
                        result = state_diff_from_mean_request(data, df)
                    case "mean_by_category_request":
                        result = mean_by_category_request(data, df)
                    case "state_mean_by_category_request":
                        result = state_mean_by_category_request(data, df)
                    case _:
                        raise ValueError(f"Unknown job type: {job_type}")
                self.save_result_to_disk(job_id, result)
                jobManager.updateStatus(job_id, "done")
            except Exception as e:
                print(f"[ERROR] Job {job_id} failed: {e}")
                jobManager.updateStatus(job_id, "failed")
            jobManager.job_queue.task_done()
