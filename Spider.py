import re
import requests
from bs4 import BeautifulSoup

import html_downloader
import html_outputer
import html_parser
import csv
import time


class SpiderMain(object):
    def __init__(self, xing, ming):
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.xing = xing
        self.ming = ming
        self.param = {'origin': 'searchauthorlookup',
                      'src': 'al',
                      'edit': '',
                      'poppUp': '',
                      'basicTab': '',
                      'affiliationTab': '',
                      'advancedTab': '',
                      'st1': xing,
                      'st2': ming,
                      'institute': '',
                      '_exactSearch': 'on',
                      'orcidId': '',
                      # 'authSubject':'LFSC',
                      '_authSubject': 'on',
                      # 'authSubject':'HLSC',
                      '_authSubject': 'on',
                      # 'authSubject':'PHSC',
                      '_authSubject': 'on',
                      # 'authSubject':'SOSC',
                      '_authSubject': 'on',
                      's': 'AUTH--LAST--NAME({0}) AND AUTH--FIRST({1})'.format(ming, xing),
                      'sdt': 'al',
                      'sot': 'al',
                      # 'searchId':sid,
                      # 'sid':sid
                      }

    def craw(self):
        root = 'https://www.scopus.com/results/authorNamesList.uri'
        ses = requests.session()  # 创建session
        # ses.proxies={'https':'http://127.0.0.1:1085'}#代理
        s = ses.get(root, params=self.param, timeout=60)  # 搜索得到作者列表页面
        AuthorID = self.parser.GetAuthorId(s)  # 获取authorid
        print(AuthorID)
        if (AuthorID == False):
            return

        else:
            self.crawel(ses, AuthorID)

    def crawel(self, ses, AuthorID, bianhao=0):
        s2 = ses.get('https://www.scopus.com/authid/detail.uri', params={'authorId': AuthorID})  # 获取作者详细信息页面
        message = self.parser.GetAuthorMessage(s2)  # 获取详细信息
        wenxin = message[0]
        AuthorName = message[1]
        area = message[2]
        lishi = message[4]
        email = ''
        suoxie = ''
        nian = ''
        if int(wenxin) < 10:  # 文献数少于10，直接返回
            # print('文献数为'+wenxin+'，不符合要求')
            return AuthorName, area, lishi, email, suoxie, nian, wenxin
        print('文献数：' + wenxin + ' ' + lishi)
        print(AuthorName)
        print(area)
        Articlelink = message[3]  # 获取作者所有文章页面链接
        print(Articlelink)
        s3 = ses.get(Articlelink, timeout=60)  # 获取作者所有文章页面
        Articles = self.parser.GetArticles(s3)  # 获得所有文章链接及年份列表
        for lists in Articles:
            print("进入文章")
            link = lists[0]
            nian = lists[1]
            s4 = ses.get(link, timeout=60)  # 获取文章详细信息页面
            emailnotparse, suoxie = self.parser.GetEmail(s4)  # 得到加密的邮件地址
            if emailnotparse != None:
                if bianhao != 0:
                    print('第' + str(bianhao) + '作者')
                print('文献数：' + wenxin + ' ' + lishi)
                print(AuthorName)
                print("缩写：" + suoxie)
                print(area)
                email = strip_email_protection(emailnotparse['href'])
                print(email)
                # print('<a href=\''+email+'\'>'+email+'></a>')
                print('年份: ' + nian + '\n')
                return AuthorName, area, lishi, email, suoxie, nian, wenxin
        return AuthorName, area, lishi, email, suoxie, nian, wenxin
        # print("没找到邮箱")


