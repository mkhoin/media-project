# -*- coding: utf-8 -*-

import time
import requests
import classifier as cf
import utils
from selenium import webdriver
from bs4 import BeautifulSoup
from konlpy.tag import Mecab

class crawl_community():
	def __init__( self ):
		self.driver = webdriver.Firefox()
		self.classifier = cf.classifier()
		self.URLs = []
		self.contexts = []

		self.bag = utils.load_dictionary()
		self.tagger = Mecab()

	
	def __del__( self ):
		self.driver.quit()
	
		
	def _crawl_URL( self ):
		titles = []

		# dynamic scrolling
		more_count = 0
		while True:
			time.sleep(0.5)
			more = self.driver.find_element_by_id("real_more_page")

			if more.is_displayed():
				if more.text == "더보기":
					more.click()
					more_count += 1
				else: 
					break
			else:
			 	self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			if more_count >= self.scroll: break

		# get html source
		html = self.driver.page_source
		soup = BeautifulSoup(html)

		# crawl URL
		for c in soup.find_all("li"):
			# if items are from community 
			if c.get("class") == ['realtimeitem', 'community']:
				href = c.find("a")["href"]
				self.URLs.append(href)
				title = c.find("a").get_text().strip()
				titles.append(title)
			# if items are from twitter
			elif c.get("class") == ['realtimeitem', 'twitter']:
				for s in c.find_all("span"):
					if s.get("class") == ['text', 'snsbody']:
						href = s['href']
						self.URLs.append(href)
						titles.append("twitter")

		return titles


	def _exclude_short( self, text ):
		pos = self.tagger.pos(text)
		words = [ p[0] for p in pos ]

		is_in = False
		for b in self.bag[0]:
			if b[0] in words: is_in = True

		for b in self.bag[1]:
			if b[0] in words: is_in = True

		return not is_in


	def _crawl_dcinside( self, url, title ):
		ret = requests.get(url)
		soup = BeautifulSoup(ret.text)

		for c in soup.find_all("div"):
			if c.get("class") == ["s_write"]:
				text = c.find_all("td")[0].get_text()
				text = text.strip().replace("\n", " ")
				
				exclude = self._exclude_short(text)
				if not exclude: self.contexts.append(["dcinside", title, text])

	"""
	def _crawl_mlbpark( self, url, title ):
		ret = requests.get(url)
		soup = BeautifulSoup(ret.text)

		for c in soup.find_all("td"):
			if c.get("class") == ["G13"] and c.find_all("div"):
				div = c.find_all("div")[0]
				text = div.get_text()
				text = text.strip().replace("\n", " ")
				
				exclude = self._exclude_short(text)
				if not exclude: self.contexts.append(["mlbpark", title, text])
				break
	"""


	def _crawl_twitter( self, url, title ):
		ret = requests.get(url)
		soup = BeautifulSoup(ret.text)
	
		for c in soup.find_all("p"):
			tag = c.get("class")
			if tag and "tweet-text" in tag:
				text = c.get_text().strip().replace("\n", " ")

				exclude = self._exclude_short(text)
				if not exclude : self.contexts.append(["twitter", title, text])


	def _crawl_todayhumor( self, url, title ):
		ret = requests.get(url)
		soup = BeautifulSoup(ret.text)

		for c in soup.find_all("div"):
			if c.get("class") == ["viewContent"]:
				text = c.get_text().strip().replace("\n", " ")

				exclude = self._exclude_short(text)
				if not exclude: self.contexts.append(["todayhumor", title, text])


	"""
	def _crawl_clien( self, url, title ):
		ret = requests.get(url)
		soup = BeautifulSoup(ret.text)

		c = soup.find(id="writeContents")
		if c: 
			text = c.get_text().strip().replace("\n", " ")
			if self._exclude_short: self.contexts.append(["clien", title, text])


	def _crawl_bobaedream( self, url, title ):
		ret = requests.get(url)
		soup = BeautifulSoup(ret.text)

		for c in soup.find_all("div"):
			if c.get("class") == ["bodyCont"]:
				text = c.get_text().strip().replace("\n", " ")
				if self._exclude_short: self.contexts.append(["bobaedream", title, text])
	"""

	def _crawl_fomos( self, url, title ):
		ret = requests.get(url)
		soup = BeautifulSoup(ret.text)

		for c in soup.find_all("div"):
			if c.get("class") == ["view_text"]:
				text = c.get_text().strip().replace("\n", " ")

				exclude = self._exclude_short(text)
				if not exclude: self.contexts.append(["fomos", title, text])
				break


	def _crawl_inven( self, url, title ):
		ret = requests.get(url)
		soup = BeautifulSoup(ret.text)

		for c in soup.find_all("div"):
			if c.get("class") == ["powerbbsContent"]:
				text = c.get_text().strip().replace("\n", " ")

				exclude = self._exclude_short(text)
				if not exclude: self.contexts.append(["inven", title, text])


	def _crawl_instiz( self, url, title ):
		ret = requests.get(url)
		soup = BeautifulSoup(ret.text)

		c = soup.find(id="memo_content_1")
		if c:
			text = c.get_text().strip().replace("\n", " ")

			exclude = self._exclude_short(text)
			if not exclude: self.contexts.append(["instiz", title, text])


	def _crawl_ppomppu( self, url, title ):
		ret = requests.get(url)
		soup = BeautifulSoup(ret.text)

		for c in soup.find_all("td"):
			if c.get("class") == ["han"]:
				text = c.get_text().strip().replace("\n", " ")

				exclude = self._exclude_short(text)
				if not exclude: self.contexts.append(["ppomppu", title, text])


	# determine which URL comes from
	def _crawl_context( self, titles ):
		for i, url in enumerate(self.URLs):
			if   "dcinside"   in url: self._crawl_dcinside(url, titles[i])
			#elif "mlbpark"    in url: self._crawl_mlbpark(url, titles[i])
			elif "todayhumor" in url: self._crawl_todayhumor(url, titles[i])
			#elif "clien"      in url: self._crawl_clien(url, titles[i])
			elif "twitter"    in url: self._crawl_twitter(url, titles[i])
			#elif "bobaedream" in url: self._crawl_bobaedream(url, titles[i])
			elif "fomos"	  in url: self._crawl_fomos(url, titles[i])
			elif "inven"	  in url: self._crawl_inven(url, titles[i])
			elif "instiz"	  in url: self._crawl_instiz(url, titles[i])
			elif "ppomppu"	  in url: self._crawl_ppomppu(url, titles[i])
			else: print(url)

		# classify sentiment
		for i, v in enumerate(self.contexts):
			vector = self.classifier.features(v[1]+v[2])
			predict = self.classifier.predict(vector).tolist()[0]
			self.contexts[i].insert(0, predict)


	def crawl( self, query, scroll = 5 ):
		self.scroll = scroll
		self.query = query
		self.url = "http://search.zum.com/search.zum?method=realtime&option=accu&query="+query+"&cm=more"
		self.driver.get(self.url)

		titles = self._crawl_URL()
		self._crawl_context(titles)	

		return self.contexts	
