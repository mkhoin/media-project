import requests
import time, re
import urllib
from bs4 import BeautifulSoup

#my python file
import classifier as cf

# load baseURL in text file
def load_baseURL():
	base_list = []
	read_list = []
	with open("./base/baseURL.txt", "r") as base:
		while True: 
			line = base.readline()
			if not line: break

			line = line.replace('\n', '')
			base_list.append(line)

	with open("./base/readURL.txt", "r") as read:
		while True: 
			line = read.readline()
			if not line: break

			line = line.replace('\n', '')
			read_list.append(line)

	return base_list, read_list


# crawl URL in entertain section (korean baseball only)
def entertain_URL(base, read, date):
	all_URL  = []
	page = 1

	while True:
		URL = []

		# request to URL
		request = base+date+"&page="+str(page)
		ret = requests.get(request)

		# get article URL
		soup = BeautifulSoup(ret.text)
		for c in soup.find_all("li"):
			if c.parent.get("class") == ['news_lst', 'news_lst2']:
				# if no attribute founded then pass
				if c.a: URL.append(c.a['href'])

		# check if last page
		if not URL: break;
	
		# construct to full-URL
		for i, v in enumerate(URL):
			# if give URL is full-URL
			if "com" in v : URL[i] = read + "/" + v.split("/")[3]
			else: 		    URL[i] = read + v
		all_URL.extend(URL)

		# sleep 0.3 sec for avoid NAVER's block
		time.sleep(0.3)
		page += 1

	return all_URL


# crawl URL in sports section
def sports_URL(base, read, date):
	all_URL = []
	page = 1

	while True:
		URL = []

		# request to URL
		date = date.replace("-", "")
		request = base+date+"&page="+str(page)
		ret = requests.get(request)

		# get article URL
		soup = BeautifulSoup(ret.text)
		for c in soup.find_all("td"):
			if c.get("class") == ['ln15']:
				#if no attribute founded then pass
				if c.a: URL.append(c.a['href'])
		
		# check if last page
		if not URL: break;
		
		# construct to full-URL
		for i, v in enumerate(URL):
			# if give URL is full-URL
			if "com" in v : URL[i] = read + "/" + v.split("/")[3]
			else: 		    URL[i] = read + v
		all_URL.extend(URL)

		# sleep 0.3 sec for avoid NAVER's block
		time.sleep(0.3)
		page += 1

	return all_URL


# crawl URL in news exclude sports, entertain
def news_URL(base, date):
	all_URL = []
	prev_URL = [] # contain URL of previous page to check last page
	page = 1
	
	while True:
		URL = []

		# request to URL
		date = date.replace("-", "")
		request = base+date+"&page="+str(page)
		ret = requests.get(request)

		# get article URL
		soup = BeautifulSoup(ret.text)
		for c in soup.find_all("dl"):
			if c.parent.parent.get("class") == ['type06'] or c.parent.parent.get("class") == ['type06_headline']:
				URL.append(c.contents[1].a['href'])
	
		# construct to full-URL
		for i, v in enumerate(URL):
			URL[i] = v

		# check if last page
		if prev_URL == URL: break;
		all_URL.extend(URL)
		prev_URL = URL

		# sleep 0.3 sec for avoid NAVER's block
		time.sleep(0.3)
		page += 1
	
	return all_URL


def entertain_context( URLs ):
	article = []
	title   = []
	for URL in URLs:
		# request to URL	
		ret = requests.get(URL)
		soup = BeautifulSoup(ret.text)

		try:
			# get title
			for c in soup.find_all("p"):
				if c.get("class") == ["end_tit"]: 
					title.append(c.get_text().strip())		

			# get article
			text = soup.find(id="articeBody").get_text().replace("\n", "")
			article.append(text.split("@")[0])
			print(title[len(title)-1])
		except AttributeError as ae:
			print("ERROR: {!s:s}\n" .format(URL))

	return title, article


def sports_context( URLs ):
	article = []
	title   = []
	for URL in URLs:
		# request to URL	
		ret = requests.get(URL)
		soup = BeautifulSoup(ret.text)
		
		try:
			# get title
			for c in soup.find_all("h4"):
				if c.get("class") == ["tit_article"]: 
					title.append(c.get_text().strip())
			
			# get article
			text = soup.find(id="naver_news_20080201_div").get_text().replace("\n", "")
			article.append(text.split("@")[0])
			print(title[len(title)-1])
		except AttributeError as ae:
			print("ERROR: {!s:s}\n" .format(URL))

	return title, article


def news_context( URLs):
	article = []
	title   = []
	for URL in URLs:
		# request to URL	
		ret = requests.get(URL)
		soup = BeautifulSoup(ret.text)

		try:
			# get title
			title.append(soup.find(id="articleTitle").get_text().strip())
			
			# get article
			text = soup.find(id="articleBodyContents").get_text().replace("\n", "")
			article.append(text.split("@")[0])
			print(title[len(title)-1])
		except AttributeError as ae:
			print("ERROR: {!s:s}\n" .format(URL))

	return title, article
