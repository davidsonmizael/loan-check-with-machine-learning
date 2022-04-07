import os
from run import app 
from dotenv import load_dotenv

load_dotenv('.env')

if __name__ == '__main__':
    host_ip = os.getenv('FLASK_HOST')
    host_port = os.getenv('FLASK_PORT')
    app.run(host=host_ip, port=host_port)