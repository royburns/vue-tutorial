# -*- coding: utf-8 -*-
# 17197602@qq.com

from threading import Thread
from flask import current_app
import time, random, requests, traceback, re, json, random, os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
from ..models import Mp, Article
from .. import create_app, db

user_agent = {
    'User-agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.0 Chrome/30.0.1599.101 Safari/537.36'}
user_agent2 = { 'Content-Type': 'application/json'}

def fetchArticle(mp, sync):
	app = current_app._get_current_object()
	return_str = 'start to fetch MP: %s ...' % (mp.weixinhao)
	try:
		if sync == 'async':
			thr = Thread(target=article_search, args=[app, db, mp.weixinhao])
			thr.start()
			return ['ok', return_str]
		else:
			article_search(app, db, mp.weixinhao)
			return ['ok', u'同步完成！']
	except Exception, e:
		print e
		return ['nok', str(e)]

def article_search(app, db, weixinhao):
	uin = os.environ.get('WXUIN', '')
	with app.app_context():
		# Mp object不能带到Thread中，需要重新query一下
		mp = db.session.query(Mp).filter(Mp.weixinhao == weixinhao).first()
		print '========= seaching articles of MP: ', mp.mpName
		s = requests.Session()
		search_url = 'http://weixin.sogou.com/weixinwap?page=1&_rtype=json&ie=utf8&type=1&query=%s' % mp.weixinhao
		encGzhUrl = mp.encGzhUrl
		trycnt = 0
		while trycnt<5 :
			r = s.get(encGzhUrl, headers=user_agent)
			soup = BeautifulSoup(r.text, 'lxml')
			print soup.title.text, search_url, encGzhUrl
			if soup.title.text == u'请输入验证码 ':
				trycnt +=1
				sleepcnt = random.randint(30,60)*trycnt
				print 'No. %d: sleeping %d seconds, before next search...' % (trycnt, sleepcnt)
				time.sleep(sleepcnt)
#			elif soup.title.text == u''	# title =='' is: 链接已过期
			elif soup.title.text == mp.mpName+' ': 
				break
			# 重新搜索 weixinhao
			r = s.get(search_url, headers=user_agent2)
			# 每次search需要隔10s以上
			# 用户您好，您的访问过于频繁，为确认本次访问为正常用户行为，需要您协助验证。http://www.doc00.com/doc/100100a35
			j = json.loads(r.text)
			for ii in j['items']:
				soup = BeautifulSoup(ii, 'xml')
				if soup.weixinhao.text == mp.weixinhao:
					break
			encGzhUrl = soup.encGzhUrl.text
			# TODO: update encGzhUrl	
			db.session.query(Mp).filter(Mp.weixinhao == mp.weixinhao).update({Mp.encGzhUrl:encGzhUrl })
			
		if (trycnt >= 5) and (soup.title.text == u'请输入验证码 '):
			return False
		reg = r'var msgList = ({.*?]});'  #var msgList = {"list ...tus":2,"type":49}}]};
		infos = re.findall(reg, soup.text)
		articles = json.loads(infos[0]).get('list')
		print articles[0][u'app_msg_ext_info'].keys()
		article = {}
		for aa in articles:
			article['title'] = aa.get('app_msg_ext_info')['title']
			article['author'] = aa.get('app_msg_ext_info')['author']
			article['cover'] = aa.get('app_msg_ext_info')['cover']	# 图片
			article['digest'] = aa.get('app_msg_ext_info')['digest']	# 摘要
			article['timestamp'] = aa['comm_msg_info']['datetime']
			article['source_url'] = aa.get('app_msg_ext_info')['source_url']	# 转载的，阅读原文
			article['content_url'] = 'http://mp.weixin.qq.com' + HTMLParser().unescape(aa.get('app_msg_ext_info')['content_url']) + '&uin=%s'%uin
			article['content_url'] = get_permanent_url(article['content_url'])
			article['fileid'] = aa.get('fileid')
