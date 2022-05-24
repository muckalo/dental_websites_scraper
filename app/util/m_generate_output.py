from app.util import query_data_from_psql, get_current_utc_date_or_datetime
from app.config.config import psql_dental_table_name


def generate_output():
    sql = """SELECT product_id FROM {table_name} WHERE status_done is true;""".format(table_name=psql_dental_table_name)
    query_result = query_data_from_psql(sql, fetch_all=True)
    query_result_formatted = [query_result[i][0] for i in range(len(query_result))]
    unique_product_ids = list(set(query_result_formatted))
    # unique_product_ids = unique_product_ids[:100]  # @TODO: DELETE AFTER TEST
    output_data = [['product_id', 'html_code']]

    for i_product_id in range(len(unique_product_ids)):
        product_id = unique_product_ids[i_product_id]
        sql = """SELECT * FROM {table_name} WHERE product_id = '{product_id}';""".format(table_name=psql_dental_table_name, product_id=product_id)
        query_result = query_data_from_psql(sql, fetch_all=True)
        products_data = [
            {
                'product_id': query_result[i][0],
                'product_url': query_result[i][1],
                'product_data': query_result[i][5],
                'status_done': query_result[i][3]
            }
            for i in range(len(query_result))
        ]
        # products_data = products_data[:10000]  # @TODO: DELETE AFTER TEST

        henryschein_product_name, henryschein_product_price, henryschein_in_stock, henryschein_product_url = None, None, None, None
        dd_product_name, dd_product_price, dd_in_stock, dd_product_url = None, None, None, None
        ds_product_name, ds_product_price, ds_in_stock, ds_product_url = None, None, None, None
        nd_product_name, nd_product_price, nd_in_stock, nd_product_url = None, None, None, None
        ke_product_name, ke_product_price, ke_in_stock, ke_product_url = None, None, None, None
        for product_dict in products_data:
            if product_dict['product_id'] != product_id:
                continue
            product_url = product_dict['product_url']
            product_data = product_dict['product_data']
            if not product_data:
                continue
            if 'www.henryschein.co.uk' in product_url:
                henryschein_product_name = product_data['product_name']
                henryschein_product_price = product_data['price']
                henryschein_in_stock = product_data['in_stock']
                henryschein_product_url = product_data['btn_url']
            elif 'www.ddgroup.com' in product_url:
                dd_product_name = product_data['product_name']
                dd_product_price = product_data['price']
                dd_in_stock = product_data['in_stock']
                dd_product_url = product_data['btn_url']
            elif 'www.dentalsky.com' in product_url:
                ds_product_name = product_data['product_name']
                ds_product_price = product_data['price']
                ds_in_stock = product_data['in_stock']  # IN STOCK
                ds_product_url = product_data['btn_url']
            elif 'www.nextdental.com' in product_url:
                nd_product_name = product_data['product_name']
                nd_product_price = product_data['price']
                nd_in_stock = product_data['in_stock']
                nd_product_url = product_data['btn_url']
            elif 'www.kentexpress.co.uk' in product_url:
                ke_product_name = product_data['product_name']
                ke_product_price = product_data['price']
                ke_in_stock = product_data['in_stock']
                ke_product_url = product_data['btn_url']

        """ Find lowest price """
        prices = []
        if henryschein_product_price:
            henryschein_product_price = henryschein_product_price.replace('£', '')
            henryschein_product_price = henryschein_product_price.replace(',', '')
            henryschein_product_price = henryschein_product_price.strip()
            henryschein_product_price = henryschein_product_price.replace(' ', '')
            henryschein_product_price = henryschein_product_price.replace('\n', '')
            henryschein_product_price = henryschein_product_price.replace('\\n', '')
            try:
                price = float(henryschein_product_price.replace('£', ''))
                prices.append(price)
            except:
                pass
        if dd_product_price:
            dd_product_price = dd_product_price.replace('£', '')
            dd_product_price = dd_product_price.replace(',', '')
            dd_product_price = dd_product_price.strip()
            dd_product_price = dd_product_price.replace(' ', '')
            dd_product_price = dd_product_price.replace('\n', '')
            dd_product_price = dd_product_price.replace('\\n', '')
            try:
                price = float(dd_product_price.replace('£', ''))
                prices.append(price)
            except:
                pass
        if ds_product_price:
            ds_product_price = ds_product_price.replace('£', '')
            ds_product_price = ds_product_price.replace(',', '')
            ds_product_price = ds_product_price.strip()
            ds_product_price = ds_product_price.replace(' ', '')
            ds_product_price = ds_product_price.replace('\n', '')
            ds_product_price = ds_product_price.replace('\\n', '')
            try:
                price = float(ds_product_price.replace('£', ''))
                prices.append(price)
            except:
                pass
        if nd_product_price:
            nd_product_price = nd_product_price.replace('£', '')
            nd_product_price = nd_product_price.replace(',', '')
            nd_product_price = nd_product_price.strip()
            nd_product_price = nd_product_price.replace(' ', '')
            nd_product_price = nd_product_price.replace('\n', '')
            nd_product_price = nd_product_price.replace('\\n', '')
            try:
                price = float(nd_product_price.replace('£', ''))
                prices.append(price)
            except:
                pass
        if ke_product_price:
            ke_product_price = ke_product_price.replace('£', '')
            ke_product_price = ke_product_price.replace(',', '')
            ke_product_price = ke_product_price.strip()
            ke_product_price = ke_product_price.replace(' ', '')
            ke_product_price = ke_product_price.replace('\n', '')
            ke_product_price = ke_product_price.replace('\\n', '')
            try:
                price = float(ke_product_price.replace('£', ''))
                prices.append(price)
            except:
                pass
        if prices:
            min_price = min(prices)
            min_price = '£{}'.format(min_price)
        else:
            min_price = None

        if min_price and min_price is not None:
            if henryschein_product_price == min_price:
                henryschein_product_price = '{} (lowest price)'.format(henryschein_product_price)
            if dd_product_price == min_price:
                dd_product_price = '{} (lowest price)'.format(dd_product_price)
            if ds_product_price == min_price:
                ds_product_price = '{} (lowest price)'.format(ds_product_price)
            if nd_product_price == min_price:
                nd_product_price = '{} (lowest price)'.format(nd_product_price)
            if ke_product_price == min_price:
                ke_product_price = '{} (lowest price)'.format(ke_product_price)

        """ Generate scrapers (rows) HTML code """
        html_code_henryschein = None
        if henryschein_product_price and henryschein_product_price is not None:
            henryschein_product_price = '£{}'.format(henryschein_product_price)
            try:
                henryschein_in_stock_formatted = henryschein_in_stock.lower().strip()
            except:
                henryschein_in_stock_formatted = henryschein_in_stock
            if henryschein_in_stock is None:
                henryschein_in_stock = 'Stock Not Shown'
            elif henryschein_in_stock_formatted == 'in stock':
                henryschein_in_stock = 'In Stock'
            elif henryschein_in_stock_formatted == 'out of stock':
                henryschein_in_stock = 'Out of Stock'
            html_code_henryschein = '''
                <tr>
                    <td><span style="color: #00940a;"><img class="aligncenter size-full wp-image-141923" src="https://dentalsupply.uk/wp-content/uploads/2021/10/HenrySchein-1.jpg" alt="" width="150" height="49" /></span></td>
                    <td><span style="color: #808080;">{henryschein_product_name}</span></td>
                    <td><span style="color:#808080;">{henryschein_product_price}</span></td>
                    <td><span style="color:#00940A;">{henryschein_in_stock}</span></td>
                    <td><span style="color: #808080;">[su_button url="{henryschein_product_url}" target="blank" style="flat" background="#00940A" size="5" radius="round"]Visit[/su_button]</span></td>
                </tr>
            '''.format(henryschein_product_name=henryschein_product_name, henryschein_product_price=henryschein_product_price, henryschein_in_stock=henryschein_in_stock, henryschein_product_url=henryschein_product_url)

        html_code_dd = None
        if dd_product_price and dd_product_price is not None:
            dd_product_price = '£{}'.format(dd_product_price)
            try:
                dd_in_stock_formatted = dd_in_stock.lower().strip()
            except:
                dd_in_stock_formatted = dd_in_stock
            if dd_in_stock is None:
                dd_in_stock = 'Stock Not Shown'
            elif dd_in_stock_formatted == 'in stock':
                dd_in_stock = 'In Stock'
            elif dd_in_stock_formatted == 'out of stock':
                dd_in_stock = 'Out of Stock'
            html_code_dd = '''
                <tr>
                <td><span style="color: #808080;"><img class="aligncenter size-full wp-image-141923" src="https://dentalsupply.uk/wp-content/uploads/2021/10/DD.jpg" alt="" width="150" height="49"></span></td>
                <td><span style="color: #808080;">{dd_product_name}</span></td>
                <td><span style="color:#808080;">{dd_product_price}</span></td>
                <td><span style="color:#E4A255;">{dd_in_stock}</span></td>
                <td><span style="color: #377DFF;">[su_button url="{dd_product_url}" target="blank" style="flat" background="#377DFF" size="5" radius="round"]Visit[/su_button]</span></td>
            </tr>
            '''.format(dd_product_name=dd_product_name, dd_product_price=dd_product_price, dd_in_stock=dd_in_stock, dd_product_url=dd_product_url)

        html_code_ke = None
        if ke_product_price and ke_product_price is not None:
            ke_product_price = '£{}'.format(ke_product_price)
            try:
                ke_in_stock_formatted = ke_in_stock.lower().strip()
            except:
                ke_in_stock_formatted = ke_in_stock
            if ke_in_stock is None:
                ke_in_stock = 'Stock Not Shown'
            elif ke_in_stock_formatted == 'in stock':
                ke_in_stock = 'In Stock'
            elif ke_in_stock_formatted == 'out of stock':
                ke_in_stock = 'Out of Stock'
            html_code_ke = '''
                <tr>
                <td><span style="color: #808080;"><img class="aligncenter size-full wp-image-141923" src="https://dentalsupply.uk/wp-content/uploads/2021/10/KentExpress.jpg" alt="" width="150" height="49"></span></td>
                <td><span style="color: #808080;">{ke_product_name}</span></td>
                <td><span style="color:#808080;">{ke_product_price}</span></td>
                <td><span style="color:#00940A;">{ke_in_stock}</span></td>
                <td><span style="color: #808080;">[su_button url="{ke_product_url}" target="blank" style="flat" background="#377DFF" size="5" radius="round"]Visit[/su_button]</span></td>
            </tr>
            '''.format(ke_product_name=ke_product_name, ke_product_price=ke_product_price, ke_in_stock=ke_in_stock, ke_product_url=ke_product_url)

        html_code_nd = None
        if nd_product_price and nd_product_price is not None:
            nd_product_price = '£{}'.format(nd_product_price)
            try:
                nd_in_stock_formatted = nd_in_stock.lower().strip()
            except:
                nd_in_stock_formatted = nd_in_stock
            if nd_in_stock is None:
                nd_in_stock = 'Stock Not Shown'
            elif nd_in_stock_formatted == 'in stock':
                nd_in_stock = 'In Stock'
            elif nd_in_stock_formatted == 'out of stock':
                nd_in_stock = 'Out of Stock'
            html_code_nd = '''
                <tr>
                <td><span style="color: #808080;"><img class="aligncenter size-full wp-image-141923" src="https://dentalsupply.uk/wp-content/uploads/2021/10/NextDental.jpg" alt="" width="150" height="49"></span</td>
                <td><span style="color: #808080;">{nd_product_name}</span></td>
                <td><span style="color:#808080;">{nd_product_price}</span></td>
                <td><span style="color:#00940A;">{nd_in_stock}</span></td>
                <td><span style="color: #808080;">[su_button url="{nd_product_url}" target="blank" style="flat" background="#377DFF" size="5" radius="round"]Visit[/su_button]</span></td>
            </tr>
            '''.format(nd_product_name=nd_product_name, nd_product_price=nd_product_price, nd_in_stock=nd_in_stock, nd_product_url=nd_product_url)

        html_code_ds = None
        if ds_product_price and ds_product_price is not None:
            ds_product_price = '£{}'.format(ds_product_price)
            try:
                ds_in_stock_formatted = ds_in_stock.lower().strip()
            except:
                ds_in_stock_formatted = ds_in_stock
            if ds_in_stock is None:
                ds_in_stock = 'Stock Not Shown'
            elif ds_in_stock_formatted == 'in stock':
                ds_in_stock = 'In Stock'
            elif ds_in_stock_formatted == 'out of stock':
                ds_in_stock = 'Out of Stock'
            html_code_ds = '''
                <tr>
                <td><span style="color: #808080;"><img class="aligncenter size-full wp-image-141923" src="https://dentalsupply.uk/wp-content/uploads/2021/10/DentalSky.jpg" alt="" width="150" height="49"></span></td>
                <td><span style="color: #808080;">{ds_product_name}</span></td>
                <td><span style="color:#808080;">{ds_product_price}</span></td>
                <td><span style="color:#B20A22;">{ds_in_stock}</span></td>
                <td><span style="color: #808080;">[su_button url="{ds_product_url}" target="blank" style="flat" background="#B20A22" size="5" radius="round"]Visit[/su_button]</span></td>
            </tr>
            '''.format(ds_product_name=ds_product_name, ds_product_price=ds_product_price, ds_in_stock=ds_in_stock, ds_product_url=ds_product_url)

        """ Generate start HTML code """
        html_code_start = '''
            [um_loggedin]
            <h1><span style="color: #377dff;">Prices</span></h1>
            [su_table responsive="yes" alternate="yes"]
            <table>
            <tbody>
            
        '''

        """ Generate end HTML code """
        current_utc_datetime = get_current_utc_date_or_datetime(use_format='%d/%m/%Y')
        html_code_end = '''
            
            </tbody>
            </table>
            [/su_table]
            
            <em>All Prices are excluding VAT and shipping. Prices last reviewed and updated on: {current_utc_datetime} GMT</em>
            [/um_loggedin]
            [um_loggedout]
            [mas_static_content id="142033"]
            [/um_loggedout]
        '''.format(current_utc_datetime=current_utc_datetime)

        """ Generate final HTML code """
        html_code = ''''''
        html_code += html_code_start
        if html_code_henryschein:
            html_code += html_code_henryschein
        if html_code_dd:
            html_code += html_code_dd
        if html_code_ke:
            html_code += html_code_ke
        if html_code_nd:
            html_code += html_code_nd
        if html_code_ds:
            html_code += html_code_ds
        html_code += html_code_end

        data = [product_id, html_code]
        output_data.append(data)

    return output_data
