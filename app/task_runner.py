from threading import Thread, Event
import json
from queue import Empty
import os
from app.manager_jobs import jobManager
from app.functions import (
    states_mean_request, state_mean_request, best5_request,
    worst5_request, global_mean_request, diff_from_mean_request,
    state_diff_from_mean_request, mean_by_category_request, state_mean_by_category_request
)


class ThreadPool:
    """
    A thread pool that manages a number of worker threads to process jobs concurrently.
    """
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

        self.shutdown_event = Event()

        if "TP_NUM_OF_THREADS" in os.environ:
            num_threads = int(os.environ["TP_NUM_OF_THREADS"])
        else:
            num_threads = os.cpu_count()

        for _ in range(num_threads):
            thread = TaskRunner(self.data_ingestor, self.shutdown_event)
            thread.start()
            self.threads.append(thread)

    def shutdown(self):
        """
        Shutdown the thread pool gracefully.
        """
        self.shutdown_event.set()

        for thread in self.threads:
            thread.join()

    def is_drained(self):
        """
        Check if the job queue is empy.
        """
        return jobManager.job_queue.empty()

class TaskRunner(Thread):
    def __init__(self, data_ingestor, shutdown_event):
        super().__init__()
        self.data_ingestor = data_ingestor
        self.shutdown_event = shutdown_event

    def save_result_to_disk(self, job_id, result):
        """
        Save the result to disk in a JSON file.
        """
        result_dir = "results"
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        result_path = os.path.join(result_dir, f"{job_id}.json")

        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(result, f)

    def run(self):
        while True:

            # Check periodically if the shutdown event is set
            try:
                job = jobManager.job_queue.get(timeout=1)
            except Empty:
                if self.shutdown_event.is_set() and jobManager.job_queue.empty():
                    break
                continue

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
                        result = best5_request(data, df, self.data_ingestor.questions_best_is_min)
                    case "worst5":
                        result = worst5_request(data, df, self.data_ingestor.questions_best_is_min)
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
                jobManager.update_status(job_id, "done")
            except Exception as e:
                print(f"[ERROR] Job {job_id} failed: {e}")
                jobManager.update_status(job_id, "failed")
            jobManager.job_queue.task_done()
