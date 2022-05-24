import os
import time
import datetime
import random
import threading
import queue
import json
from app.util import get_current_utc_date_or_datetime, time_for_reset_between_midnight_and_one, \
    redirect_output, \
    insert_data_into_psql, create_tables, open_data_from_csv, remove_file_if_exist, \
    generate_output, \
    create_folder_if_not_exists, save_data_to_csv, \
    task_send_email, query_data_from_psql, insert_all_data_at_once_into_psql, check_does_date_exist, \
    upload_file_to_server, download_file_from_server
from app.config.config import psql_dental_table_name, CSV_INPUT_FP, CSV_OUTPUT_FP, CSV_FAILED_OUTPUT_FP, \
    THREAD_LOG_START_PROGRAM, THREAD_LOG_MAIN_SCRAPER
from app.scrapers import MainScraper

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def download_file_from_gdrive(folder_id, input_csv_file_name, output_fp, settings_fp):
    """ DOWNLOAD FILE FROM GDRIVE """

    """ AUTHENTICATE"""
    gauth = GoogleAuth()
    # gauth = GoogleAuth(settings_file=settings_fp)
    # gauth.CommandLineAuth()
    gauth.ServiceAuth()
    drive = GoogleDrive(gauth)

    """ LIST ALL FILES IN DRIVE """
    file_list = drive.ListFile({'q': "'{folder_id}' in parents and trashed=false".format(folder_id=folder_id)}).GetList()
    for file in file_list:
        title = file['title']
        if title != input_csv_file_name:
            continue
        file.GetContentFile(output_fp)


def generate_email_data(items_for_scraping):
    failed_lst = []
    txt = ''''''
    txt += 'Total Scrapers: {} \n'.format(len(items_for_scraping))
    for item_for_scraping in items_for_scraping:
        scraper_name = item_for_scraping['scraper_name']
        like_url = item_for_scraping['like_url']
        sql = """SELECT * FROM {table_name} WHERE status_done is true AND product_url LIKE '%{like_url}%';""".format(table_name=psql_dental_table_name, like_url=like_url)
        success_processed_urls = query_data_from_psql(sql, row_count=True)
        sql = """SELECT * FROM {table_name} WHERE url_error is true AND product_url LIKE '%{like_url}%';""".format(table_name=psql_dental_table_name, like_url=like_url)
        failed_processed_urls = query_data_from_psql(sql, fetch_all=True)
        sql = """SELECT * FROM {table_name} WHERE product_url LIKE '%{like_url}%';""".format(table_name=psql_dental_table_name, like_url=like_url)
        total_processed_urls = query_data_from_psql(sql, row_count=True)
        scraper_failed_lst = [
            [i[0], i[1]]
            for i in failed_processed_urls
        ]
        failed_lst.extend(scraper_failed_lst)

        txt += '\n' \
               'Scraper: {} \n' \
               'Success Processed Urls: {} \n' \
               'Failed Processed Urls: {} \n' \
               'Total Processed Urls: {} \n' \
               'Run Time: {} \n'.format(
            scraper_name, success_processed_urls, len(scraper_failed_lst), total_processed_urls, scrapers_speed[scraper_name]
        )
    current_utc_datetime = get_current_utc_date_or_datetime()
    tt = str(datetime.timedelta(seconds=time.time() - st))
    txt += '\n' \
           'Total Run Time: {} \n' \
           'Current UTC Datetime: {}'.format(tt, current_utc_datetime)

    return txt, failed_lst


