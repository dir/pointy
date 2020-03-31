from bs4 import BeautifulSoup
import grequests
import argparse
import requests
import time
import lxml
import tqdm
import re
import os

""" ____           _          __        
   / __ \\ ____   (_)____    / /_ __  __
  / /_/ // __ \\ / // __ \\ / __// / / /
 / ____// /_/  // //  / / // /_ / /_/ / 
/_/     \\____//_//_/ /_/ \\__/ \\__,/  
                               /____/  
Endpoint locator/scraper. Useful for finding endpoints.
Written by Luke Davis (http://luke.onl)
MIT License
"""

def cls():
	os.system('cls' if os.name=='nt' else 'clear')

class IncorrectHeaderType(Exception):
   """Raised when the headers are incorrect type"""
   pass

class InvalidURL(Exception):
   """Raised when url parameter given is valid."""
   pass

class EndpointScraper(object):
	def __init__(self, url):
		self.url = url
		self.printUI()

		self.headers = {
			'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
			'accept-language': 'en-US,en;q=0.9,de;q=0.8'
		}

	def printUI(self):
		print (
		"    ____          _         __        \n"
		"   / __ \\ ____   (_)____   / /_ __  __\n"
		"  / /_/ // __ \\ / // __ \\ / __// / / /\n "
		"/ ____// /_/ // // / / // /_ / /_/ /   \n"
		"/_/     \\____//_//_/ /_/ \\__/ \\__, /  \n"
		"                             /____/   ")
		print("written by Luke Davis (http://luke.onl)")

	def findAllURLs(self):
		try:
			source = requests.get(self.url, headers=self.headers)
		except:
			raise InvalidURL

		url_regex = re.compile(r"['|\"]http[s].*?['|\"]")

		url_with_quotes_list = url_regex.findall(source.text)

		url_list = []

		for url_with_quotes in url_with_quotes_list:
			url_with_quotes = url_with_quotes.replace('\'', '')
			url_with_quotes = url_with_quotes.replace('\"', '')
			url_list.append(url_with_quotes)

		return url_list

	def findURLsWithExtension(self, extension):
		urls = self.findAllURLs()

		if "." in extension:
			pass
		else:
			extension = "." + extension

		url_list = []

		for url in urls:
			if extension in url:
				url_list.append(url)

		return url_list
	
	def keywordSearch(self, keyword, extension):
		keyword = keyword.lower()
		url_list = self.findURLsWithExtension(extension)

		keyword_list = []

		responses = grequests.map(grequests.get(url, headers=self.headers) for url in url_list)

		for response in tqdm.tqdm(responses):
			if keyword in response.text:
				keyword_list.append(response.url)

		return keyword_list

	def setHeaders(self, headers):
		if(type(headers) is dict):
			self.headers = headers
		else:
			raise IncorrectHeaderType

if __name__ == '__main__':
	pointy_argparser = argparse.ArgumentParser(prog='pointy', description='Display endpoints based on keywords.')
	pointy_argparser.add_argument('-url', type=str, help='base url for endpoint finder')
	pointy_argparser.add_argument('-kw', type=str, help='keyword for endpoint search')
	pointy_argparser.add_argument('-ext', type=str, help='file extension for endpoint search')
	
	args = pointy_argparser.parse_args()

	args_dict = vars(args)

	es = EndpointScraper(args_dict['url'])
	list = es.keywordSearch(args_dict['kw'], args_dict['ext'])

	for url in list:
		print(url)
