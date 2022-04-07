from dotenv import load_dotenv
from app import init_app
import os

load_dotenv('.env')

app = init_app()

host_ip = os.getenv('FLASK_HOST')
host_port = os.getenv('FLASK_PORT')
app.run(host=host_ip, port=host_port)