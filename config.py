from dotenv import load_dotenv
import os

MONGO_URL = "mongodb+srv://pedroetges11:PedroEtges11@pfc.0hhrvpi.mongodb.net/?retryWrites=true&w=majority"#os.environ.get('MONGO_URL')
SECRET_KEY = '264e27bfc06137833f7603cfd26f9a98fa0c784aef640e5b192b43486257aab0' #os.environ.get('SECRET_KEY')
ALGORITHM = 'HS256'#os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 600 #os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES') 