class AuthorIDSpiderMain(object):
    def __init__(self, authorid):
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.authorid = authorid
        self.param = {'origin': 'searchauthorlookup',
                      'src': 'al',
                      'edit': '',
                      'poppUp': '',
                      'basicTab': '',
                      'affiliationTab': '',
                      'advancedTab': '',
                      'st1': '',
                      'st2': '',
                      'institute': '',
                      '_exactSearch': 'on',
                      'orcidId': '',
                      # 'authSubject':'LFSC',
                      '_authSubject': 'on',
                      # 'authSubject':'HLSC',
                      '_authSubject': 'on',
                      # 'authSubject':'PHSC',
                      '_authSubject': 'on',
                      # 'authSubject':'SOSC',
                      '_authSubject': 'on',
                      's': '',
                      'sdt': 'al',
                      'sot': 'al',
                      # 'searchId':sid,
                      # 'sid':sid
                      }

    def craw(self):
        ses = requests.session()  # 创建session
        root = 'https://www.scopus.com/results/authorNamesList.uri'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        url = 'https://pusidp4.polyu.edu.hk/nidp/idff/sso?id=56&sid=0&option=credential&sid=0&target=https://www2.polyu.edu.hk/library/ticket.php?url=http://www.scopus.com'
        # ses.proxies={'https':'http://127.0.0.1:1085'}#代理
        s = ses.get(root, params=self.param, timeout=20)  # 搜索得到作者列表页面
        AuthorID = self.authorid  # 获取authorid
        print(AuthorID)
        if (AuthorID == False):
            return

        else:
            return self.crawel(ses, AuthorID)

    def crawel(self, ses, AuthorID, bianhao=0):
        s2 = ses.get('https://www.scopus.com/authid/detail.uri',
                     params={'authorId': AuthorID})  # 获取作者详细信息页面
        message = self.parser.GetAuthorMessage2(s2)  # 获取详细信息
        wenxin = message[0]
        AuthorName = message[1]
        area = message[2]
        lishi = message[4]
        firstname = message[5]
        lastname = message[6]
        country = message[7]
        city = message[8]
        university = message[9]
        dept = message[10]
        email = ''
        suoxie = ''
        nian = ''
        if int(wenxin) < 10:  # 文献数少于10，直接返回
            # print('文献数为'+wenxin+'，不符合要求')
            return AuthorName, area, lishi, email, suoxie, nian, wenxin
        print('文献数：' + wenxin + ' ' + lishi)
        print(AuthorName)
        print(area)
        Articlelink = message[3]  # 获取作者所有文章页面链接
        print(Articlelink)
        s3 = ses.get(Articlelink, timeout=60)  # 获取作者所有文章页面
        Articles = self.parser.GetArticles(s3)  # 获得所有文章链接及年份列表
        for lists in Articles:
            print("进入文章")
            link = lists[0]
            nian = lists[1]
            s4 = ses.get(link, timeout=60)  # 获取文章详细信息页面
            emailnotparse, suoxie = self.parser.GetEmail(s4)  # 得到加密的邮件地址
            if emailnotparse != None:
                if bianhao != 0:
                    print('第' + str(bianhao) + '作者')
                print('文献数：' + wenxin + ' ' + lishi)
                print(AuthorName)
                print("缩写：" + suoxie)
                print(area)
                email = strip_email_protection(emailnotparse['href'])
                print(email)
                # print('<a href=\''+email+'\'>'+email+'></a>')
                print('年份: ' + nian + '\n')
                result = [AuthorID, lastname, firstname, university, dept, city, country, email]
                # result = [AuthorName, area, lishi, email, suoxie, nian, wenxin]
                return result
        result = [AuthorID, lastname, firstname, university, dept, city, country, email]
        return result
        # print("没找到邮箱")


