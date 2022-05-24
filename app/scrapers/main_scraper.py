import os
import sys

import time
import datetime
import random
import threading
import queue
import json
from app.util import get_current_utc_date_or_datetime, redirect_output, \
    get_firefox, get_chrome, \
    query_data_from_psql, update_data_into_psql, \
    make_short_pause
from app.config.config import psql_dental_table_name, MAX_ATTEMPTS_URL_ERROR

from .henryschein import HenrySchein
from .dd import DD
from .dental_sky import DentalSky
from .next_dental import NextDental
from .kent_express import KentExpress


class MainScraper:
    def single_thread(self, q, t_name, scraper_obj, items_for_scraping_len, done_q_lst, failed_q_lst):
        driver = None
        logged_in = False
        while not q.empty():
            # queueLock.acquire()
            q_item = q.get()
            current_utc_datetime = get_current_utc_date_or_datetime()
            tt = str(datetime.timedelta(seconds=time.time() - st))
            msg = json.dumps({
                "thread": t_name,
                "msg": "get_q_item",
                "q": q_item,
                "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
                "qsize": q.qsize(),
                "tt": tt,
                "utc": current_utc_datetime
            })
            redirect_output(script_name, msg)
            # queueLock.release()

            """ Do work here """
            product_id = q_item['product_id']
            product_url = q_item['product_url']

            """ We must get "attempts" live from DB """
            # sql = """SELECT * FROM {table_name} WHERE product_url = '{product_url}'""".format(table_name=psql_dental_table_name, product_url=product_url)
            # attempts = query_data_from_psql(sql, fetch_one=True)[2]

            """ Get driver if is None """
            open_driver_pass = True
            if not driver or driver is None:
                open_driver_pass = False
                # queueLock.acquire()
                open_driver_attempt = 0
                while not driver and open_driver_attempt < max_driver_attempts:
                    open_driver_attempt += 1
                    current_utc_datetime = get_current_utc_date_or_datetime()
                    tt = str(datetime.timedelta(seconds=time.time() - st))
                    msg = json.dumps({
                        "thread": t_name,
                        "msg": "opening_driver",
                        "attempts": "{}/{}".format(open_driver_attempt, max_driver_attempts),
                        "q": q_item,
                        "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
                        "qsize": q.qsize(),
                        "tt": tt,
                        "utc": current_utc_datetime
                    })
                    redirect_output(script_name, msg)
                    try:
                        if scraper_obj().scraper_driver == 'firefox':
                            driver = get_firefox()
                        else:
                            driver = get_chrome()
                        open_driver_pass = True
                    except Exception as e:
                        current_utc_datetime = get_current_utc_date_or_datetime()
                        tt = str(datetime.timedelta(seconds=time.time() - st))
                        msg = json.dumps({
                            "thread": t_name,
                            "msg": "error: driver - {}/{}".format(open_driver_attempt + 1, max_driver_attempts),
                            "Exception(open_driver)": str(e),
                            "q": q_item,
                            "qsize": q.qsize(),
                            "ERROR": "total_result",
                            "tt": tt,
                            "utc": current_utc_datetime
                        })
                        redirect_output(script_name, msg)
                        continue
                # queueLock.release()
            if not open_driver_pass:
                current_utc_datetime = get_current_utc_date_or_datetime()
                tt = str(datetime.timedelta(seconds=time.time() - st))
                msg = json.dumps({
                    "thread": t_name,
                    "msg": "error: driver",
                    "q": q_item,
                    "qsize": q.qsize(),
                    "ERROR": "total_result",
                    "tt": tt,
                    "utc": current_utc_datetime
                })
                redirect_output(script_name, msg)
                return {'STATUS': 'ERROR', 'ERROR': 'driver'}

            current_utc_datetime = get_current_utc_date_or_datetime()
            tt = str(datetime.timedelta(seconds=time.time() - st))
            msg = json.dumps({
                "thread": t_name,
                "msg": "driver_opened_successfully",
                "q": q_item,
                "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
                "qsize": q.qsize(),
                "tt": tt,
                "utc": current_utc_datetime
            })
            redirect_output(script_name, msg)

            """ Log in """
            if not logged_in:
                try:
                    """ Login """
                    # scraper_obj().login_to_website(driver)
                    login_status = scraper_obj().login_to_website(driver, st, t_name, q, q_item, done_q_lst, failed_q_lst, items_for_scraping_len, script_name)
                    if login_status:
                        logged_in = True
                    current_utc_datetime = get_current_utc_date_or_datetime()
                    tt = str(datetime.timedelta(seconds=time.time() - st))
                    msg = json.dumps({
                        "thread": t_name,
                        "msg": "login_status: {}".format(str(login_status)),
                        "q": q_item,
                        "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
                        "qsize": q.qsize(),
                        "tt": tt,
                        "utc": current_utc_datetime
                    })
                    redirect_output(script_name, msg)
                except Exception as e:
                    logged_in = False
                    if driver:
                        driver.close()
                        driver = None

                    """ We must get "attempts" live from DB """
                    sql = """SELECT * FROM {table_name} WHERE product_url = '{product_url}'""".format(table_name=psql_dental_table_name, product_url=product_url)
                    attempts = query_data_from_psql(sql, fetch_one=True)[2]
                    if attempts + 1 > int(MAX_ATTEMPTS_URL_ERROR):
                        failed_q_lst.append('c')
                        update_data = {'url_error': True}
                        update_data_into_psql(psql_dental_table_name, update_data, 'product_url', product_url)
                        # logged_in = False
                        # if driver:
                        #     driver.close()
                        #     driver = None
                    else:
                        """ ADD +1 TO "attempts" """
                        update_data = {'attempts': attempts + 1}
                        update_data_into_psql(psql_dental_table_name, update_data, 'product_url', product_url)
                        # q.put(q_item)

                    current_utc_datetime = get_current_utc_date_or_datetime()
                    tt = str(datetime.timedelta(seconds=time.time() - st))
                    msg = json.dumps({
                        "thread": t_name,
                        "status": "failed login",
                        "Exception(logged_in)": str(e),
                        "q": q_item,
                        "attempts": attempts,
                        "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
                        "qsize": q.qsize(),
                        "tt": tt,
                        "utc": current_utc_datetime
                    })
                    redirect_output(script_name, msg)
                    q.task_done()
                    # continue

            """ Get product data """
            try:
                product_data = scraper_obj().get_product_data(driver, product_id, product_url)
                if product_data:
                    """ Update data in DB """
                    product_data_formatted = json.dumps(product_data)
                    update_data = {'product_data': product_data_formatted, 'attempts': 0, 'status_done': True, 'url_error': False}
                    update_status = update_data_into_psql(psql_dental_table_name, update_data, 'product_url', product_url)
                    if update_status is None:
                        status = "failed update in db"

                        """ We must get "attempts" live from DB """
                        sql = """SELECT * FROM {table_name} WHERE product_url = '{product_url}'""".format(table_name=psql_dental_table_name, product_url=product_url)
                        attempts = query_data_from_psql(sql, fetch_one=True)[2]
                        if attempts + 1 > int(MAX_ATTEMPTS_URL_ERROR):
                            failed_q_lst.append('c')
                            update_data = {'url_error': True}
                            update_data_into_psql(psql_dental_table_name, update_data, 'product_url', product_url)
                            logged_in = False
                            # if driver:
                            #     driver.close()
                            #     driver = None
                        else:
                            """ ADD +1 TO "attempts" """
                            update_data = {'attempts': attempts + 1}
                            update_data_into_psql(psql_dental_table_name, update_data, 'product_url', product_url)
                            # q.put(q_item)
                    else:
                        status = "success"
                        attempts = 0
                        done_q_lst.append('c')
                else:
                    status = "no product_data"

                    """ We must get "attempts" live from DB """
                    sql = """SELECT * FROM {table_name} WHERE product_url = '{product_url}'""".format(table_name=psql_dental_table_name, product_url=product_url)
                    attempts = query_data_from_psql(sql, fetch_one=True)[2]
                    if attempts + 1 > int(MAX_ATTEMPTS_URL_ERROR):
                        failed_q_lst.append('c')
                        update_data = {'url_error': True}
                        update_data_into_psql(psql_dental_table_name, update_data, 'product_url', product_url)
                        # logged_in = False
                        # if driver:
                        #     driver.close()
                        #     driver = None
                    else:
                        """ ADD +1 TO "attempts" """
                        update_data = {'attempts': attempts + 1}
                        update_data_into_psql(psql_dental_table_name, update_data, 'product_url', product_url)
                        # q.put(q_item)
            except Exception as e:
                """ We must get "attempts" live from DB """
                sql = """SELECT * FROM {table_name} WHERE product_url = '{product_url}'""".format(table_name=psql_dental_table_name, product_url=product_url)
                attempts = query_data_from_psql(sql, fetch_one=True)[2]
                if attempts + 1 > int(MAX_ATTEMPTS_URL_ERROR):
                    failed_q_lst.append('c')
                    update_data = {'url_error': True}
                    update_data_into_psql(psql_dental_table_name, update_data, 'product_url', product_url)
                    logged_in = False
                    if driver:
                        driver.close()
                        driver = None
                else:
                    """ ADD +1 TO "attempts" """
                    update_data = {'attempts': attempts + 1}
                    update_data_into_psql(psql_dental_table_name, update_data, 'product_url', product_url)
                    # q.put(q_item)

                current_utc_datetime = get_current_utc_date_or_datetime()
                tt = str(datetime.timedelta(seconds=time.time() - st))
                msg = json.dumps({
                    "thread": t_name,
                    "msg": "failed product_data",
                    "status": "Exception(product_data): {}".format(str(e)),
                    "q": q_item,
                    "attempts": attempts,
                    "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
                    "qsize": q.qsize(),
                    "tt": tt,
                    "utc": current_utc_datetime
                })
                redirect_output(script_name, msg)
                q.task_done()
                continue

            """ Jobs done """
            current_utc_datetime = get_current_utc_date_or_datetime()
            tt = str(datetime.timedelta(seconds=time.time() - st))
            msg = json.dumps({
                "thread": t_name,
                "msg": "jobs_done",
                "status": status,
                "q": q_item,
                "attempts": attempts,
                "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
                "qsize": q.qsize(),
                "tt": tt,
                "utc": current_utc_datetime
            })
            redirect_output(script_name, msg)
            q.task_done()

        """ Remove driver """
        if driver:
            driver.close()

        # try:
        #     queueLock.release()
        # except:
        #     pass

    def start_thread(self, q, t_name, scraper_obj, items_for_scraping_len, done_q_lst, failed_q_lst):
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
            self.single_thread(q, t_name, scraper_obj, items_for_scraping_len, done_q_lst, failed_q_lst)
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

    def prepare_data_for_queue(self, like_url):
        sql = """SELECT * FROM {table_name} WHERE status_done is false AND url_error is false AND product_url LIKE '%{like_url}%';""".format(table_name=psql_dental_table_name, like_url=like_url)
        try:
            query_result = query_data_from_psql(sql, fetch_all=True)
            query_result_formatted = [
                {
                    'product_id': query_result[i][0],
                    'product_url': query_result[i][1],
                    'attempts': query_result[i][2],
                    'status_done': query_result[i][3]
                }
                for i in range(len(query_result))
            ]
            return query_result_formatted
        except Exception as e:
            print('Exception(prepare_data_for_queue): {}'.format(e))
            return None

    def run(self, scraper_name, like_url):
        done_q_lst = list()
        failed_q_lst = list()

        """ DEFINING "workQueue" MUST BE INSIDE "run" METHOD, OTHERWISE QUEUE WILL BE MESSED UP FROM ALL SUB-THREADS """
        workQueue = queue.Queue()

        if scraper_name == 'henryschein':
            scraper_obj = HenrySchein
        elif scraper_name == 'dd':
            scraper_obj = DD
        elif scraper_name == 'dental_sky':
            scraper_obj = DentalSky
        elif scraper_name == 'next_dental':
            scraper_obj = NextDental
        elif scraper_name == 'kent_express':
            scraper_obj = KentExpress
        else:
            sys.exit(1)

        main_thread_name = "T-{}-m".format(scraper_name)

        data_for_queue = True
        while data_for_queue:
            """ PREPARE DATA FOR QUEUE """
            data_for_queue = None
            while data_for_queue is None:
                data_for_queue = self.prepare_data_for_queue(like_url)
                make_short_pause()

            """ Copy data to template list """
            items_for_scraping = data_for_queue.copy()
            """ Shuffle list """
            random.shuffle(items_for_scraping)
            items_for_scraping_len = len(items_for_scraping)
            """ Set max number of threads """
            max_threads = int(scraper_obj().scraper_max_threads)
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
                t_name = "T-{}-{}".format(scraper_name, i_thread + 1)
                t = threading.Thread(target=self.start_thread, args=(workQueue, t_name, scraper_obj, items_for_scraping_len, done_q_lst, failed_q_lst))
                t.daemon = True
                threads.append(t)
            [thread.start() for thread in threads]
            [thread.join() for thread in threads]
            done_q_lst = list()
            failed_q_lst = list()
            """ TURN DONE """
            current_utc_datetime = get_current_utc_date_or_datetime()
            tt = str(datetime.timedelta(seconds=time.time() - st))
            msg = json.dumps({
                "thread": main_thread_name,
                "success_cause": "turn_done",
                "tt": tt,
                "utc": current_utc_datetime
            })
            redirect_output(script_name, msg)

        """ WORK DONE """
        current_utc_datetime = get_current_utc_date_or_datetime()
        tt = str(datetime.timedelta(seconds=time.time() - st))
        msg = json.dumps({
            "thread": main_thread_name,
            "success_cause": "work_done",
            "tt": tt,
            "utc": current_utc_datetime
        })
        redirect_output(script_name, msg)


st = time.time()
script_name = os.path.basename(__file__).rsplit('.', 1)[0]

queueLock = threading.Lock()

max_driver_attempts = 5
