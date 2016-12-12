"""
The idea is to obtain starting times for the Australian Open matches. All we need is date, time and who played.
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from collections import defaultdict
from datetime import datetime  # need to convert timezone
from pytz import timezone  # note that the AO timezone is called Australia/Melbourne

# choose years
y_from = 2010
y_to = 2016


ao_tz = timezone("Australia/Melbourne")
de_tz = timezone("Europe/Berlin")


# choose what sort of competitions
"""
MS : Men's Singles
WS : Women's Singles

"""

comp_types = "MS WS"

comp_types_dict = {"MS" : "Men's Singles", "WS" : "Women's Singles"}
# dictionary used to create the right URL
add_to_link_dict = {"MS": "men", "WS": "women"}

# show this 
print("""-------> scraping tennis.wettpoint.com/""")
# lists to store the scraped data
list_player1 = []
list_player2 = []
list_dtime= []
list_scores = []

for ct in comp_types.split():
	for year in range(y_from, y_to + 1):

		# http://tennis.wettpoint.com/en/archiv/australian-open-men-2015.html
		season_line = "http://tennis.wettpoint.com/en/archiv/australian-open-" + add_to_link_dict[ct] + "-" + str(year) + ".html"

		#print("line:",season_line)
		print("downloading ", comp_types_dict[ct], "data for", str(year), "...", end="")
		headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
		page = requests.get(season_line, headers=headers)

		if page.status_code == 200:
			print("ok")
		else:
			print("error!")
			print("status code {}".format(page.status_code))

		# create a soup object
		soup = BeautifulSoup(page.content, 'html.parser')

		rws = soup.find_all("tr")

		for row in rws:

			# check if it's a header
			if len(row.find_all("td")) == 3:

				c1, c2, c3 = row.find_all("td")

				# localized data and tome below look like 2015-01-23 13:00:00+11:00
				dtime_parsed_berlin = de_tz.localize(datetime.strptime(c1.text, "%d/%m/%y %H:%M"))
				dtime_parsed_melbourne = dtime_parsed_berlin.astimezone(ao_tz)
				
				player1_full, player2_full = map(lambda x: x.strip(), c2.text.split(" - "))  # note 2 white spaces around - !

				list_player1.append(player1_full)
				list_player2.append(player2_full)

				list_dtime.append(dtime_parsed_melbourne.strftime("%Y-%m-%d %H:%M"))
				list_scores.append(c3.text.strip())

# now combine eerything into a zip
data = zip(list_dtime, list_player1, list_player2, list_scores)


# put the data into a pandas data frame
df = pd.DataFrame(columns="date  player1 player2 score".split())

for i, row in enumerate(data):
	df.loc[i] = row

print("successfully retrieved {} results..".format(len(df.index)))

if y_from != y_to:
	csv_fl = "scraped_data_from_tennis_wettpoint_ao_yrs_" + str(y_from) + "_to_" + str(y_to) + ".csv"
else:
	csv_fl = "scraped_data_from_tennis_wettpoint_ao_" + str(y_from) + ".csv"

df.to_csv(csv_fl, index=False, sep="&")







