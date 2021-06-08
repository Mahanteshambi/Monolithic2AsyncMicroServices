from flask import Flask, Response
import time
import json

class TaskThree:

    def __init__(self):
        self.is_debug = True

    def performe_task_three(self):
        if self.is_debug:
            print('Performing task three: ')
        time.sleep(3)

app = Flask(__name__)
taskThree = TaskThree()

@app.route('/health')
def health():
    return '200'

@app.route('/experiment/task_three', methods=['POST'])
def perform_task_three():
    start_time = time.time()
    taskThree.performe_task_three()
    end_time = time.time()
    data = dict()
    data['Time'] = end_time - start_time
    response = Response(response=json.dumps(data),
                            status=200,
                            mimetype='application/json')
    if taskThree.is_debug:
        print(response)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='10083')
