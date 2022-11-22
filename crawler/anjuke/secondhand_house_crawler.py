"""
爬取安居客网站苏州的二手房数据
"""

import requests
from bs4 import BeautifulSoup
import threading
import time
from crawlUrlManager import CrawlerUrlManager

def get_proxies():
    proxy_list = []
    #proxy_list = [{'http': 'http://27.159.142.62:40042', 'https': 'http://27.159.142.62:40042'},
                  #{'http': 'http://121.230.208.242:40041', 'http': 'http://121.230.208.242:40041'},
                  #{'http': 'http://27.159.142.62:40042', 'https': 'http://27.159.142.62:40042'},
                  #{'http': 'http://121.230.208.242:40041', 'http': 'http://121.230.208.242:40041'},
                  #{'http': 'http://27.159.142.62:40042', 'https': 'http://27.159.142.62:40042'},
                  #{'http': 'http://121.230.208.242:40041', 'http': 'http://121.230.208.242:40041'}]
    proxy_url = 'http://api.tianqiip.com/getip?secret=zmwapiifw1q2ad7l&num=1&type=json&port=1&time=3&mr=1&sign=9a3585376ca017b008a9a34d6b1f19de'
    try:    
        datas = requests.get(proxy_url).json()
        #如果代理ip获取成功
        if datas['code'] == 1000: 
            data_array = datas['data']   
            for i in range(len(data_array)):
                proxy_ip = data_array[i]['ip']
                proxy_port = str(data_array[i]['port'])
                proxy = proxy_ip + ":" + proxy_port
                proxy_list.append({'http':'http://'+proxy,'https':'http://'+proxy})
        else:
            code = datas['code'] 
            print(f'获取代理失败，状态码={code}')
        return proxy_list
    except Exception as e:
        print('调用天启API获取代理IP异常:'+ e)
        return proxy_list

