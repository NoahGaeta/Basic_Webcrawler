# Author: Noah Gaeta -- Date: 02/28/2019
from __future__ import print_function

from urllib import urlopen
from time import time
import re
import json


class Webcrawler:

	def __init__(self, start_url, crawl_time, already_crawled=[]):
		self.start_url = start_url
		self.crawl_time = crawl_time
		self.already_crawled = already_crawled

	def find_urls(self, response):
		urls_found = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', response)
		return self.remove_duplicates(urls_found)

	def start_crawl(self):
		start_url = self.start_url
		response = self.get_response(start_url)
		url_list = self.find_urls(response)
		self.already_crawled = [start_url]
		returned_list = self.crawl(url_list)
		start_time = time()
		while self.get_time_left(start_time) < self.crawl_time:
			returned_list = self.crawl(returned_list)

	def crawl(self, url_list):
		for url in url_list:
			if url not in self.already_crawled:
				try:
					response = self.get_response(url)
					print("finding urls on " + url)
					url_list += (self.find_urls(response))
					url_list = self.remove_duplicates(url_list)
					self.already_crawled.append(url)
					with open('urls.json', 'w') as outfile:
						json.dump(url_list, outfile, indent=4)
				except Exception as e:
					self.already_crawled.append(url)
					print("Exception: " + str(e) + "\ncontinuing")
			else:
				print("Already crawled: " + url)
		return url_list

	@staticmethod
	def get_response(url):
		socket = urlopen(url)
		response = socket.read()
		socket.close()
		return response

	@staticmethod
	def remove_duplicates(url_list):
		return list(set(url_list))

	@staticmethod
	def get_time_left(start_time):
		print(str(time() - start_time))
		return time() - start_time