class StartProgram:
    def single_thread(self, q, t_name):
        while not q.empty():
            queueLock.acquire()
            q_item = q.get()
            queueLock.release()

            """ Do work here """
            scraper_name = q_item['scraper_name']
            like_url = q_item['like_url']
            scraper_obj = MainScraper()
            scraper_obj.run(scraper_name, like_url)

            """ Jobs done """
            done_q_lst.append('c')
            current_utc_datetime = get_current_utc_date_or_datetime()
            tt = str(datetime.timedelta(seconds=time.time() - st))
            msg = json.dumps({
                "thread": t_name,
                "msg": "jobs_done",
                "q": str(q_item),
                "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
                "qsize": q.qsize(),
                "page": "all_done (no filter)",
                "tt": tt,
                "utc": current_utc_datetime
            })
            redirect_output(script_name, msg)

            scrapers_speed[scraper_name] = tt

            q.task_done()

    def start_thread(self, q, t_name):
        current_utc_datetime = get_current_utc_date_or_datetime()
        tt = str(datetime.timedelta(seconds=time.time() - st))
        msg = json.dumps({
            "thread": t_name,
            "msg": "start thread",
            "qsize": q.qsize(),
            "t_active": threading.active_count(),
            "tt": tt,
            "utc": current_utc_datetime
        })
        redirect_output(script_name, msg)

        try:
            self.single_thread(q, t_name)
            current_utc_datetime = get_current_utc_date_or_datetime()
            tt = str(datetime.timedelta(seconds=time.time() - st))
            msg = json.dumps({
            "thread": t_name,
            "msg": "exit thread",
            "qsize": q.qsize(),
            "t_active": threading.active_count(),
            "tt": tt,
            "utc": current_utc_datetime
        })
            redirect_output(script_name, msg)
        except Exception as e:
            current_utc_datetime = get_current_utc_date_or_datetime()
            tt = str(datetime.timedelta(seconds=time.time() - st))
            msg = json.dumps({
                "thread": t_name,
                "msg": "Exception(exit_thread): {}".format(str(e)),
                "qsize": q.qsize(),
                "t_active": threading.active_count(),
                "tt": tt,
                "utc": current_utc_datetime
            })
            redirect_output(script_name, msg)

    def prepare_data_for_queue(self):
        data_for_queue = [
            {'scraper_name': 'henryschein', 'like_url': 'www.henryschein.co.uk'},
            {'scraper_name': 'dd', 'like_url': 'www.ddgroup.com'},
            {'scraper_name': 'dental_sky', 'like_url': 'www.dentalsky.com'},
            {'scraper_name': 'next_dental', 'like_url': 'www.nextdental.com'},
            {'scraper_name': 'kent_express', 'like_url': 'www.kentexpress.co.uk'}
        ]
        return data_for_queue

    def insert_input_csv_into_db(self):
        csv_data = open_data_from_csv(CSV_INPUT_FP, encoding='latin-1')

        csv_data_unique = []
        csv_data_formatted = []
        for i in range(1, len(csv_data)):
            product_id = csv_data[i][1]
            product_url = csv_data[i][0]
            if product_url in csv_data_unique:
                continue
            csv_data_unique.append(product_url)
            d = {'product_id': product_id, 'product_url': product_url}
            csv_data_formatted.append(d)

        insert_result = insert_all_data_at_once_into_psql(csv_data_formatted, psql_dental_table_name)
        return len(csv_data) - 1, insert_result

    def download_file(self):
        try:
            """ Download file from server """
            # input_csv_file_name = 'BotInputFile_CSV3.csv'
            input_csv_file_name = 'input.csv'
            remote_folder_path = '/public_html/bot/'
            local_folder_path = '/mnt/files/input/'
            local_fp = '{}{}'.format(local_folder_path, input_csv_file_name)
            download_file_from_server(remote_folder_path, input_csv_file_name, local_fp)
            time.sleep(5)
        except:
            pass

    def create_db_and_tables_if_not_exists(self):
        """ Find longest url to set max size for varchar """
        csv_data = open_data_from_csv(CSV_INPUT_FP, encoding='latin-1')
        product_url_max_len = max([len(i[0]) for i in csv_data[1:]])

        """ Create db and table """
        sql = """
        CREATE TABLE IF NOT EXISTS {table_name} (
            product_id TEXT,
            product_url VARCHAR({varchar_len}) UNIQUE,
            attempts INTEGER DEFAULT 0,
            status_done BOOLEAN NOT NULL DEFAULT FALSE,
            url_error BOOLEAN DEFAULT FALSE,
            product_data JSON
        )
        """.format(table_name=psql_dental_table_name, varchar_len=product_url_max_len + 10)
        create_tables(sql)

    def delete_table_if_exist(self):
        sql = """DROP TABLE IF EXISTS {table_name};""".format(table_name=psql_dental_table_name)
        query_data_from_psql(sql)

    def run(self):
        global items_for_scraping_len
        global done_q_lst
        global failed_q_lst
        global scrapers_speed

        main_thread_name = "T-sp-m"

        date_exist = check_does_date_exist('status')
        jobs_date = date_exist["jobs_date"]
        started = date_exist["started"]
        finished = date_exist["finished"]

        msg = json.dumps({"thread": main_thread_name, "started": "{} {}".format(type(started), started), "date_exist": str(date_exist)})
        redirect_output(script_name, msg)

        """ Create DB at the start - we will delete it at the end """
        if not started:
            self.create_db_and_tables_if_not_exists()
            self.download_file()
            self.insert_input_csv_into_db()
            # Update "started" to True
            update_col = 'started'
            update_val = True
            match_col = 'jobs_date'
            match_val = jobs_date
            sql = """UPDATE {} SET {} = '{}' WHERE {} = '{}'""".format(
                'status', update_col, update_val, match_col, match_val
            )
            update_status = query_data_from_psql(sql, row_count=True)
            print('update_status(started): {}'.format(update_status))
            msg = json.dumps({"thread": main_thread_name, "update_status(started)": update_status})
            redirect_output(script_name, msg)

        """ Update "last_restart" in status """
        update_col = 'last_restart'
        update_val = get_current_utc_date_or_datetime()
        match_col = 'jobs_date'
        match_val = jobs_date
        sql = """UPDATE {} SET {} = '{}' WHERE {} = '{}'""".format(
            'status', update_col, update_val, match_col, match_val
        )
        update_status = query_data_from_psql(sql, row_count=True)
        print('update_status(last_restart): {}'.format(update_status))
        msg = json.dumps({"thread": main_thread_name, "update_status(started)": update_status})
        redirect_output(script_name, msg)

        """ Prepare data for queue """
        data_for_queue = self.prepare_data_for_queue()
        """ Copy data to template list """
        items_for_scraping = data_for_queue.copy()
        """ Shuffle list """
        random.shuffle(items_for_scraping)
        items_for_scraping_len = len(items_for_scraping)
        """ Set max number of threads """
        max_threads = 5
        if max_threads > items_for_scraping_len:
            max_threads = items_for_scraping_len
        current_utc_datetime = get_current_utc_date_or_datetime()
        tt = str(datetime.timedelta(seconds=time.time() - st))
        msg = json.dumps({
            "thread": main_thread_name,
            "max_threads": max_threads,
            "items_for_scraping": items_for_scraping_len,
            "tt": tt,
            "utc": current_utc_datetime,
        })
        redirect_output(script_name, msg)
        """ Fill the queue """
        [workQueue.put(i) for i in items_for_scraping]
        """ Start threads """
        threads = []
        for i_thread in range(max_threads):
            t_name = "T-sp-{}".format(i_thread + 1)
            t = threading.Thread(target=self.start_thread, args=(workQueue, t_name))
            t.daemon = True
            threads.append(t)
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        done_q_lst = list()
        failed_q_lst = list()

        """ Generate output data """
        current_utc_datetime = get_current_utc_date_or_datetime()
        tt = str(datetime.timedelta(seconds=time.time() - st))
        msg = json.dumps({
            "thread": main_thread_name,
            "generate_output": "started",
            "tt": tt,
            "utc": current_utc_datetime
        })
        redirect_output(script_name, msg)
        output_data = generate_output()
        current_utc_datetime = get_current_utc_date_or_datetime()
        tt = str(datetime.timedelta(seconds=time.time() - st))
        msg = json.dumps({
            "thread": main_thread_name,
            "generate_output": "finished",
            "tt": tt,
            "utc": current_utc_datetime
        })
        redirect_output(script_name, msg)

        """ Save output data - historical """
        csv_fp_split = CSV_OUTPUT_FP.rsplit('/', 1)
        historical_fp = '{}/historical/'.format(csv_fp_split[0])
        create_folder_if_not_exists(historical_fp)
        file_name_split = csv_fp_split[1].rsplit('.', 1)
        current_date_time_formatted = get_current_utc_date_or_datetime().replace('-', '').replace(':', '').replace(' ', '_')
        historical_file_name = '{}_{}.{}'.format(file_name_split[0], current_date_time_formatted, file_name_split[1])
        csv_output_fp_historical = '{}{}'.format(historical_fp, historical_file_name)
        encoding_str = None
        save_data_to_csv(csv_output_fp_historical, output_data, encoding=encoding_str)
        current_utc_datetime = get_current_utc_date_or_datetime()
        tt = str(datetime.timedelta(seconds=time.time() - st))
        msg = json.dumps({
            "thread": main_thread_name,
            "saved_csv": csv_output_fp_historical,
            "tt": tt,
            "utc": current_utc_datetime
        })
        redirect_output(script_name, msg)
        """ Save output data - current """
        save_data_to_csv(CSV_OUTPUT_FP, output_data, encoding=encoding_str)
        current_utc_datetime = get_current_utc_date_or_datetime()
        tt = str(datetime.timedelta(seconds=time.time() - st))
        msg = json.dumps({
            "thread": main_thread_name,
            "saved_csv": CSV_OUTPUT_FP,
            "tt": tt,
            "utc": current_utc_datetime
        })
        redirect_output(script_name, msg)

        """ Send email notification """
        email_subject = "Dental Supply Scrapers Status"
        email_msg, failed_lst = generate_email_data(items_for_scraping)
        task_send_email(email_subject, email_msg)
        current_utc_datetime = get_current_utc_date_or_datetime()
        tt = str(datetime.timedelta(seconds=time.time() - st))
        msg = json.dumps({
            "thread": main_thread_name,
            "email_notification": "sent",
            "tt": tt,
            "utc": current_utc_datetime
        })
        redirect_output(script_name, msg)

        """ Save failed URLs to CSV file """
        if failed_lst:
            save_data_to_csv(CSV_FAILED_OUTPUT_FP, failed_lst)
            current_utc_datetime = get_current_utc_date_or_datetime()
            tt = str(datetime.timedelta(seconds=time.time() - st))
            msg = json.dumps({
                "thread": main_thread_name,
                "saved_csv": CSV_FAILED_OUTPUT_FP,
                "tt": tt,
                "utc": current_utc_datetime
            })
            redirect_output(script_name, msg)
        failed_lst = []

        """ COPY/UPLOAD FILES SOMEWHERE (GDRIVE, FTP, etc...) """
        st_upload = time.time()
        remote_folder_path = '/public_html/bot/'
        remote_historical_folder_path = '{}{}/'.format(remote_folder_path, 'historical')
        remote_output_fp = '{}{}'.format(remote_folder_path, csv_fp_split[1])
        remote_historical_fp = '{}{}'.format(remote_historical_folder_path, historical_file_name)
        remote_failed_file_name = CSV_FAILED_OUTPUT_FP.rsplit('/', 1)[1]
        remote_failed_fp = '{}{}'.format(remote_folder_path, remote_failed_file_name)

        try:
            upload_file_to_server(CSV_OUTPUT_FP, remote_output_fp)
        except Exception as e:
            # current_utc_datetime = get_current_utc_date_or_datetime()
            # tt = str(datetime.timedelta(seconds=time.time() - st))
            # msg = json.dumps({
            #     "thread": main_thread_name,
            #     "Exception(1)": str(e),
            #     "tt": tt,
            #     "utc": current_utc_datetime
            # })
            # redirect_output(script_name, msg)
            pass

        try:
            upload_file_to_server(csv_output_fp_historical, remote_historical_fp)
        except Exception as e:
            # current_utc_datetime = get_current_utc_date_or_datetime()
            # tt = str(datetime.timedelta(seconds=time.time() - st))
            # msg = json.dumps({
            #     "thread": main_thread_name,
            #     "Exception(2)": str(e),
            #     "tt": tt,
            #     "utc": current_utc_datetime
            # })
            # redirect_output(script_name, msg)
            pass

        if failed_lst:
            try:
                upload_file_to_server(CSV_FAILED_OUTPUT_FP, remote_failed_fp)
            except Exception as e:
                # current_utc_datetime = get_current_utc_date_or_datetime()
                # tt = str(datetime.timedelta(seconds=time.time() - st))
                # msg = json.dumps({
                #     "thread": main_thread_name,
                #     "Exception(3)": str(e),
                #     "tt": tt,
                #     "utc": current_utc_datetime
                # })
                # redirect_output(script_name, msg)
                pass

        # """ Delete DB at the end - we will create it at the start """
        self.delete_table_if_exist()
        current_utc_datetime = get_current_utc_date_or_datetime()
        tt = str(datetime.timedelta(seconds=time.time() - st))
        msg = json.dumps({
            "thread": main_thread_name,
            "deleted_psql_table": "true",
            "tt": tt,
            "utc": current_utc_datetime
        })
        redirect_output(script_name, msg)

        # Update "finished" to True
        update_col = 'finished'
        update_val = True
        match_col = 'jobs_date'
        match_val = jobs_date
        sql = """UPDATE {} SET {} = '{}' WHERE {} = '{}'""".format(
            'status', update_col, update_val, match_col, match_val
        )
        update_status = query_data_from_psql(sql, row_count=True)
        # print('update_status(finished): {}'.format(update_status))
        current_utc_datetime = get_current_utc_date_or_datetime()
        tt = str(datetime.timedelta(seconds=time.time() - st))
        msg = json.dumps({
            "thread": main_thread_name,
            "updated_status": str(update_status),
            "tt": tt,
            "utc": current_utc_datetime
        })
        redirect_output(script_name, msg)

        """ Shut down instance """
        # Instance is shut down from "monitor_scrapers.py"

        # @TODO: Remove deleting thread logs from crontab job after You finish next todo
        # DONE - @TODO: After turn is done:
        #   DONE - @TODO: copy thread logs to server or email them
        #   DONE - @TODO: delete thread logs from VM

        """ Upload thread logs to server """
        thread_log_start_program_split = THREAD_LOG_START_PROGRAM.rsplit('/', 1)
        remote_thread_log_start_program = '{}{}'.format(remote_folder_path, thread_log_start_program_split[1])
        try:
            upload_file_to_server(THREAD_LOG_START_PROGRAM, remote_thread_log_start_program)
            msg = json.dumps({
                "thread": main_thread_name,
                "THREAD_LOG_START_PROGRAM": THREAD_LOG_START_PROGRAM,
                "uploaded log": "success"
            })
            redirect_output(script_name, msg)
        except Exception as e:
            msg = json.dumps({
                "thread": main_thread_name,
                "THREAD_LOG_START_PROGRAM": THREAD_LOG_START_PROGRAM,
                "Exception(upload_file_to_server-start_program)": str(e)
            })
            redirect_output(script_name, msg)
            pass

        thread_log_main_scraper_split = THREAD_LOG_MAIN_SCRAPER.rsplit('/', 1)
        remote_thread_log_main_scraper = '{}{}'.format(remote_folder_path, thread_log_main_scraper_split[1])
        try:
            upload_file_to_server(THREAD_LOG_MAIN_SCRAPER, remote_thread_log_main_scraper)
            msg = json.dumps({
                "thread": main_thread_name,
                "THREAD_LOG_MAIN_SCRAPER": THREAD_LOG_MAIN_SCRAPER,
                "uploaded log": "success"
            })
            redirect_output(script_name, msg)
        except Exception as e:
            msg = json.dumps({
                "thread": main_thread_name,
                "THREAD_LOG_MAIN_SCRAPER": THREAD_LOG_MAIN_SCRAPER,
                "Exception(upload_file_to_server-main_scraper)": str(e)
            })
            redirect_output(script_name, msg)
            pass

        """ Delete thread logs from VM """
        # @TODO: CHECK DOES FILES REMOVED FROM "mnt" ARE ALSO REMOVED FROM VM's
        remove_file_if_exist(THREAD_LOG_START_PROGRAM)  # @TODO: UNCOMMENT AFTER TEST
        remove_file_if_exist(THREAD_LOG_MAIN_SCRAPER)  # @TODO: UNCOMMENT AFTER TEST

        """ WORK DONE """
        current_utc_datetime = get_current_utc_date_or_datetime()
        tt = str(datetime.timedelta(seconds=time.time() - st))
        msg = json.dumps({
            "thread": main_thread_name,
            "success_cause": "work_done",
            "failed_lst": len(failed_lst),
            "tt": tt,
            "utc": current_utc_datetime
        })
        redirect_output(script_name, msg)


st = time.time()
script_name = os.path.basename(__file__).rsplit('.', 1)[0]

workQueue = queue.Queue()
queueLock = threading.Lock()

done_q_lst = list()
failed_q_lst = list()

scrapers_speed = {}
scrapers_speed.update({
    "henryschein": "0",
    "dd": "0",
    "dental_sky": "0",
    "next_dental": "0",
    "kent_express": "0"
})  # @TODO: DELETE AFTER TEST


def main():
    o = StartProgram()
    o.run()


if __name__ == '__main__':
    main()
