#!usr/bin/python
#_*_ coding:utf-8 _*_
import urllib2
import cookielib
import re
import json
def get_page_sources(url):
	headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Cache-Control':'max-age=0'
	}
	cookie = cookielib.CookieJar()
	handle = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handle)
	request = urllib2.Request(url = url,headers = headers)
	response = urllib2.urlopen(request)
	contents = response.read()
	return str(contents)
def get_meichandise_picture(url):
    mattern = r'"pic_url":"([^"]+)'
    meichandise_picture = re.compile(mattern).findall(get_page_sources(url))
    return meichandise_picture
def get_all_url_numb(url):
	mattern = r'"totalPage":([^,]+)'
	All_url_numb = re.compile(mattern).findall(get_page_sources(url))
	return All_url_numb
def get_all_page_url(url,search_name):
	page_url1 = "https://s.taobao.com/search?q=%s&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20160718" % search_name
	page_url = [page_url1]
	page_url2 = []
	for i in range(int(get_all_url_numb(url)[0])):
		page_numb = 30 * i
		last_page = '&bcoffset=0&s=' + str(page_numb)
		all_page_url = page_url[0] + last_page
		page_url2.append(all_page_url)
	return page_url2
def Combine_name_price_grade(url):
	all_meichandise = []
	mattern1 = r'"raw_title":"([^"]+)'
	get_meichandise_name = re.compile(mattern1).findall(get_page_sources(url))
	mattern2 = r'"view_price":"([^"]+)'
	get_meichandise_price = re.compile(mattern2).findall(get_page_sources(url))
	mattern = r'"view_sales":"([^"]+)'
	pay_people_numb = re.compile(mattern).findall(get_page_sources(url))
	for i in range(get_meichandise_name.__len__()):
		single_meichandise = []
		single_meichandise.append(get_meichandise_name[i])
		single_meichandise.append(get_meichandise_price[i])
		single_meichandise.append(pay_people_numb[i])
		all_meichandise.append(single_meichandise)
	return all_meichandise

def get_all_meichandise_contents(url,search_name = None):
	for i in get_all_page_url(url,search_name):
		meidantise_contents = Combine_name_price_grade(i)
		print json.dumps(meidantise_contents,encoding='utf-8',ensure_ascii=False)
search_name = "鞋子"
URL2 = 'https://s.taobao.com/search?q=%s&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20160718' % search_name
d = get_all_meichandise_contents(URL2,search_name)
