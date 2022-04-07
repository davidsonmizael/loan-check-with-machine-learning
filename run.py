from dotenv import load_dotenv
from app import init_app

load_dotenv('.env')

app = init_app()

app.run(host='0.0.0.0', port=5555)