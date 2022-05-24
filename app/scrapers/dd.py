import random
import datetime
import time
import json

from app.util import make_short_pause, make_medium_pause, make_long_pause, \
    get_current_utc_timestamp, \
    get_current_utc_date_or_datetime, redirect_output
from app.config.cfg_dd import CLIENT_CRED_LST, MAX_THREADS, DRIVER
from app.config.config import logo_img_link_dd, product_name_color, price_color, btn_color


class DD:
    scraper_driver = DRIVER
    scraper_max_threads = MAX_THREADS

    def login_to_website(self, driver, st, t_name, q, q_item, done_q_lst, failed_q_lst, items_for_scraping_len, script_name):
        client_cred = random.choice(CLIENT_CRED_LST)
        CLIENT_USERNAME = client_cred["username"]
        CLIENT_PWD = client_cred["password"]

        """ Login """
        website_url = 'https://www.ddgroup.com/'
        driver.get(website_url)
        make_short_pause()

        btn_el = driver.find_element_by_css_selector('div.login-popup-container button')
        btn_el.click()
        make_short_pause()

        # form_el = driver.find_element_by_css_selector('form[action="/dentalloginpage/login/"]')
        form_el = driver.find_element_by_css_selector('div#login form')

        """ Username """
        username_el = form_el.find_element_by_css_selector('input[name="FormModel.Username"]')
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
        pwd_el = form_el.find_element_by_css_selector('input[name="FormModel.Password"]')
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
        form_el.find_element_by_css_selector('button[type="submit"]').click()
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

        product_name, product_price, stock_status = None, None, None
        try:
            driver.get(product_url)

            try:
                product_name = driver.find_element_by_css_selector('h1.product-title').text
                product_name = product_name.replace("'", "")
                product_name = product_name.strip()
                product_name = product_name.replace('\n', '')
                product_name = product_name.replace('\\n', '')
            except:
                pass

            try:
                t1 = driver.find_element_by_css_selector('h3.product-base-price').text
                product_price = t1.replace('Catalogue Price:', '').strip()
                product_price = product_price.replace('\n', '')
                product_price = product_price.replace('\\n', '')
            except:
                pass

            try:
                stock_status = driver.find_element_by_css_selector('p.stock-status').text
            except:
                pass
        except:
            pass
        if not product_price or product_price is None:
            return None
        product_dict = {
            'time_data_is_fetched': time_data_is_fetched,
            'product_id': product_id,
            'logo_img_link': logo_img_link_dd,
            'product_name_color': product_name_color,
            'product_name': product_name,
            'price_color': price_color,
            'price': product_price,
            'lowest_price': '',
            'btn_url': product_url,
            'btn_color': btn_color,
            'in_stock': stock_status
        }
        return product_dict