def craw_anjuke_suzhou(craw_url,proxy):
    
    if craw_url is None:
        print(threading.current_thread().getName()+' craw_url is None')
        return

    print(threading.current_thread().getName()+f' is crawing...使用代理{proxy}')
    
    #构造url的request headers，伪装成正常用户
    headers = {
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'cookie': 'sessid=52E9DCA6-EF00-3B81-DB4B-92501A00C897; aQQ_ajkguid=E28EFACC-BD44-DCB3-36AD-44C7F4C59F54; twe=2; ajk-appVersion=; seo_source_type=0; fzq_h=a11c708eee2f58b50c57db78180c25a0_1668935822035_47858592090d4ccb84ebb0951dc167df_1780979444; id58=CrIgxGN58I+ph40vUiLbAg==; ctid=19; fzq_js_anjuke_ershoufang_pc=35248d391b15e8fa346ef7d1fcd298a6_1668958842229_24; obtain_by=1; xxzl_cid=4474178988384322b9f12c2b9ff082ea; xxzl_deviceid=dWfUPC2sWkeSUujJ+hW52AvyRDziPV06903sSUCgTiZF8LD/+0Xcwtu2EnNcFBmC',
        'pragma': 'no-cache',
        'referer': 'https://suzhou.anjuke.com/sale/p5/?from=HomePage_TopBar',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "macOS",
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    
    with open('crawler/anjuke/suzhouSecondHouse.csv','a') as fout:
        #有代理用代理，没代理直接爬
        if proxy is None:
            r = requests.get(url=craw_url,headers=headers,timeout=3)
        else:
            r = requests.get(url=craw_url,headers=headers,proxies=proxy,timeout=10)
        #如果正常返回结果，开始解析    
        if r.status_code == 200:
            content = r.text
            #print(content)
            soup = BeautifulSoup(content,'html.parser') 
            content_div_nodes = soup.find_all('div',class_='property-content')
            for content_div_node in content_div_nodes:
                #获取房产标题内容
                content_title_name = content_div_node.find('h3',class_='property-content-title-name')
                title_name = content_title_name.get_text()
                #获取房子户型
                content_layout = content_div_node.find('p',class_='property-content-info-text property-content-info-attribute')
                layout_datas = content_layout.find_all('span')
                datas_shi = layout_datas[0].get_text()+layout_datas[1].get_text()
                datas_ting = layout_datas[2].get_text()+layout_datas[3].get_text()
                datas_wei = layout_datas[4].get_text()+layout_datas[5].get_text()
                #获取房子的面积、朝向、楼层和建筑年份
                square_num = ''
                square_unit = ''
                orientations = ''
                floor_level = ''
                build_year = ''
                content_extra_info_datas = content_div_node.find_all(lambda content_div_node:content_div_node.name == 'p'and content_div_node.get('class')==['property-content-info-text'])
                for i in range(len(content_extra_info_datas)):
                    if i == 0:
                        square = content_extra_info_datas[0].get_text().strip()
                        square_num = square[0:len(square)-1]
                        square_unit = square[len(square)-1:]
                    if i == 1:
                        orientations = content_extra_info_datas[1].get_text().strip()
                    if i == 2 :
                        floor_level = content_extra_info_datas[2].get_text().strip()
                    if i == 3:
                        build_year = content_extra_info_datas[3].get_text().strip()
                #获取房子的小区名称、位置信息（区-镇-道路）
                content_info_comm = content_div_node.find('div',class_='property-content-info property-content-info-comm')
                #获取小区名称
                housing_estate = content_info_comm.find('p',class_='property-content-info-comm-name').get_text().strip()
                #获取小区地址信息
                content_info_address = content_info_comm.find('p',class_='property-content-info-comm-address').find_all('span')
                district = content_info_address[0].get_text().strip()
                town = content_info_address[1].get_text().strip()
                road = content_info_address[2].get_text().strip()
                #获取房子的更多tag信息，比如朝向、是否满五唯一、房子新旧、是否近地铁等
                content_info_tag = content_div_node.find_all('span',class_='property-content-info-tag')
                tagstr = ''
                for i in range(len(content_info_tag)):
                    tagstr = tagstr + content_info_tag[i].get_text().strip() +','
                #获取房子价格信息
                price_info_datas = content_div_node.find('div',class_='property-price')
                total_price = price_info_datas.find('span',class_='property-price-total-num').get_text().strip()
                total_price_unit = price_info_datas.find('span',class_='property-price-total-text').get_text().strip()
                avarage_price = price_info_datas.find('p',class_='property-price-average').get_text().strip()
                avarage_price_num = avarage_price[0:len(avarage_price)-3]
                avarage_price_unit= avarage_price[len(avarage_price)-3:]
                #输出到文件
                fout.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"%(title_name,datas_shi,datas_ting,datas_wei,square_num,square_unit,orientations,floor_level,build_year,housing_estate,district,town,road,tagstr,total_price,total_price_unit,avarage_price_num,avarage_price_unit))
            print(f'{threading.current_thread().getName()} crawl over!;Crawler Url is:{craw_url}') 
        else:
            print(f'{threading.current_thread().getName()} crawl fail!status code={r.status_code};Crawler Url is:{craw_url}') 
    
if __name__ == '__main__':
    
    #先将标题写入结果数据文件
    with open('crawler/anjuke/suzhouSecondHouse.csv','w') as fout:
        fout.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"%('待售房屋','室','厅','卫','面积','面积单位','朝向','楼层','建筑年份','小区名称','区','镇','道路','标签','总价','总价单位','均价','均价单位'))
    
    #假设爬取crawler_pages页，生成待爬取的url，放入url池管理起来
    crawlerUrlManager = CrawlerUrlManager()
    #要爬取的页数，默认为100，可调整
    crawler_pages = 200
    for i in range(crawler_pages):
        craw_url = f'https://suzhou.anjuke.com/sale/p{i+1}/?from=HomePage_TopBar'
        crawlerUrlManager.add_new_url(craw_url)
    
    #尝试获取代理ip，避免同一个ip频繁访问被网站的反爬机制给封禁
    proxy_list = get_proxies()
    proxy_num = len(proxy_list)
    if proxy_num >= 5:#如果获取到代理ip，则用代理ip，建议至少获取5个及以上的代理ip，爬取的时候每个线程一个ip进行爬取
        print(f'获取到{proxy_num}个代理ip，开始使用代理IP爬取页面数据...')
        
        while crawlerUrlManager.has_new_url():
            crawler_threads = []
            for i in range(len(proxy_list)):
                proxy = proxy_list[i]
                crawler_thread = threading.Thread(target=craw_anjuke_suzhou,args=(crawlerUrlManager.get_url(),proxy))
                crawler_threads.append(crawler_thread)
                    
            #启动线程开始爬取
            for crawler_thread in crawler_threads:
                crawler_thread.start()
                                
            for crawler_thread in crawler_threads:
                crawler_thread.join()

            #谨慎起见，一批线程爬取结束后，间隔一段时间，再启动下一批爬取，这里默认设置为3秒，可调整
            time.sleep(3)
        
    else:#如果没获取到代理ip，则直接爬取，控制一下每个线程爬取的间隔时间，不要太频繁
        try:    
            print('没有获取到代理IP，开始使用自身IP爬取页面数据...')
            while crawlerUrlManager.has_new_url():
                    
                crawler_thread = threading.Thread(target=craw_anjuke_suzhou,args=(crawlerUrlManager.get_url(),None))
                crawler_thread.start()
                    
                crawler_thread.join()
                time.sleep(10)#为避免同一个ip频繁爬取被反爬封禁，一线程爬取完后，等待10秒再爬取下一个页面
            
        except Exception as e:
            print('Crawler Excepiton:' + e)
        finally:
            print(f'已爬取的url数量：{crawlerUrlManager.get_old_url_size()}')
            print(f'未爬取的url数量：{+crawlerUrlManager.get_new_url_size()}')
            if crawlerUrlManager.get_new_url_size() > 0:
                print('未爬取的url如下：')
                for new_url in crawlerUrlManager.get_url():
                    print(f'{new_url}')
            
       
             
