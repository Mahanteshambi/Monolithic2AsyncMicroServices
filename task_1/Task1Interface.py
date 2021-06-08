from flask import Flask, Response
import time
import json

class TaskOne:

    def __init__(self):
        self.is_debug = True

    def performe_task_one(self):
        if self.is_debug:
            print('Performing task one: ')
        time.sleep(3)

app = Flask(__name__)
taskOne = TaskOne()

@app.route('/health')
def health():
    return '200'

@app.route('/experiment/task_one', methods=['POST'])
def perform_task_one():
    start_time = time.time()
    taskOne.performe_task_one()
    end_time = time.time()
    data = dict()
    data['Time'] = end_time - start_time
    response = Response(response=json.dumps(data),
                            status=200,
                            mimetype='application/json')
    if taskOne.is_debug:
        print(response)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='10081')
