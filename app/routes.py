from app import webserver
from flask import request, jsonify, current_app
from app.manager_jobs import jobManager

from app.task_runner import ThreadPool

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    # Method Not Allowed
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")

    job_status = jobManager.get_status(int(job_id))
    if job_status is None:
        # Job does not exist
        return jsonify({
            'status': 'error',
            'message': f"Job ID {job_id} not found"
        }), 404

    if job_status == 'done':
        result_data = jobManager.get_result(int(job_id))
        return jsonify({
            'status': 'done',
            'data': result_data
        })

    if job_status == 'running':
        return jsonify({
            'status': 'running',
            'message': 'Job is still processing'
        })

    # Daca am ajuns aici e ceva problema
    return jsonify({
        'status': 'error',
        'message': f"Unknown job status for job {job_id}"
    }), 500


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    thread_pool = current_app.tasks_runner

    if thread_pool.shutdown_event.is_set():
        return jsonify({"status": "error", "reason": "shutting down"})

    data = request.json
    print(f"Got request {data}")
    job_id = jobManager.add_job("running", "states_mean_request", data)
    return jsonify({"job_id": job_id}), 200


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    thread_pool = current_app.tasks_runner

    if thread_pool.shutdown_event.is_set():
        return jsonify({"status": "error", "reason": "shutting down"})

    data = request.json
    job_id = jobManager.add_job("running", "state_mean", data)
    return jsonify({"status": "running", "job_id": job_id}), 200


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    thread_pool = current_app.tasks_runner

    if thread_pool.shutdown_event.is_set():
        return jsonify({"status": "error", "reason": "shutting down"})

    data = request.json
    job_id = jobManager.add_job("running", "best5", data)
    return jsonify({"status": "running", "job_id": job_id}), 200

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    thread_pool = current_app.tasks_runner

    if thread_pool.shutdown_event.is_set():
        return jsonify({"status": "error", "reason": "shutting down"})

    data = request.json
    job_id = jobManager.add_job("running", "worst5", data)
    return jsonify({"status": "running", "job_id": job_id}), 200

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    thread_pool = current_app.tasks_runner

    if thread_pool.shutdown_event.is_set():
        return jsonify({"status": "error", "reason": "shutting down"})

    data = request.json
    job_id = jobManager.add_job("running", "global_mean", data)
    return jsonify({"status": "running", "job_id": job_id}), 200

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    thread_pool = current_app.tasks_runner

    if thread_pool.shutdown_event.is_set():
        return jsonify({"status": "error", "reason": "shutting down"})

    data = request.json
    job_id = jobManager.add_job("running", "diff_from_mean", data)
    return jsonify({"status": "running", "job_id": job_id}), 200

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    thread_pool = current_app.tasks_runner

    if thread_pool.shutdown_event.is_set():
        return jsonify({"status": "error", "reason": "shutting down"})

    data = request.json
    job_id = jobManager.add_job("running", "state_diff_from_mean_request", data)
    return jsonify({"status": "running", "job_id": job_id}), 200

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    thread_pool = current_app.tasks_runner

    if thread_pool.shutdown_event.is_set():
        return jsonify({"status": "error", "reason": "shutting down"})

    data = request.json
    job_id = jobManager.add_job("running", "mean_by_category_request", data)
    return jsonify({"status": "running", "job_id": job_id}), 200

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    thread_pool = current_app.tasks_runner

    if thread_pool.shutdown_event.is_set():
        return jsonify({"status": "error", "reason": "shutting down"})

    data = request.json
    job_id = jobManager.add_job("running", "state_mean_by_category_request", data)
    return jsonify({"status": "running", "job_id": job_id}), 200

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    """
    Gracefully shutdown the web server.
    """
    thread_pool = current_app.tasks_runner
    if thread_pool is None:
        return jsonify({"status": "error", "reason": "Thread pool not initialized"}), 500

    thread_pool.shutdown()

    if thread_pool.is_drained():
        status = "done"
    else:
        status = "running"

    return jsonify({"status": status}), 200

@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    num_jobs = jobManager.get_num_jobs()
    return jsonify({"num_jobs": num_jobs}), 200

@webserver.route('/api/jobs', methods=['GET'])
def jobs():
    """
    Get the status of all jobs.
    """
    jobs_data = jobManager.job_status

    if not jobs_data:
        return jsonify({"status": "no jobs"}), 200

    jobs_list = [{str(job_id): info["status"]} for job_id, info in jobs_data.items()]

    response = {
        "status": "done",
        "data": jobs_list
    }

    return jsonify(response)

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
