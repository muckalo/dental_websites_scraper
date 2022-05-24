import os
import random
import dotenv
dotenv.load_dotenv('/mnt/.env')


client_cred_1 = {"username": os.getenv("CLIENT_USERNAME_HENRYSCHEIN_1"), "password": os.getenv("CLIENT_PWD_HENRYSCHEIN_1")}
client_cred_2 = {"username": os.getenv("CLIENT_USERNAME_HENRYSCHEIN_2"), "password": os.getenv("CLIENT_PWD_HENRYSCHEIN_2")}
client_cred_3 = {"username": os.getenv("CLIENT_USERNAME_HENRYSCHEIN_3"), "password": os.getenv("CLIENT_PWD_HENRYSCHEIN_3")}
# client_cred_4 = {"username": os.getenv("CLIENT_USERNAME_HENRYSCHEIN_4"), "password": os.getenv("CLIENT_PWD_HENRYSCHEIN_4")}  # BAD
# client_cred_5 = {"username": os.getenv("CLIENT_USERNAME_HENRYSCHEIN_5"), "password": os.getenv("CLIENT_PWD_HENRYSCHEIN_5")}  # BAD
client_cred_6 = {"username": os.getenv("CLIENT_USERNAME_HENRYSCHEIN_6"), "password": os.getenv("CLIENT_PWD_HENRYSCHEIN_6")}
client_cred_7 = {"username": os.getenv("CLIENT_USERNAME_HENRYSCHEIN_7"), "password": os.getenv("CLIENT_PWD_HENRYSCHEIN_7")}
client_cred_8 = {"username": os.getenv("CLIENT_USERNAME_HENRYSCHEIN_8"), "password": os.getenv("CLIENT_PWD_HENRYSCHEIN_8")}
client_cred_9 = {"username": os.getenv("CLIENT_USERNAME_HENRYSCHEIN_9"), "password": os.getenv("CLIENT_PWD_HENRYSCHEIN_9")}
client_cred_10 = {"username": os.getenv("CLIENT_USERNAME_HENRYSCHEIN_10"), "password": os.getenv("CLIENT_PWD_HENRYSCHEIN_10")}
client_cred_11 = {"username": os.getenv("CLIENT_USERNAME_HENRYSCHEIN_11"), "password": os.getenv("CLIENT_PWD_HENRYSCHEIN_11")}
# # client_cred = random.choice([client_cred_1, client_cred_2, client_cred_3, client_cred_4, client_cred_5, client_cred_6, client_cred_7, client_cred_8])
# # CLIENT_USERNAME = client_cred["username"]
# # CLIENT_PWD = client_cred["password"]
CLIENT_CRED_LST = [client_cred_1, client_cred_2, client_cred_3, client_cred_6, client_cred_7, client_cred_8, client_cred_9, client_cred_10, client_cred_11]

MAX_THREADS = os.getenv("MAX_THREADS_HENRYSCHEIN")

DRIVER = os.getenv("DRIVER_HENRYSCHEIN")
