
# coding: utf-8

# In[ ]:


import requests,re,time,bs4

from requests.exceptions import RequestException

import csv


# In[ ]:


def get_one_page(url):
    try:
        headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
        }
        res = requests.get(url,headers = headers)
        #data = re.findall('div.*?class="hd".*?href=".*?(\d+)/".*?title">(.*?)</span>.*?',res.text,re.S) #list
        if res.status_code==200:
            #print(res.text)
            return res.text
            #print('\n')
        else:
            return None
    except RequestException:
        return None
    
    
#返回的是榜单界面的代码


# In[ ]:


#定义解析页面的方法   html是榜单界面文本
def parse_one_page(html):  
    html = str(html)
    pattern = re.compile('div.*?class="hd".*?href=".*?(\d+)/".*?title">(.*?)</span>.*?',re.S) 
    items = re.findall(pattern,html)
    return items


# In[ ]:


def get_detail_page_url(list_hostname_filmname):
    film_name_info = []
    for filmname in list_hostname_filmname:
        return hostname[0]


# In[ ]:


def get_detail_page_name(list_hostname_filmname):
    for hostname in list_hostname_filmname:
        return hostname[1]


# In[ ]:


def parse_detail_page(html):#一个text
    film_info = []  #包含一部电影的信息，0：剧情简介
                    #                1:作品类型
                    #                2：豆瓣评分
                    #                3:相关电影
                    #                4:获得的奖项
    html = str(html)
    pattern_1 = re.compile('property="v:summary.*?>(.*?)(<br />|</span>).*?',re.S)
    pattern_2 = re.compile('property="v:genre">(.*?)</span>.*?property="v:average">(.*?)</strong>.*?class="recommendations-bd.*?alt="(.*?)".*?',re.S)
    synopsis = re.search(pattern_1,html)
    items = re.findall(pattern_2,html)
    #data_4 = re.search('span.*?class="all hidden">(.*?)<.*?>(.*?)</span>.*?',res_1.text,re.S)
    #print(data_3.group(1))
    #print(res_1.text) #详情页面
    #简介
    soup = bs4.BeautifulSoup(html,'html.parser')
    targets = soup.find_all("ul",class_="award")  
  
    #return data_3.group(1)
    for i in items:
        film_info.append(i)
        
    for each in targets:
        film_info.append(each.text)
    #except AttributeError:
     #   print(data_3.group(1))
    try:
        #Str = str(synopsis.group(1))
        film_info.append(synopsis.group(1))
    except:
        film_info.append("此电影暂无剧情简介！")

    return film_info
    
    #return film_detail  #返回一个列表


# In[ ]:


def film_short_comment(html):
    html = str(html)
    pattern = re.compile('div class="comment".*?votes">(.*?)</span>.*?class="short">(.*?)</span>.*?',re.S)
    items = re.findall(pattern,html) #list
    try:
        return items
    except:
        return None


# In[ ]:


url_1 = 'https://movie.douban.com/top250'
url_2 = 'https://movie.douban.com/subject/'
url_4 = '/comments?sort=new_score&status=P'
url_1_1 = '?start='
url_1_2 = '&filter='
with open('DouBanTop250.docx','a',encoding = 'utf-8')as f:
    f.write("=========================豆瓣电影前250榜单=========================\n\t\t\t\t\t\tCreate by Baikal\n\t\t\t\tdate updated:July 21th 2018\n\n\n")
    print("=========================豆瓣电影前250榜单=========================\n\t\t\t\t\t\tCreate by Baikal\n\t\t\t\tdate updated:July 21th 2018\n\n\n")
    for i in range(0,10):
        #https://movie.douban.com/top250?start=0&filter=
        url = url_1 + url_1_1 + str(i * 25) + url_1_2
        html = get_one_page(url)  #得到榜单界面代码
        list_hostname_filmname = parse_one_page(html)  #得到榜单界面代码里面的所有的主机名和电影名
        #filmname = get_detail_page_name(list_hostname_filmname)
        #hostname = get_detail_page_url(list_hostname_filmname) #得到榜单主机名
        
        for filmname in list_hostname_filmname:
            #print(filmname[1])
            f.write('电影名：'+filmname[1]+'\n')
            f.write('***********************************************\n')
            url_3 = url_2 + filmname[0]

            #html_1 = get_one_page(url_3)  #详情页面
           # detail = parse_detail_page(html_1)  #返回列表
                                #包含一部电影的信息，0：剧情简介
                                #                1:作品类型
                                #                2：豆瓣评分
                                #                3:相关电影
                                #                4:获得的奖项
            """for data in detail:
                f.write('剧情简介：'+data[4]+'\n')
                f.write('作品类型：'+data[0]+'\n')
                f.write('豆瓣评分：'+data[1]+'\n')
                f.write('相关电影：'+data[2]+'\n')
                f.write('获得的奖项：'+data[3]+'\n')"""
            url_5 = url_3 + url_4 
            print('电影名：'+filmname[1]+'\n')
            print('**************************************************\n')
            html_2 = get_one_page(url_5)
            comment = film_short_comment(html_2)
            f.write('电影热评：\n')
            for com in comment:
                print(com[0] + '人点赞:\n')
                print(com[1] + '\n')
                print('----------------------------------------------\n')

            for com in comment:
                f.write(com[0] + '人点赞:\n')
                f.write(com[1] + '\n')
                f.write('----------------------------------------------\n')
            f.write('==================================================\n')


            
            
            
            
    #with open('Douban.csv','w' )as csvfile:
    #    writer = csv.writer(csvfile)
    #    for fn in filmname:
   #         writer.writerow(fn)
    #https://movie.douban.com/subject/1292281/comments?sort=new_score&status=P
    #film_comment_page = url_2 + offset +url_1_1 + url_1_3
    #film_comment = get_one_page(film_comment_page)  #text
    #comment_want = film_short_comment(film_comment)

