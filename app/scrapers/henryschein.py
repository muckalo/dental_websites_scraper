import random
import datetime
import time
import json

from app.util import make_short_pause, make_medium_pause, make_long_pause, \
    get_current_utc_timestamp, \
    get_current_utc_date_or_datetime, redirect_output
from app.config.cfg_henryschine import CLIENT_CRED_LST, MAX_THREADS, DRIVER
from app.config.config import logo_img_link_hs, product_name_color, price_color, btn_color


class HenrySchein:
    scraper_driver = DRIVER
    scraper_max_threads = MAX_THREADS

    def close_ad_popup(self, driver):
        a_el = driver.find_element_by_css_selector('a.dismiss')
        a_el.click()
        make_short_pause()

    def click_deny_for_cookies(self, driver):
        """ Inject javaScript to get "shadowRoot" """
        shadow_section = driver.execute_script("""
            var host = document.getElementById('usercentrics-root');
            var root = host.shadowRoot;
            var avatar = root.querySelectorAll('button[data-testid="uc-deny-all-button"]');
            return avatar;
            """)
        shadow_section_1 = shadow_section[0]
        shadow_section_1.click()
        make_short_pause()

    # def login_to_website(self, driver):
    def login_to_website(self, driver, st, t_name, q, q_item, done_q_lst, failed_q_lst, items_for_scraping_len, script_name):
        client_cred = random.choice(CLIENT_CRED_LST)
        CLIENT_USERNAME = client_cred["username"]
        CLIENT_PWD = client_cred["password"]

        """ Login """
        website_url = 'https://www.henryschein.co.uk/gb-en/dental-gb/Default.aspx?did=dental-gb'
        driver.get(website_url)
        make_short_pause()

        """ Deny cookies """
        try:
            self.click_deny_for_cookies(driver)
            # current_utc_datetime = get_current_utc_date_or_datetime()
            # tt = str(datetime.timedelta(seconds=time.time() - st))
            # msg = json.dumps({
            #     "thread": t_name,
            #     "msg": "clicked_deny_cookies",
            #     "q": q_item,
            #     "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
            #     "qsize": q.qsize(),
            #     "tt": tt,
            #     "utc": current_utc_datetime
            # })
            # redirect_output(script_name, msg)
        except Exception as e:
            # current_utc_datetime = get_current_utc_date_or_datetime()
            # tt = str(datetime.timedelta(seconds=time.time() - st))
            # msg = json.dumps({
            #     "thread": t_name,
            #     "msg": "Exception(click_deny_for_cookies): {}".format(str(e)),
            #     "q": q_item,
            #     "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
            #     "qsize": q.qsize(),
            #     "tt": tt,
            #     "utc": current_utc_datetime
            # })
            # redirect_output(script_name, msg)
            pass

        """ Close Ad Pop-up """
        try:
            self.close_ad_popup(driver)
        except Exception as e:
            # current_utc_datetime = get_current_utc_date_or_datetime()
            # tt = str(datetime.timedelta(seconds=time.time() - st))
            # msg = json.dumps({
            #     "thread": t_name,
            #     "msg": "Exception(close_ad_popup): {}".format(str(e)),
            #     "q": q_item,
            #     "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
            #     "qsize": q.qsize(),
            #     "tt": tt,
            #     "utc": current_utc_datetime
            # })
            # redirect_output(script_name, msg)
            pass

        """ Click button "Login" """
        login_attempt = 0
        while True:
            login_attempt += 1
            if login_attempt > 3:
                return False

            driver.refresh()
            # current_utc_datetime = get_current_utc_date_or_datetime()
            # tt = str(datetime.timedelta(seconds=time.time() - st))
            # msg = json.dumps({
            #     "thread": t_name,
            #     "msg": "refresh_driver",
            #     "q": q_item,
            #     "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
            #     "qsize": q.qsize(),
            #     "tt": tt,
            #     "utc": current_utc_datetime
            # })
            # redirect_output(script_name, msg)

            """
            # {"thread": "T-henryschein-1", "status": "failed login",
            # "Exception(logged_in)":
            # "Message: Element <input id=\"ctl00_ucHeader_ucSessionBar_ucLogin_txtLogonName\" class=\"hs-input username\" name=\"ctl00$ucHeader$ucSessionBar$ucLogin$txtLogonName\" type=\"text\">
            # could not be scrolled into view\n",
            # "q": {"product_id": "DS/3764", "product_url": "https://www.henryschein.co.uk/gb-en/dental-gb/p/handpieces/adaptors-and-couplings/quick-coupling-with-light/1894588", "attempts": 0, "status_done": false}, "attempts": 0, "q_done": "0/0/18862", "qsize": 18833, "tt": "0:00:54.342837", "utc": "2022-02-12 18:26:00"}
            """

            btn_clicked = False
            els = driver.find_elements_by_css_selector('div.anonymous.pad-left div.hs-login a')
            # current_utc_datetime = get_current_utc_date_or_datetime()
            # tt = str(datetime.timedelta(seconds=time.time() - st))
            # msg = json.dumps({
            #     "thread": t_name,
            #     "msg": "els: {}".format(len(els)),
            #     "q": q_item,
            #     "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
            #     "qsize": q.qsize(),
            #     "tt": tt,
            #     "utc": current_utc_datetime
            # })
            # redirect_output(script_name, msg)
            for el in els:
                try:
                    el.find_element_by_css_selector('i')
                    el.click()
                    btn_clicked = True
                    make_short_pause()
                    # current_utc_datetime = get_current_utc_date_or_datetime()
                    # tt = str(datetime.timedelta(seconds=time.time() - st))
                    # msg = json.dumps({
                    #     "thread": t_name,
                    #     "msg": "clicked: {}/{}".format(els.index(el) + 1, len(els)),
                    #     "q": q_item,
                    #     "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
                    #     "qsize": q.qsize(),
                    #     "tt": tt,
                    #     "utc": current_utc_datetime
                    # })
                    # redirect_output(script_name, msg)
                    break
                except Exception as e:
                    # current_utc_datetime = get_current_utc_date_or_datetime()
                    # tt = str(datetime.timedelta(seconds=time.time() - st))
                    # msg = json.dumps({
                    #     "thread": t_name,
                    #     "msg": "Exception(click): {}/{} - {}".format(els.index(el) + 1, len(els), str(e)),
                    #     "q": q_item,
                    #     "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
                    #     "qsize": q.qsize(),
                    #     "tt": tt,
                    #     "utc": current_utc_datetime
                    # })
                    # redirect_output(script_name, msg)
                    pass
            if not btn_clicked:
                # current_utc_datetime = get_current_utc_date_or_datetime()
                # tt = str(datetime.timedelta(seconds=time.time() - st))
                # msg = json.dumps({
                #     "thread": t_name,
                #     "msg": "not_btn_clicked",
                #     "q": q_item,
                #     "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
                #     "qsize": q.qsize(),
                #     "tt": tt,
                #     "utc": current_utc_datetime
                # })
                # redirect_output(script_name, msg)
                break

            """ Username """
            # username_el = driver.find_elements_by_css_selector('input.hs-input.username')[1]
            # username_el = driver.find_elements_by_css_selector('input.hs-input.username')[-1]
            username_el = driver.find_element_by_css_selector('div.anonymous.pad-left div.hs-login input.hs-input.username')
            username_el.clear()
            username_el.send_keys(CLIENT_USERNAME)
            make_short_pause()
            # current_utc_datetime = get_current_utc_date_or_datetime()
            # tt = str(datetime.timedelta(seconds=time.time() - st))
            # msg = json.dumps({
            #     "thread": t_name,
            #     "msg": "username_done",
            #     "q": q_item,
            #     "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
            #     "qsize": q.qsize(),
            #     "tt": tt,
            #     "utc": current_utc_datetime
            # })
            # redirect_output(script_name, msg)

            """ Password """
            # pwd_el = driver.find_elements_by_css_selector('input.hs-input.password')[1]
            # pwd_el = driver.find_elements_by_css_selector('input.hs-input.password')[-1]
            pwd_el = driver.find_element_by_css_selector('div.anonymous.pad-left div.hs-login input.hs-input.password')
            pwd_el.clear()
            pwd_el.send_keys(CLIENT_PWD)
            make_short_pause()
            # current_utc_datetime = get_current_utc_date_or_datetime()
            # tt = str(datetime.timedelta(seconds=time.time() - st))
            # msg = json.dumps({
            #     "thread": t_name,
            #     "msg": "password_done",
            #     "q": q_item,
            #     "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
            #     "qsize": q.qsize(),
            #     "tt": tt,
            #     "utc": current_utc_datetime
            # })
            # redirect_output(script_name, msg)

            """ Submit """
            # p_el = pwd_el.find_element_by_xpath('..').find_element_by_xpath('..')
            # p_el.find_element_by_css_selector('button').click()
            driver.find_element_by_css_selector('div#ctl00_ucHeader_ucSessionBar_ucLogin_divLogin button').click()
            make_long_pause()
            # current_utc_datetime = get_current_utc_date_or_datetime()
            # tt = str(datetime.timedelta(seconds=time.time() - st))
            # msg = json.dumps({
            #     "thread": t_name,
            #     "msg": "submit_done",
            #     "q": q_item,
            #     "q_done": "{}/{}/{}".format(len(done_q_lst), len(failed_q_lst), items_for_scraping_len),
            #     "qsize": q.qsize(),
            #     "tt": tt,
            #     "utc": current_utc_datetime
            # })
            # redirect_output(script_name, msg)

        return True

    def get_product_data(self, driver, product_id, product_url):
        time_data_is_fetched = get_current_utc_timestamp()
        product_name, product_price = None, None
        try:
            driver.get(product_url)
            div_details_el = driver.find_element_by_css_selector('div.details')

            try:
                t1 = div_details_el.find_element_by_css_selector('h2')
                t1_txt = t1.text
                t2_txt = t1.find_element_by_css_selector('small').text
                product_name = t1_txt.replace(t2_txt, '').strip()
                product_name = product_name.replace("'", "")
                product_name = product_name.replace('\n', '')
                product_name = product_name.replace('\\n', '')
            except:
                pass

            try:
                # product_price_t1 = div_details_el.find_element_by_css_selector('div.product-price').text
                product_price_t1 = div_details_el.find_element_by_css_selector('div.product-price span.amount').text
                product_price_t2 = product_price_t1.split('£')[1]
                product_price = '£{}'.format(product_price_t2)
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
            'logo_img_link': logo_img_link_hs,
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
