from flask import Flask, Response, request
import requests
import os
import datetime
import time
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ProcessRequest:

    def __init__(self, ):
        self.is_asycn = False
        self.is_debug = True
        self.UPLOAD_FOLDER = './queryinput/'
        task_one_url = 'http://127.0.0.1:10081/experiment/task_one'
        task_two_url = 'http://127.0.0.1:10082/experiment/task_two'
        task_three_url = 'http://127.0.0.1:10083/experiment/task_three'
        self.tasks_url_list = [task_one_url, task_two_url, task_three_url]
        try:
            os.makedirs(self.UPLOAD_FOLDER)
        except FileExistsError:
            pass

    def process_request_serially(self, img_file):
        if self.is_debug:
            print('Processing request', img_file)
        files = {'media': open(img_file, 'rb')}
        for url in self.tasks_url_list:
            #print('URL: ', url)
            response = requests.post(url, files=files)
            response = response.json()
            print('URL: ', url, '; Response: ', response)

    def process_request_parallely(self, img_file):
        if self.is_debug:
            print('Processing request parallely: ', img_file)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        #future = asyncio.ensure_future(self.process_parallely())
        #loop.run_until_complete(future)
        loop.run_until_complete(self.process_parallely())
        #loop.run_until_complete(self.process_parallely_async())

    async def process_parallely_async(self):
        task_responses = list()
        loop = asyncio.get_event_loop()
        session = requests.Session()
        for url in self.tasks_url_list:
            task_responses.append(loop.create_task(self.fetch(session, url)))
        #await asyncio.wait(task_responses)
        for response in await asyncio.gather(task_responses):
            response = json.loads(response)
            print(response)

    async def process_parallely(self):
        with ThreadPoolExecutor(max_workers=3) as executor:
            with requests.Session() as session:
                loop = asyncio.get_event_loop()
                tasks = [
                        loop.run_in_executor(
                            executor,
                            self.fetch,
                            *(session, url)
                        ) 
                        for url in self.tasks_url_list
                ]
                count = 0
                for response in await asyncio.gather(*tasks):
                    response = json.loads(response)
                    count += 1
                    print(response)

    def fetch(self, session, url):
        with session.post(url) as response:
            data = response.text
            if response.status_code != 200:
                print('Failed: (0)'.format(url))
            return data


    def save_image(self):
        if self.is_debug:
            print('Files in request: ', request.files)
        img_file = request.files['file']
        curr_date_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        curr_file_name = os.path.join(self.UPLOAD_FOLDER, curr_date_time + '_' + img_file.filename)
        if self.is_debug:
            print('Saving image at ', curr_file_name)
        img_file.save(curr_file_name)
        return curr_file_name

app = Flask(__name__)
requestProcessor = ProcessRequest()

@app.route('/health')
def health():
    return '200'

@app.route('/experiment/aync/', methods=['POST'])
def classify_image():
    start_time = time.time()
    img_file = requestProcessor.save_image()
    #requestProcessor.process_request_serially(img_file)
    requestProcessor.process_request_parallely(img_file)
    end_time = time.time()
    print('Total processing time: ', (end_time - start_time))
    data = dict()
    data['Time'] = end_time - start_time
    response = Response(response=json.dumps(data),
                status=200,
                mimetype='application/json')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10080)
