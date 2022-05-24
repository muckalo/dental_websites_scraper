import os
import random
import dotenv
dotenv.load_dotenv('/mnt/.env')


client_cred_1 = {"username": os.getenv("CLIENT_USERNAME_DENTAL_SKY_1"), "password": os.getenv("CLIENT_PWD_DENTAL_SKY_1")}
client_cred_2 = {"username": os.getenv("CLIENT_USERNAME_DENTAL_SKY_2"), "password": os.getenv("CLIENT_PWD_DENTAL_SKY_2")}
client_cred_3 = {"username": os.getenv("CLIENT_USERNAME_DENTAL_SKY_3"), "password": os.getenv("CLIENT_PWD_DENTAL_SKY_3")}
client_cred_4 = {"username": os.getenv("CLIENT_USERNAME_DENTAL_SKY_4"), "password": os.getenv("CLIENT_PWD_DENTAL_SKY_4")}
client_cred_5 = {"username": os.getenv("CLIENT_USERNAME_DENTAL_SKY_5"), "password": os.getenv("CLIENT_PWD_DENTAL_SKY_5")}
# client_cred = random.choice([client_cred_1, client_cred_2, client_cred_3, client_cred_4, client_cred_5])
# CLIENT_USERNAME = client_cred["username"]
# CLIENT_PWD = client_cred["password"]
CLIENT_CRED_LST = [client_cred_1, client_cred_2, client_cred_3, client_cred_4, client_cred_5]

MAX_THREADS = os.getenv("MAX_THREADS_DENTAL_SKY")

DRIVER = os.getenv("DRIVER_DENTAL_SKY")
