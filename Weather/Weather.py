# encode:utf-8
'''
2018-04-08 爬取杭州2017年的历史天气
crawl Hangzhou's historical weather of 2017
output example:
2017-01-01,00:00,Mist,6буC,2 km/h,93%,1028 hPa
'''

import requests
from bs4 import BeautifulSoup
from lxml import etree
import datetime

url = 'https://en.tutiempo.net/records/zshc'
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
"Accept": "text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}

postdata = {
    'date':'8-2-2017' # example
}
# from 2017.01.01 to 2017.12.31
cur_day = datetime.datetime(year=2016, month=12, day=31)
with open('weather.csv', 'w', newline='\n') as fout:
    for i in range(365):
        cur_day += datetime.timedelta(days=1)
        postdata['date'] = "%s-%s-%s" % (cur_day.day, cur_day.month, cur_day.year)
        date = str(cur_day.date())
        print(date)
        html_data = requests.post(url, data=postdata, headers=headers)
        selector = etree.HTML(html_data.text)
        # //*[@id="HistoricosData"]/div/table/tbody/tr[3]
        links = selector.xpath('//*[@id="HistoricosData"]/div/table/tbody')
        Soup = BeautifulSoup(etree.tostring(links[0]), 'lxml')
        for line in Soup.find_all('tr'):
            result = line.select('td')
            if len(result) == 0:
                continue
            Hour = result[0].text
            WC = result[1].text
            Temp = result[2].text
            Wind = result[3].text
            Hum = result[4].text
            Pressure = result[5].text
            data = "%s,%s,%s,%s,%s,%s,%s\n" % (date, Hour, WC, Temp, Wind, Hum, Pressure)
            fout.write(data)