class WenxianSpiderMain(object):
    def __init__(self, wenxian):
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.wenxian = wenxian
        self.wenxianparse = self.wenxian.replace(' ', '+')
        self.param = {
            'numberOfFields': '0',
            'src': 's',
            'clickedLink': '',
            'edit': '',
            'editSaveSearch': '',
            'origin': 'searchbasic',
            'authorTab': '',
            'affiliationTab': '',
            'advancedTab': '',
            'scint': '1',
            'menu': 'search',
            'tablin': '',
            'searchterm1': self.wenxianparse,
            'field1': 'TITLE_ABS_KEY',
            'dateType': 'Publication_Date_Type',
            'yearFrom': 'Before+1960',
            'yearTo': 'Present',
            'loadDate': '7',
            'documenttype': 'All',
            'subjects': 'LFSC',
            '_subjects': 'on',
            'subjects': 'HLSC',
            '_subjects': 'on',
            'subjects': 'PHSC',
            '_subjects': 'on',
            'subjects': 'SOSC',
            '_subjects': 'on',
            'st1': self.wenxianparse,
            'st2': '',
            'sot': 'b',
            'sdt': 'b',
            'sl': '101',
            's': 'TITLE-ABS-KEY%28' + self.wenxianparse + '%29',
            # 'sid':0D8A156F36B35369FE6B68BAAA111169.N5T5nM1aaTEF8rE6yKCR3A%3A150
            # searchId:0D8A156F36B35369FE6B68BAAA111169.N5T5nM1aaTEF8rE6yKCR3A%3A150
            # txGid:0D8A156F36B35369FE6B68BAAA111169.N5T5nM1aaTEF8rE6yKCR3A%3A15
            'sort': 'plf-f',
            'originationType': 'b',
            'rr': ''
        }

        self.param2 = {
            'numberOfFields': '0',
            'src': 's',
            'clickedLink': '',
            'edit': '',
            'editSaveSearch': '',
            'origin': 'searchbasic',
            'authorTab': '',
            'affiliationTab': '',
            'advancedTab': '',
            'scint': '1',
            'menu': 'search',
            'tablin': '',
            'searchterm1': self.wenxian,
            'field1': 'TITLE_ABS_KEY',
            'dateType': 'Publication_Date_Type',
            'yearFrom': 'Before 1960',
            'yearTo': 'Present',
            'loadDate': '7',
            'documenttype': 'All',
            'authSubject': 'LFSC',
            '_authSubject': 'on',
            'authSubject': 'HLSC',
            '_authSubject': 'on',
            'authSubject': 'PHSC',
            '_authSubject': 'on',
            'authSubject': 'SOSC',
            '_authSubject': 'on',
            'st1': self.wenxian,
            'st2': '',
            'sot': 'b',
            'sdt': 'b',
            'sl': '101',
            's': 'TITLE-ABS-KEY({0})'.format(self.wenxian),
            # sid:558EDC31DD2FC5442E4523A31F75350C.N5T5nM1aaTEF8rE6yKCR3A:70
            # searchId:558EDC31DD2FC5442E4523A31F75350C.N5T5nM1aaTEF8rE6yKCR3A:70
            # txGid:558EDC31DD2FC5442E4523A31F75350C.N5T5nM1aaTEF8rE6yKCR3A:7
            'sort': 'plf-f',
            'originationType': 'b',
            'rr': ''
        }

    # 输入文献名称爬取

    def craw(self, idlist=[], file_mode=False, file_mode2=False):
        root = 'https://www.scopus.com/results/results.uri'
        ses = requests.session()  # 创建session
        # ses.proxies={'https':'http://127.0.0.1:1085'}
        s = ses.get(root, params=self.param2, timeout=60)  # 搜索得到文献列表页面
        soup = BeautifulSoup(s.text, 'html.parser')
        span = soup.find_all('span', class_='docTitle')
        if len(span) == 0:
            print("找不到文献")
            return
        elif len(span) == 1:
            link = span[0].a['href']
        else:
            bianhao = 0
            links = []
            mark = 0
            link = ''
            nameoffirst = 'if you see me, no result'
            for spans in span:
                bianhao += 1
                links.append(spans.a['href'])
                biaoti = spans.a.text.strip().replace('\n', '')
                if bianhao == 1:
                    nameoffirst = biaoti  # 存下第一篇的标题，用于文件模式

                # 替换掉可能影响判断的字符
                if biaoti.lower().replace(' ', '').replace('.', '').replace(',', '').replace('-',
                                                                                             '') == self.wenxian.lower().replace(
                        ' ', '').replace('.', '').replace(',', '').replace('-', ''):
                    mark = 1
                    link = spans.a['href']
                    break
                zuozhemen = spans.parent.parent.find('div', class_='dataCol3').span.text.strip().replace('\n', '')
                nian = spans.parent.parent.find('div', class_='dataCol4').span.text.strip().replace('\n', '')
                if spans.parent.parent.find('div', class_='dataCol5').span.a is None:
                    kan = str(spans.parent.parent.find('div', class_='dataCol5').span.string).strip().replace('\n', '')
                else:
                    kan = spans.parent.parent.find('div', class_='dataCol5').span.a.text.strip().replace('\n', '')
                if not file_mode:
                    print('编号：' + str(bianhao) + ' 标题：' + biaoti + ' 作者：' + zuozhemen + ' 年份：' + nian + ' 出版刊物：' + kan)
            if mark == 0:
                if not file_mode:
                    link = links[int(input('输入编号：')) - 1]
                else:
                    print(nameoffirst)
                    link = links[0]  # 都不匹配时，文件模式默认选择第一个
        s2 = ses.get(link)  # 进入文章页面
        # fout = open('output4.html', 'w',encoding="UTF-8")
        # fout.write(s2.text)
        soup2 = BeautifulSoup(s2.text, 'html.parser')
        atitles = soup2.find('div', id='authorlist').find_all('a', title='Show Author Details')

        spi = SpiderMain('a', 'b')  # 创建对象
        sum = 0
        authors = []
        for atitle in atitles:
            authorId = re.findall(r'authorId=\w+&', atitle['href'])[0].replace('authorId=', '').replace('&', '')
            sum += 1
            if authorId not in idlist:

                idlist.append(authorId)

                # print('第'+str(sum)+'作者')
                if file_mode2:
                    author = {}
                    AuthorName, area, lishi, email, suoxie, nian, wenxin = spi.crawel(ses, authorId, sum)
                    if email == '':
                        continue
                    author["AuthorName"] = AuthorName
                    author["area"] = area
                    author["lishi"] = lishi
                    author["email"] = email
                    author["suoxie"] = suoxie
                    author["nian"] = nian
                    author["wenxin"] = wenxin
                    authors.append(author)
                else:
                    spi.crawel(ses, authorId, sum)  # 利用得到的authorid复用SpiderMain中的方法
        return authors


