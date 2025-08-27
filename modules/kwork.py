from loguru import logger
import requests
import re
import json, json5
import html


class KworkAPI:
    def __init__(self):
        session = json.load(open('modules/session.json', 'r'))
        self.headers = session['headers']
        self.cookies = session['cookies']


    def _get_data(self, page):
        try:
            res = requests.get(f'https://kwork.ru/projects?a=1&price-from=500&price-to=10000&page={page}', headers=self.headers, cookies=self.cookies)
            html = res.text

            with open('fetches/kworks.html', 'w', encoding='utf-8') as f:
                f.write(html)

            data = re.findall(r'window.stateData=(.*?)window.firebaseConfig', html)[0]
            data = json5.loads(data[:-1])

            with open('fetches/data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return data
        
        except Exception as e:
            logger.error(f'Не удалось получить страницу биржи: {e}')
            return None


    def _get_pages(self, data):
        links = data['pagination']['links']
        pages = []
        for link in links:
            try:
                pages.append(int(link["label"]))
            except: pass
        return pages


    def get_orders(self):
        first_data = self._get_data(page=1)
        pages = self._get_pages(data=first_data)
        use_first_data = True

        for page in pages:
            if use_first_data:
                data = first_data
                use_first_data = False
            else:
                data = self._get_data(page)

            orders = data['wantsListData']['pagination']['data']

            for order in orders:
                try:
                    yield {
                        "id": order['id'],
                        "title": order['name'],
                        "description": html.unescape(order['description']),
                        "price": int(float(order['priceLimit'])),
                        "max_price": int(float(order['possiblePriceLimit'])),
                        "offers_count": order['kwork_count'],
                        "last_date": order['wantDates']['dateExpire']
                    }
                    logger.info(f'Получен новый кворк {order['id']}')
                except Exception as e:
                    logger.warning(f'Не удалось спарсить кворк: {e}')
            
            logger.success(f'Все кворки со страницы {page} получены')
        
        logger.success(f'Все кворки получены, последняя страница - {page}')
