from flask import Flask, Response
import time
import json

class TaskTwo:

    def __init__(self):
        self.is_debug = True

    def performe_task_two(self):
        if self.is_debug:
            print('Performing task two: ')
        time.sleep(3)

app = Flask(__name__)
taskTwo = TaskTwo()

@app.route('/health')
def health():
    return '200'

@app.route('/experiment/task_two', methods=['POST'])
def perform_task_two():
    start_time = time.time()
    taskTwo.performe_task_two()
    end_time = time.time()
    data = dict()
    data['Time'] = end_time - start_time
    response = Response(response=json.dumps(data),
                            status=200,
                            mimetype='application/json')
    if taskTwo.is_debug:
        print(response)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='10082')