class wenxianSpiderMain2(object):
    def __init__(self, wenxian):
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.wenxian = wenxian
        self.wenxianparse = self.wenxian.replace(' ', '+')
        self.param = {
            'numberOfFields': '0',
            'src': 's',
            'clickedLink': '',
            'edit': '',
            'editSaveSearch': '',
            'origin': 'searchbasic',
            'authorTab': '',
            'affiliationTab': '',
            'advancedTab': '',
            'scint': '1',
            'menu': 'search',
            'tablin': '',
            'searchterm1': self.wenxianparse,
            'field1': 'TITLE_ABS_KEY',
            'dateType': 'Publication_Date_Type',
            'yearFrom': 'Before+1960',
            'yearTo': 'Present',
            'loadDate': '7',
            'documenttype': 'All',
            'subjects': 'LFSC',
            '_subjects': 'on',
            'subjects': 'HLSC',
            '_subjects': 'on',
            'subjects': 'PHSC',
            '_subjects': 'on',
            'subjects': 'SOSC',
            '_subjects': 'on',
            'st1': self.wenxianparse,
            'st2': '',
            'sot': 'b',
            'sdt': 'b',
            'sl': '101',
            's': 'TITLE-ABS-KEY%28' + self.wenxianparse + '%29',
            # 'sid':0D8A156F36B35369FE6B68BAAA111169.N5T5nM1aaTEF8rE6yKCR3A%3A150
            # searchId:0D8A156F36B35369FE6B68BAAA111169.N5T5nM1aaTEF8rE6yKCR3A%3A150
            # txGid:0D8A156F36B35369FE6B68BAAA111169.N5T5nM1aaTEF8rE6yKCR3A%3A15
            'sort': 'plf-f',
            'originationType': 'b',
            'rr': ''
        }

        self.param2 = {
            'numberOfFields': '0',
            'src': 's',
            'clickedLink': '',
            'edit': '',
            'editSaveSearch': '',
            'origin': 'searchbasic',
            'authorTab': '',
            'affiliationTab': '',
            'advancedTab': '',
            'scint': '1',
            'menu': 'search',
            'tablin': '',
            'searchterm1': self.wenxian,
            'field1': 'TITLE_ABS_KEY',
            'dateType': 'Publication_Date_Type',
            'yearFrom': 'Before 1960',
            'yearTo': 'Present',
            'loadDate': '7',
            'documenttype': 'All',
            'authSubject': 'LFSC',
            '_authSubject': 'on',
            'authSubject': 'HLSC',
            '_authSubject': 'on',
            'authSubject': 'PHSC',
            '_authSubject': 'on',
            'authSubject': 'SOSC',
            '_authSubject': 'on',
            'st1': self.wenxian,
            'st2': '',
            'sot': 'b',
            'sdt': 'b',
            'sl': '101',
            's': 'TITLE-ABS-KEY({0})'.format(self.wenxian),
            # sid:558EDC31DD2FC5442E4523A31F75350C.N5T5nM1aaTEF8rE6yKCR3A:70
            # searchId:558EDC31DD2FC5442E4523A31F75350C.N5T5nM1aaTEF8rE6yKCR3A:70
            # txGid:558EDC31DD2FC5442E4523A31F75350C.N5T5nM1aaTEF8rE6yKCR3A:7
            'sort': 'plf-f',
            'originationType': 'b',
            'rr': ''
        }

    def craw(self, idlist=[], file_mode2=False):
        root = 'https://www.scopus.com/results/results.uri'
        ses = requests.session()  # 创建session
        # ses.proxies={'https':'http://127.0.0.1:1085'}
        s = ses.get(root, params=self.param2, timeout=60)  # 搜索得到文献列表页面
        soup = BeautifulSoup(s.text, 'html.parser')
        span = soup.find_all('span', class_='docTitle')
        if len(span) == 0:
            print("找不到文献")
            return
        else:
            bianhao = 0
            mark = 0
            nameoffirst = 'if you see me, no result'
            authors = []
            for spans in span:
                try:
                    bianhao += 1
                    link = spans.a['href']
                    biaoti = spans.a.text.strip().replace('\n', '')

                    zuozhemen = spans.parent.parent.find('div', class_='dataCol3').span.text.strip().replace('\n', '')
                    nian = spans.parent.parent.find('div', class_='dataCol4').span.text.strip().replace('\n', '')
                    if spans.parent.parent.find('div', class_='dataCol5').span.a is None:
                        kan = str(spans.parent.parent.find('div', class_='dataCol5').span.string).strip().replace('\n',
                                                                                                                  '')
                    else:
                        kan = spans.parent.parent.find('div', class_='dataCol5').span.a.text.strip().replace('\n', '')
                    print(biaoti)
                    s2 = ses.get(link)  # 进入文章页面
                    soup2 = BeautifulSoup(s2.text, 'html.parser')
                    atitles = soup2.find('div', id='authorlist').find_all('a', title='Show Author Details')

                    spi = SpiderMain('a', 'b')  # 创建对象
                    sum = 0

                    for atitle in atitles:
                        authorId = re.findall(r'authorId=\w+&', atitle['href'])[0].replace('authorId=', '').replace('&',
                                                                                                                    '')
                        sum += 1
                        if authorId not in idlist:
                            idlist.append(authorId)
                            # print('第'+str(sum)+'作者')
                            author = {}
                            AuthorName, area, lishi, email, suoxie, nian, wenxin = spi.crawel(ses, authorId, sum)
                            if email == '':
                                continue
                            author["AuthorName"] = AuthorName
                            author["area"] = area
                            author["lishi"] = lishi
                            author["email"] = email
                            author["suoxie"] = suoxie
                            author["nian"] = nian
                            author["wenxin"] = wenxin
                            authors.append(author)
                except Exception as e:
                    print('出现error')
                    continue
                finally:
                    print('\n\n\n\n')
        return sorted(authors, key=lambda author: int(author["wenxin"]), reverse=True)


