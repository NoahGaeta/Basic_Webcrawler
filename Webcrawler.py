# Author: Noah Gaeta -- Date: 02/28/2019
from __future__ import print_function

from urllib import urlopen
from multiprocessing import Process, Manager
import multiprocessing as mp
import re
import json


class Webcrawler:

	URL_JSON_FILE_PATH = 'urls.json'

	def __init__(self, start_url, crawl_amount, already_crawled=[]):
		self.start_url = start_url
		self.crawl_amount = crawl_amount
		self.already_crawled = already_crawled

	def find_url_pattern_matches(self, response):
		urls_found = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', response)
		return self.remove_duplicates(urls_found)

	def start_crawl(self):
		response = self.get_response(self.start_url)
		url_list = self.find_url_pattern_matches(response)

		self.already_crawled = list(self.start_url)
		returned_list = self.crawl(url_list)
		while len(returned_list) < self.crawl_amount:
			returned_list = self.crawl(returned_list)
		self.dump_urls(returned_list, self.URL_JSON_FILE_PATH)

	def crawl(self, url_list):
		processes = []
		result_manager = Manager()
		results = result_manager.list()
		map(lambda url: processes.append(Process(target=self.crawl_url, args=(url, results,))), url_list)
		chunked_processes = self.split_list(processes, mp.cpu_count() - 1)
		for chunk in chunked_processes:
			map(lambda process: process.start(), chunk)
			map(lambda process: process.join(), chunk)
		return list(results)

	def crawl_url(self, url, results):
		if url not in self.already_crawled:
			results += self.find_urls(url)

	def find_urls(self, url):
		try:
			response = self.get_response(url)
			self.already_crawled.append(url)
			return self.find_url_pattern_matches(response)
		except Exception as e:
			self.already_crawled.append(url)
			print("Exception: " + str(e) + "\ncontinuing")
			return []

	@staticmethod
	def dump_urls(url_list, path):
		with open(path, 'w') as outfile:
			json.dump(url_list, outfile, indent=4)

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
	def split_list(l, n):
		for i in range(0, len(l), n):
			yield l[i:i + n]
