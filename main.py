import pandas as pd
import requests
from bs4 import BeautifulSoup

pd.set_option('colheader_justify', 'center')

cookies = {'calendar-importance': '3', 'ASP.NET_SessionId': 'gadirjyodeqlil34zneb5kua', 'TEServer': 'TEIIS2',
		   'cal-timezone-offset': '480', }

headers = {'authority': 'tradingeconomics.com',
		   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		   'accept-language': 'en', 'cache-control': 'max-age=0',
		   # 'cookie': 'calendar-importance=3; ASP.NET_SessionId=gadirjyodeqlil34zneb5kua; TEServer=TEIIS2; cal-timezone-offset=480',
		   'dnt': '1', 'referer': 'https://tradingeconomics.com/calendar',
		   'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"', 'sec-ch-ua-mobile': '?0',
		   'sec-ch-ua-platform': '"Linux"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
		   'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
		   'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46', }

response = requests.get('https://tradingeconomics.com/calendar', cookies=cookies, headers=headers)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

# print(soup.prettify())
dates = set()
count = 0
for header in soup.find('table', id='calendar').find_all('thead', {"class": "table-header"}):
	for th in header.find_all('th'):
		if th.string is not None:
			if count % 5 == 0:
				dates.add(th.string.strip())
			count += 1

# print(dates)
unique_dates = dates
count = 0
current_date = ''
output_dict = {}
row = 0
for rows in soup.find('table', id='calendar').find_all('tr'):
	for tag in rows.find_all():
		if count == 13:
			count = 0
			row += 1
			output_dict[current_date][row] = []
		if tag.text.strip() in unique_dates:
			current_date = tag.text.strip()
			row = 0
			output_dict[current_date] = {row: []}
			unique_dates.remove(tag.text.strip())
		if tag.name == 'td':
			if count <= 8 and count != 2 and count != 3:
				output_dict[current_date][row].append(tag.text.strip())
			count += 1

df_list = []
for date in output_dict.keys():
	header = [date, 'Country', 'Event', 'Actual', 'Previous', 'Consensus', 'Forecast']
	df = pd.DataFrame(columns=header)
	df.columns = header
	for row in output_dict[date].keys():
		if output_dict[date][row]:
			df.loc[len(df)] = output_dict[date][row]
	df_list.append(df)

for df in df_list:
	print(df.to_string(index=False))
