import os
import random
import dotenv
dotenv.load_dotenv('/mnt/.env')


client_cred_1 = {"username": os.getenv("CLIENT_USERNAME_DD_1"), "password": os.getenv("CLIENT_PWD_DD_1")}
client_cred_2 = {"username": os.getenv("CLIENT_USERNAME_DD_2"), "password": os.getenv("CLIENT_PWD_DD_2")}
client_cred_3 = {"username": os.getenv("CLIENT_USERNAME_DD_3"), "password": os.getenv("CLIENT_PWD_DD_3")}
client_cred_4 = {"username": os.getenv("CLIENT_USERNAME_DD_4"), "password": os.getenv("CLIENT_PWD_DD_4")}
client_cred_5 = {"username": os.getenv("CLIENT_USERNAME_DD_5"), "password": os.getenv("CLIENT_PWD_DD_5")}
client_cred_6 = {"username": os.getenv("CLIENT_USERNAME_DD_6"), "password": os.getenv("CLIENT_PWD_DD_6")}
# client_cred = random.choice([client_cred_1, client_cred_2, client_cred_3, client_cred_4, client_cred_5, client_cred_6])
# CLIENT_USERNAME = client_cred["username"]
# CLIENT_PWD = client_cred["password"]
CLIENT_CRED_LST = [client_cred_1, client_cred_2, client_cred_3, client_cred_4, client_cred_5, client_cred_6]

MAX_THREADS = os.getenv("MAX_THREADS_DD")

DRIVER = os.getenv("DRIVER_DD")
