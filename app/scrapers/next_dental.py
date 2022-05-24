import random
import datetime
import time
import json

from app.util import make_short_pause, make_medium_pause, make_long_pause, \
    get_current_utc_timestamp, \
    get_current_utc_date_or_datetime, redirect_output
from app.config.cfg_next_dental import CLIENT_CRED_LST, MAX_THREADS, DRIVER
from app.config.config import logo_img_link_nd, product_name_color, price_color, btn_color


class NextDental:
    scraper_driver = DRIVER
    scraper_max_threads = MAX_THREADS

    def login_to_website(self, driver, st, t_name, q, q_item, done_q_lst, failed_q_lst, items_for_scraping_len, script_name):
        client_cred = random.choice(CLIENT_CRED_LST)
        CLIENT_USERNAME = client_cred["username"]
        CLIENT_PWD = client_cred["password"]

        """ Login """
        login_url = 'https://www.nextdental.com/account.aspx'
        driver.get(login_url)
        make_short_pause()

        table_el = driver.find_element_by_css_selector('table.login-table-container')

        """ Username """
        username_el = table_el.find_element_by_css_selector('input[type="text"]')
        username_el.clear()
        username_el.send_keys(CLIENT_USERNAME)
        make_short_pause()
        current_utc_datetime = get_current_utc_date_or_datetime()
        tt = str(datetime.timedelta(seconds=time.time() - st))
        msg = json.dumps({
            "thread": t_name,
            "msg": "username_done",
            "q": q_item,
            "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
            "qsize": q.qsize(),
            "tt": tt,
            "utc": current_utc_datetime
        })
        redirect_output(script_name, msg)

        """ Password """
        pwd_el = table_el.find_element_by_css_selector('input[type="password"]')
        pwd_el.clear()
        pwd_el.send_keys(CLIENT_PWD)
        make_short_pause()
        current_utc_datetime = get_current_utc_date_or_datetime()
        tt = str(datetime.timedelta(seconds=time.time() - st))
        msg = json.dumps({
            "thread": t_name,
            "msg": "password_done",
            "q": q_item,
            "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
            "qsize": q.qsize(),
            "tt": tt,
            "utc": current_utc_datetime
        })
        redirect_output(script_name, msg)

        """ Submit """
        driver.find_element_by_css_selector('a.loginbutton').click()
        make_long_pause()
        current_utc_datetime = get_current_utc_date_or_datetime()
        tt = str(datetime.timedelta(seconds=time.time() - st))
        msg = json.dumps({
            "thread": t_name,
            "msg": "submit_done",
            "q": q_item,
            "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
            "qsize": q.qsize(),
            "tt": tt,
            "utc": current_utc_datetime
        })
        redirect_output(script_name, msg)

        return True

    def get_product_data(self, driver, product_id, product_url):
        time_data_is_fetched = get_current_utc_timestamp()

        product_name, product_price = None, None
        try:
            driver.get(product_url)

            try:
                h2_el = driver.find_element_by_css_selector('div.item-description h2')
                h2_txt = h2_el.text
                t1_txt = h2_el.find_element_by_css_selector('span.product-code').text
                product_name = h2_txt.replace(t1_txt, '').strip()
                product_name = product_name.replace("'", "")
                product_name = product_name.replace('\n', '')
                product_name = product_name.replace('\\n', '')
            except:
                pass

            try:
                product_price = driver.find_element_by_css_selector('span.rrpProductPrice').text
                product_price = product_price.strip()
                product_price = product_price.replace('\n', '')
                product_price = product_price.replace('\\n', '')
            except:
                pass
        except:
            pass
        if not product_price or product_price is None:
            return None
        product_dict = {
            'time_data_is_fetched': time_data_is_fetched,
            'product_id': product_id,
            'logo_img_link': logo_img_link_nd,
            'product_name_color': product_name_color,
            'product_name': product_name,
            'price_color': price_color,
            'price': product_price,
            'lowest_price': '',
            'btn_url': product_url,
            'btn_color': btn_color,
            'in_stock': None
        }
        return product_dict
