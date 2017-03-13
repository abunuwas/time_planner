from datetime import datetime
import logging

from flask import (abort,
                   flash,
                   g,
                   jsonify,
                   make_response,
                   redirect,
                   render_template,
                   request,
                   session,
                   url_for)

from app import app

logger = logging.getLogger(__name__)


tasks = [
    {
        'id': 1,
        'title': 'Read book',
        'goal': 'Read one book per month',
        'when': datetime.utcnow().isoformat(),
        'done': False
    },
    {
        'id': 2,
        'title': 'Cook',
        'goal': None,
        'when': datetime.utcnow().isoformat(),
        'done': True
    }
]


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def method_not_allowed(_):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    pass


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


@app.route('/task/<int:task_id>', methods=['GET'])
def get_task(task_id=None):
    task = [task for task in tasks if task['id'] == task_id]
    if task:
        return jsonify(task)
    return abort(404)


@app.route('/task', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    new_task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'goal': request.json.get('goal'),
        'when': request.json.get('when'),
        'done': request.json.get('done', False)
    }
    tasks.append(new_task)
    return jsonify({'task': new_task}), 201


@app.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id=None):
    task = [task for task in tasks if task['id'] == task_id][0]
    if not task:
        return abort(404)
    if not request.json:
        abort(400)
    task['title'] = request.json.get('title', task['title'])
    task['goal'] = request.json.get('goal', task['goal'])
    task['when'] = request.json.get('when', task['when'])
    task['done'] = request.json.get('done', task['done'])
    return jsonify({'task': task})


@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id=None):
    task = [task for task in tasks if task['id'] == task_id]
    if task:
        tasks.remove(task[0])
        return jsonify({'result': True})
    abort(404)


@app.route('/log_time/<time>/task/<task>', methods=['POST'])
def log_time(time, task):
    return 'you are logging time %s for task %s' % (time, task)


@app.route('/goals', methods=['GET'])
def get_goals():
    pass


@app.route('/goal/<goal_id>', methods=['GET'])
def get_goal():
    pass


@app.route('/goal', methods=['POST'])
def create_goal():
    pass


@app.route('/goal/<goal_id>', methods=['UPDATE'])
def update_goal(goal_id=None):
    pass


@app.route('/goal/<goal_id>', methods=['DELETE'])
def delete_goal(goal_id=None):
    pass
