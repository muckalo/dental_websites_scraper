import os
import dotenv
# dotenv.load_dotenv('/home/muckalo/PycharmProjects/Projects/Nikunj/dental/docker_mnt/.env')  # LOCAL
# dotenv.load_dotenv('/home/muckalo/monitor_scrapers/.env')  # GCLOUD
dotenv.load_dotenv('/mnt/.env')  # DOCKER


PROJECT_NAME = 'dental'

""" Proxies """
# PROXY = os.getenv("PROXY")

cwd = os.getcwd()
cwd_split = cwd.split(PROJECT_NAME)[0]
PROJECT_DIR_PATH = '{}{}'.format(cwd_split, PROJECT_NAME)

""" DATABASE"""
APPLICATION_POSTGRES_USER = os.getenv("APPLICATION_POSTGRES_USER")
APPLICATION_POSTGRES_PW = os.getenv("APPLICATION_POSTGRES_PW")
APPLICATION_POSTGRES_HOST = os.getenv("APPLICATION_POSTGRES_HOST")
APPLICATION_POSTGRES_DB = os.getenv("APPLICATION_POSTGRES_DB")
DB_PARAMS = {
    "host": APPLICATION_POSTGRES_HOST,
    "database": APPLICATION_POSTGRES_DB,
    "user": APPLICATION_POSTGRES_USER,
    "password": APPLICATION_POSTGRES_PW
}

psql_dental_table_name = 'dental'

""" Product data - fix values """
logo_img_link_hs = 'https://dentalsupply.uk/wp-content/uploads/2021/10/HenrySchein-1.jpg'
logo_img_link_dd = 'https://dentalsupply.uk/wp-content/uploads/2021/10/DD.jpg'
logo_img_link_ds = 'https://dentalsupply.uk/wp-content/uploads/2021/10/DentalSky.jpg'
logo_img_link_nd = 'https://dentalsupply.uk/wp-content/uploads/2021/10/NextDental.jpg'
logo_img_link_ke = 'https://dentalsupply.uk/wp-content/uploads/2021/10/KentExpress.jpg'
product_name_color = '#808080'
price_color = '#808080'
lowest_price_color = '#00940A'
btn_color = '#377DFF'

# CSV_INPUT_FP = '/mnt/files/input/BotInputFile_CSV3.csv'
CSV_INPUT_FP = '/mnt/files/input/input.csv'

CSV_OUTPUT_FP = '/mnt/files/output/Output.csv'

CSV_FAILED_OUTPUT_FP = '/mnt/files/output/Failed.csv'

THREAD_LOG_START_PROGRAM = '/mnt/files/thread_logs/start_program.log'
THREAD_LOG_MAIN_SCRAPER = '/mnt/files/thread_logs/main_scraper.log'

MAX_THREADS_HENRYSCHEIN = os.getenv("MAX_THREADS_HENRYSCHEIN")
MAX_THREADS_DD = os.getenv("MAX_THREADS_DD")
MAX_THREADS_DENTAL_SKY = os.getenv("MAX_THREADS_DENTAL_SKY")
MAX_THREADS_NEXT_DENTAL = os.getenv("MAX_THREADS_NEXT_DENTAL")
MAX_THREADS_KENT_EXPRESS = os.getenv("MAX_THREADS_KENT_EXPRESS")

MAX_ATTEMPTS_URL_ERROR = os.getenv("MAX_ATTEMPTS_URL_ERROR")

NOTIFICATION_EMAIL_FROM = os.getenv("NOTIFICATION_EMAIL_FROM")
NOTIFICATION_EMAIL_PASSWORD = os.getenv("NOTIFICATION_EMAIL_PASSWORD")
NOTIFICATION_EMAIL_TO = os.getenv("NOTIFICATION_EMAIL_TO")

SFTP_HOSTNAME = os.getenv("SFTP_HOSTNAME")
SFTP_USERNAME = os.getenv("SFTP_USERNAME")
SFTP_PASSWORD = os.getenv("SFTP_PASSWORD")
