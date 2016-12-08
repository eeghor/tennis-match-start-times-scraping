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
y_from = 2015
y_to = 2015


ao_tz = timezone("Australia/Melbourne")


# choose what sort of competitions
"""
MS : Men's Singles
WS : Women's Singles

"""

comp_types = "MS"

comp_types_dict = {"MS" : "Men's Singles", "WS" : "Women's Singles"}
# dictionary used to create the right URL
add_to_link_dict = {"MS": "men", "WS": "women"}

# show this 
print("""-------> scraping tennis.wettpoint.com/""")
# lists to store the scraped data
list_player1 = []
list_player2 = []
list_date = []
list_starttime_cet = []  # CET – Central European Time (presumably)

for ct in comp_types.split():
	for year in range(y_from, y_to + 1):

		season_line = "http://tennis.wettpoint.com/en/archiv/australian-open-" + add_to_link_dict[ct] + "-" + str(year) + ".html"

		print("line:",season_line)
		print("downloading ", comp_types_dict[ct], "data for ", str(year), "...", end="")
		page = requests.get(season_line)

		if page.status_code == 200:
			print("ok")
		else:
			print("error {}!".format(year))

		# create a soup object
		soup = BeautifulSoup(page.content, 'html.parser')

		rws = soup.find_all("tr")

		for row in rws:

			# check if it's a header
			if len(row.find_all("td")) == 3:
				c1, c2, c3 = row.find_all("td")
				datetime.strptime(c1.text, "%d/%m/%y %H:%M")
				list_date.append(date_full.split()[0].strip())
				list_starttime_cet.append(date_full.split()[1].strip())
				player1_full, player2_full = c2.text.split("-")
				list_player1.append(player1_full.strip())
				list_player2.append(player2_full.strip())

			print(list_date)