#			print 'content_url:', article['content_url']
			article_row = db.session.query(Article).filter(Article.title == article['title']).first()
#			print 'article_row.mp_id', article_row.mp_id, article_row.title
			if article_row and article_row.mp_id is None:	# 有时候数据库里，有Article记录，但这些记录没有关联MP
				db.session.query(Article).filter(Article.title == article['title']).update({
                        	Article.mp_id: mp.id,
				})
			elif article_row is None:
#			if db.session.query(Article).filter(Article.title == article['title']).first() == None:
				try: print u'发现新的article:', article['title']
				except: pass
				db.session.add(Article(title=article['title'], cover=article['cover'], digest=article['digest'], timestamp=article['timestamp'], 
					author=article['author'], source_url=article['source_url'], content_url=article['content_url'], fileid=article['fileid'], mp_id=mp.id, ))
#		    		db.session.commit()
	    		# 如果有嵌套的article:
			if aa['app_msg_ext_info'].get('multi_app_msg_item_list'):
				timestamp = article['timestamp']
				arr = aa['app_msg_ext_info'].get('multi_app_msg_item_list')
				for item in arr:
					try: print u'嵌套的article:', item['title'], item['source_url'], item['content_url'], item['digest']
					except: pass
					content_url = 'http://mp.weixin.qq.com' + HTMLParser().unescape(item['content_url']) + '&uin=%s'%uin
					content_url = get_permanent_url(content_url)
					article_row = db.session.query(Article).filter(Article.title == item['title']).first()
					if article_row and article_row.mp_id is None:	# 有时候数据库里，有Article记录，但这些记录没有关联MP
						db.session.query(Article).filter(Article.title == item['title']).update({
		                        	Article.mp_id: mp.id,
						})
					elif article_row is None:
#					if db.session.query(Article).filter(Article.title == item['title']).first() == None:
						db.session.add(Article(title=item['title'], cover=item['cover'], digest=item['digest'], timestamp=timestamp,
							author=item['author'], source_url=item['source_url'], fileid=item['fileid'], content_url=content_url, mp_id=mp.id, ))
			db.session.commit()
		db.session.query(Mp).filter(Mp.weixinhao == mp.weixinhao).update({Mp.sync_time:datetime.utcnow() })
		db.session.commit()
		return True

def get_permanent_url(pre_redirect_url):
	response = requests.head(pre_redirect_url)
	permanent_url = response.headers['Location']
	return permanent_url

def send_async_email(app, msg):
    # with app.app_context():
    #     mail.send(msg)
    print

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def fetchty_async(app, db, tb, p):
    with app.app_context():
        time.sleep(random.randint(1, 3))
        # p2 = Ty5439941.query.first()
        print '============ last page:', tb.query.order_by(tb.page.desc()).first().page
        lastpost = tb.query.order_by(tb.page.desc()).first()
        a = tb(page=lastpost.page+1, floors='{}')
        db.session.add(a)
        # db.session.query(tb).filter(tb.page == lastpost.page).update(lastpost)
        db.session.commit()
        print '=========== db updated'

def fetchty(Article, a_type, author):
    AUTHOR = author
    Article = Article
    a_type = a_type
    urlsession = requests.Session()
    app = current_app._get_current_object()
    lastpost = Article.query.order_by(Article.page.desc()).first()
    try:
        if lastpost:  # and lastpost.page>1: #如果已经有数据
            previous_page = lastpost.page
            # db.session.delete(lastpost)	# 清空最后一page
            # db.session.commit()
            print '====== current last page:', previous_page
            # print '====== now last page is:', Ty556242.query.order_by(Ty556242.page.desc()).first().page
            url = 'http://bbs.tianya.cn/post-%s-%s-1.shtml' % (a_type, Article.articleId)  # #ty_vip_look[21035714]'
            r = urlsession.get(url, headers=user_agent)
            soup = BeautifulSoup(r.text, "html.parser")
            # print soup.select('div.atl-pages > form > a')
            maxpage = int(soup.select('div.atl-pages > form > a')[-2].text)
            return_str = 'start to fetch bbs<%s> from page %d to %d ...' % (Article.articleId, previous_page, maxpage)
            print return_str

            for page in range(previous_page, maxpage + 1):
                # page_content = bbs_search2(pg, urlsession, AUTHOR, articleId, type)
                thr = Thread(target=bbs_search2, args=[app, db, Article, page, previous_page, urlsession, AUTHOR, a_type])
                thr.start()