class WenjianSpiderMain(object):
    def __init__(self, f_in):
        self.f_in = f_in
        # self.f_out=f_out

    def craw(self):
        idlist = []
        lines = self.f_in.readlines()
        # print(lines)
        for line in lines:
            try:
                wenxian = line.rstrip('\n')
                if wenxian == '':
                    continue
                print(wenxian)
                obj_spider = WenxianSpiderMain(wenxian)
                obj_spider.craw(idlist, True)
            except Exception as e:
                print('出现error ', end='')
                print(e)
                continue
            finally:
                print('\n\n\n\n')


class AuthorSpiderMain(object):
    def __init__(self, f_in):
        self.f_in = f_in
        # self.f_out=f_out

    def craw(self):
        idlist = []
        lines = self.f_in.readlines()
        with open('resultpart2.csv', 'w') as csvout:
            header = ['authorid', 'lastname', 'firstname', 'university', 'dept', 'city', 'country', 'email']
            # header = ['AuthorName', 'area', 'lishi', 'email', 'suoxie', 'nian', 'wenxin']
            writer = csv.writer(csvout, dialect='excel')
            writer.writerow(header)
            for line in lines:
                time.sleep(15)
                try:
                    authorid = line.rstrip('\n')
                    if authorid == '':
                        continue
                    print(authorid)
                    obj_spider = AuthorIDSpiderMain(authorid)
                    result = obj_spider.craw()
                    writer.writerow(result)
                except Exception as e:
                    print('出现error ', end='')
                    print(e)
                    writer.writerow([authorid, e])
                    continue
                finally:
                    print('\n\n\n\n')


