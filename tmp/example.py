#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date, timedelta
import urllib
from selenium import webdriver
import os


def getText(link, driver):
	driver.get(link)
	result = driver.page_source
	soup = BeautifulSoup(result, 'html.parser')

	header= soup.find("h2", {"id": "titleapp"}).find("div").text.strip()
	
	date_list = soup.find("div", {"class": "headline-data"}).text.strip().split("KST")[0][12:].split()
	hour = date_list[-1]

	rest = date_list[0].split(".")
	month = rest[0]
	day = rest[1].split(",")[0]
	year = rest[1].split(",")[-1]

	if "Jan" == month:
		month = "01"
	elif "Feb" == month:
		month = "02"
	elif "Mar" == month:
		month = "03"
	elif "Apr" == month:
		month = "04"
	elif "May" == month:
		month = "05"
	elif "Jun" == month:
		month = "06"
	elif "Jul" == month:
		month = "07"
	elif "Aug" == month:
		month = "08"
	elif "Sep" == month:
		month = "09"
	elif "Oct" == month:
		month = "10"
	elif "Nov" == month:
		month = "11"
	elif "Dec" == month:
		month = "12"
	if len(day)==1:
		day = "0"+day
	date = year + "-" + month +"-"+day+" " + hour
	category = soup.find("div", {"class": "view_map"}).find("span").findAll("a")[-1].text.strip()


	content_tag = soup.find("div", {"id": "bodyapp"}).find("div")
	
	for i in content_tag.findAll(True):
		i.extract()
	content = content_tag.text.strip()

	author = ""
	try:
		author_list = content.split('Please direct comments or questions to')[0].strip().split()[-16:]
		for i in range(len(author_list)):
			if "By" in author_list[i]:
				author += author_list[i+1] + " " +  author_list[i+2]
				break	
		if "," in author:
			author = author.replace(",","")
	except:
		author= ""
	
	
	return [header, date, category, author, content]



base_dir = os.getcwd()
driver = webdriver.Chrome(base_dir + '/chromeforwindow')
driver.implicitly_wait(10)
abc = getText("http://english.hani.co.kr/arti/english_edition/e_northkorea/869635.html", driver)
for i in abc:
	print(i)
	print("------------------------------------------------------------")