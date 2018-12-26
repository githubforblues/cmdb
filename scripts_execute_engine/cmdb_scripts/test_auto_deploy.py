
def main():

    import subprocess
    import requests
    import random
    import sys
    import time

    API_SERVER_IP = '127.0.0.1'
    API_SERVER_PORT = '8100'

    API_DEPLOY_ROW_GET = '/api/autodeploy/rowget/'
    API_DEPLOY_SERVICE_DELETE = '/api/autodeploy/scriptdelete/'

    while True:
        url = 'http://{}:{}{}'.format(API_SERVER_IP, API_SERVER_PORT, API_DEPLOY_ROW_GET)
        rowdata = requests.get(url).text
        if rowdata == 'empty':
            url = 'http://{}:{}{}'.format(API_SERVER_IP, API_SERVER_PORT, API_DEPLOY_SERVICE_DELETE)
            url = url + '?scriptname=test_auto_deploy.py'
            result = requests.get(url)
            return 0
        else:
            # out = subprocess.check_output("touch testfile-{}".format(random.randint(10000, 99999)), stderr=subprocess.STDOUT,shell=True)
            time.sleep(10)
            print('发布...')


if __name__ == '__main__':
    main()