class WenjianSpiderMain2(object):
    def __init__(self, f_in):
        self.f_in = f_in
        # self.f_out=f_out

    def craw(self):
        authors = []
        idlist = []
        lines = self.f_in.readlines()
        # print(lines)
        for line in lines:
            try:
                wenxian = line.rstrip('\n')
                if wenxian == '':
                    continue
                print(wenxian)
                obj_spider = WenxianSpiderMain(wenxian)
                authors += obj_spider.craw(idlist, True, True)
            except Exception as e:
                print('出现error ', end='')
                print(e)
                continue
            finally:
                print('\n\n\n\n')
        return authors


def seperatename(name):
    # 获取姓和名
    namelist = name.strip().split()
    xing = namelist[-1]
    namelist.pop()
    ming = " ".join(namelist)
    return xing, ming


def strip_email_protection(s):
    # 解密邮件地址
    fp = re.findall(r'email-protection#[A-Za-z0-9]+', s)
    # parse email
    fp = fp[0].replace('email-protection#', '')
    # print(fp)

    r = int(fp[:2], 16)
    email = ''.join([chr(int(fp[i:i + 2], 16) ^ r) for i in range(2, len(fp), 2)])
    # m = re.sub(r'<a class="__cf_email__".*?</a>', email, s)
    # #strip <script>
    # m = re.sub('<script.*?</script>', '', s, flags = re.DOTALL)
    return email