#                time.sleep(random.random())
                if page%10 == 0:
                    print '==== ten fetchty jobs ongoing, add additional wait...'
                    time.sleep(random.random())
                    # time.sleep(random.randint(1, 5))
                    db.session.commit() # 每10页 commit 一次
            print '====================== Done'
            db.session.commit()
            return ['ok', return_str]
        else:
            return_str = u"============ <%s> empty table, will add first page only. 请再次 /ip? 更新后续页面" % (Article.articleId)
            print return_str
            thr = Thread(target=bbs_search2,
                         args=[app, db, Article, 1, 0, urlsession, AUTHOR, a_type])
            thr.start()
            return ['ok', return_str]
    except Exception, e:
        print e
        return ['nok', str(e)]



def bbs_search2(app, db, Article, page, previous_page, urlsession, AUTHOR, a_type):
    with app.app_context():
        DEBUG = False
        url = 'http://bbs.tianya.cn/post-%s-%s-%d.shtml'% (a_type, Article.articleId, page)  # #ty_vip_look[21035714]'
        print '============= Page:', page
        r = urlsession.get(url, headers=user_agent)
        soup = BeautifulSoup(r.text, "html.parser")
        eles = soup.select('div.atl-item')
        try:
            floors = {}
            if page==1:
                floor = {}
                timestamp = soup.select('div.atl-info')[0].select('span')[1].text.strip()[-19:] # <span>时间：2011-01-29 22:31:00 </span>
                timestamp = datetime.strptime(timestamp, u"%Y-%m-%d %H:%M:%S") + timedelta(hours=-8)
                floor['timestamp'] = timestamp
                master = soup.select('div.bbs-content')[0].text.strip().replace(u'      ', '<br/>')
                floor['master'] = master
                floor['original'] = ''
                floor['reply'] = ''
                floor['comments'] = {}
                floor['lz_reply'] = False
                floors[0] = floor
                print 0, timestamp, '0 floor'

            for i in eles :
                if i['_host'] == AUTHOR:
                    floor = {}
                    replyid = i['replyid']
                    original, reply, master, lz_reply = ('', '', '', False)
                    #			timestamp = i['js_restime']
                    timestamp = datetime.strptime( i['js_restime'], "%Y-%m-%d %H:%M:%S")+ timedelta(hours=-8) # 中国时区转换为UTC
                    lz_update=timestamp
                    #content = i.select('div.bbs-content')[0]
                    content_raw = str(i.select('div.bbs-content')[0])[25:-6].strip().decode('utf8')
                    content = i.select('div.bbs-content')[0].text.strip()
                    floor_id = int( i.select('div.atl-reply > span')[0].text[:-1] ) # 多少楼
                    if DEBUG: print eles.index(i), timestamp, floor_id, 'floor'
                    rawstr = u"(.*)(<br/?>　　[-]{15,99}<br/?>)(.*)"		# 匹配 <br/>　　-------------<br/>
                    rawstr2 = u"(.*)(<br/?>　　[—]{15,99}<br/?>)(.*)"		# 匹配: u'<br/>　　—————————————————<br/>'
                    match_obj = re.search(rawstr, content_raw)
                    match_obj2 = re.search(rawstr2, content_raw)
                    if match_obj and (content[0]=='@' or  content[:3]==u'作者：' ) :	# 回帖
                        original = match_obj.group(1)
                        splitline = match_obj.group(2)
                        reply = match_obj.group(3)
                        if DEBUG: print u'【原帖】', original
                    elif match_obj2 and (content[0]=='@' or  content[:3]==u'作者：' ) :	# 回帖
                        original = match_obj2.group(1)
                        splitline = match_obj2.group(2)
                        reply = match_obj2.group(3)
                        if DEBUG: print u'【原帖】', original
                    else:
                        if DEBUG: print u'[M]', content
                        master = content_raw.replace(u'<br/>　　<br/>　　', '<br/>')#.replace(u'　　 ', '<br/>')
                    floor['timestamp']=timestamp
                    floor['master']=master
                    floor['original']=original
                    floor['reply']=reply
                    floor['comments']= {}
                    cmt_ele = i.select('div.ir-list > ul > li')
                    commentlist = []
                    cmt_id = 0
                    for cc in cmt_ele:
                        tt = cc['_replytime']
                        if cc['_username'] == AUTHOR:
                            lz_reply = True
                            lz_update = datetime.strptime( tt, "%Y-%m-%d %H:%M:%S")+ timedelta(hours=-8)
                        #						commentlist.append( cc['_username'] + '>>>>'+ cc['_replytime'] + '>>>>' + cc.select('span.ir-content')[0].text)
                        author = cc['_username']
                        comment = cc.select('span.ir-content')[0].text
                        floor['comments'][cmt_id] = {'timestamp': tt, 'author': author, 'comment': comment}
                        cmt_id += 1
                        if DEBUG: print '[CMT]', cmt_id, author

                    try: cmt_page = int( soup.select('div.atl-item')[1].select('span.ir-pageNums > a')[-1]['page'] )	# 评论页数
                    except: cmt_page = 0

                    for ccc in range(2, cmt_page+1):
                        if DEBUG: print u'有多页评论', cmt_page
                        url = 'http://bbs.tianya.cn/api?method=bbs.api.getCommentList&params.item=%s&params.articleId=%s&params.replyId=%s&params.pageNum=%d' \
                              % (a_type, Article.articleId, replyid, ccc)
                        resp = urlsession.get(url, headers=user_agent).text
                        if eval(resp)['success'] == '1':
                            for cccc in eval(resp)['data']:
                                #							commentlist.append(cccc['author_name'].decode('utf8') + '>>>>' + cccc['comment_time'] + '>>>>' + cccc['content'].decode('utf8'))
                                tt = cccc['comment_time']
                                author = cccc['author_name'].decode('utf8')
                                comment = cccc['content'].decode('utf8')
                                floor['comments'][cmt_id] = {'timestamp': tt, 'author': author, 'comment': comment}
                                cmt_id += 1
                                if DEBUG: print '[CMT]', cmt_id, author

                    floor['lz_reply']=lz_reply
                    floors[floor_id] = floor

            last_update = datetime.utcnow()
            #		print [page, floors, last_update, lz_update]
            if floors<>{}:
                p = Article(page=page, floors=str(floors), last_update=last_update, lz_update=lz_update)
                if page == previous_page:
                    db.session.query(Article).filter(Article.page == page).update({
                        Article.floors: str(floors),
                        Article.last_update: last_update,
                        Article.lz_update: lz_update
                    })
                    print '====== previous last page updated!'
                else:
                    db.session.add(p)
                # db.session.commit()
                log_str = '======= Success! <%s> page %d updated/added. Now last page is:%d' % (
                    Article.articleId, page, Article.query.order_by(Article.page.desc()).first().page)
            else:
                log_str = '======= Success! <%s> no update. Author not found in this page:%d'% (Article.articleId, page)
            print log_str
            comment = Logs(name='[Admin.INFO]', email='', comment=log_str, last_access=datetime.utcnow() )
            db.session.add(comment)
            return 'ok'

        except Exception, e:
            log_str = str(e)
            print traceback.print_exc()
            comment = Logs(name='[Admin.ERROR]', email='', comment=log_str, last_access=datetime.utcnow())
            db.session.add(comment)
            return 'nok'