def zuozhe_mode():
    # 通过输入人名查找审稿人
    # 形如'hong, weirong'姓在前，不带逗号的姓在后
    namelist = input("人名: ").split(',')
    namelist.reverse()
    name = ' '.join([i.strip() for i in namelist])
    if name == 'exit':
        exit()
    xing, ming = seperatename(name)
    # ming=seperatename(name)[1]
    obj_spider = SpiderMain(xing, ming)
    obj_spider.craw()


def wenxian_mode():
    # 通过输入文献查找审稿人
    wenxian = input('文献标题：').strip()
    if wenxian == 'exit':
        exit()
    obj_spider = WenxianSpiderMain(wenxian)
    obj_spider.craw()


def wenjian_mode():
    # 通过读取分行写好需要爬的文献名，循环爬取审稿人信息，输出文档。
    f_in = open('spider.txt', 'r',
                encoding='utf-8')  # 不加encoding会出现UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 in position
    # f_out=open('result.txt','w')
    try:
        # 传入文件对象
        # obj_spider=WenjianSpiderMain(f_in,f_out)
        obj_spider = WenjianSpiderMain(f_in)
        obj_spider.craw()
    finally:
        f_in.close()
        # f_out.close()


def author_mode():
    # 通过读取分行写好需要爬的文献名，循环爬取审稿人信息，输出文档。
    f_in = open('authors.txt', 'r',
                encoding='utf-8')  # 不加encoding会出现UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 in position
    # f_out=open('result.csv', 'wb')
    try:
        # 传入文件对象
        # obj_spider=AuthorSpiderMain(f_in,f_out)
        obj_spider = AuthorSpiderMain(f_in)
        obj_spider.craw()
    finally:
        f_in.close()
        # f_out.close()


def wenjian_mode2():
    f_in = open('spider.txt', 'r', encoding='utf-8')

    try:
        # 传入文件对象
        # obj_spider=WenjianSpiderMain(f_in,f_out)
        obj_spider2 = WenjianSpiderMain2(f_in)
        authors = obj_spider2.craw()

        # 以文献数大小排序
        authors = sorted(authors, key=lambda author: int(author["wenxin"]), reverse=True)
    finally:
        f_in.close()
        return authors


def wenxian_mode2():
    wenxian = input('文献模糊标题：').strip()
    if wenxian == 'exit':
        exit()
    obj_spider = wenxianSpiderMain2(wenxian)
    authors = obj_spider.craw()
    return authors


if __name__ == "__main__":

    while True:
        print()
        print('编号1为人名模式，编号2为文献模式，编号3为文件模式，编号4为按发表数排列输出的文件模式，编号5为模糊文献模式，编号6为id模式，输入exit退出')
        flag = input('输入编号：').strip()
        if flag == str(1):
            zuozhe_mode()
        elif flag == str(2):
            wenxian_mode()
        elif flag == str(3):
            print('*************************')
            print('读取spider.txt...')
            wenjian_mode()
        elif flag == str(4):
            print('*************************')
            print('读取spider.txt...')
            authors = wenjian_mode2()
            print("\n\n\n\n排序后")
            for author in authors:
                print('文献数：' + author["wenxin"] + ' ' + author['lishi'])
                print(author['AuthorName'])
                print("缩写：" + author['suoxie'])
                print(author['area'])
                print(author['email'])
                # print('<a href=\''+email+'\'>'+email+'></a>')
                print('年份: ' + author['nian'] + '\n')
                print('\n\n')
        elif flag == str(5):
            authors = wenxian_mode2()
            print("\n\n\n\n排序后")
            for author in authors:
                print('文献数：' + author["wenxin"] + ' ' + author['lishi'])
                print(author['AuthorName'])
                print("缩写：" + author['suoxie'])
                print(author['area'])
                print(author['email'])
                # print('<a href=\''+email+'\'>'+email+'></a>')
                print('年份: ' + author['nian'] + '\n')
                print('\n\n')
        elif flag == str(6):
            print('*************************')
            print('读取authorsid.txt...')
            author_mode()
        elif flag == 'exit':
            exit()
        else:
            print('输入不符合要求，重新输入')
