# encoding: utf-8
from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Mp, User, Article
from . import api
from flask_security import auth_token_required
from fetchArticles import fetchArticle
from datetime import datetime, timedelta
import time

@api.route('/mps', methods=['POST'])
@auth_token_required
def new_mps():
    email = request.get_json()['email']
    user = User.query.filter_by(email=email).first()
    Mps = Mp.from_json(request.json)
#    subscribed_mps = user.subscribed_mps
    subscribed_mps_weixinhao = [i.weixinhao for i in user.subscribed_mps]
    rsp = []
    for mp in Mps:
	    mp_sql = Mp.query.filter_by(weixinhao=mp.weixinhao).first()
#	    print mp.weixinhao,  mp.weixinhao in subscribed_mps_weixinhao
	# 如果不存在这个订阅号，则添加到Mp，并订阅
	    if mp_sql is None:
	    		db.session.add(mp)
	    		user.subscribe(mp)
	    		rsp.append(mp.to_json())
	    		db.session.commit()
	# aync update Articles
	    		mp_sql = Mp.query.filter_by(weixinhao=mp.weixinhao).first()	# 此mp跟初始的 mp已经是不同对像
	    		[ok, return_str] = fetchArticle(mp_sql, 'async')

	# 如果用户没有订阅，则订阅
	    elif not mp.weixinhao in subscribed_mps_weixinhao:
	    		user.subscribe(mp_sql)
	    		rsp.append(mp.to_json())
	    		db.session.commit()
	# aync update Articles
	    		[ok, return_str] = fetchArticle(mp, 'async')

     # TODO: 删除不再订阅的公众号



    return jsonify(rsp), 201, \
        {'Location': url_for('api.get_mps', id=mp.id, _external=True)}


# 带 /mps/ 斜杠的，必须放在 /mps POST后面，不然默认会选择以下GET
@api.route('/mps/')
@auth_token_required
def get_mps():
	# request.args.items().__str__()
	email = request.args.get('email')
	print email
	mps = User.query.filter_by(email=email).first().subscribed_mps
	mps_list = [ mp.to_json() for mp in mps ]
	print mps_list
	return jsonify(mps_list)

@api.route('/articles')
@auth_token_required
def get_articles():
	# request.args.items().__str__()
#	time.sleep(3)
	weixinhao = request.args.get('weixinhao')
	print 'fetch articles of ', weixinhao
	mp = Mp.query.filter_by(weixinhao=weixinhao).first()
	if mp is not None:
		if request.args.get('action') == 'sync':
			print '================sync'
			if datetime.utcnow() - mp.sync_time > timedelta(seconds=60*5):
				[ok, return_str] = fetchArticle(mp, 'sync')
				print ok, return_str
				# 需要重新获取mp对象，
				#DetachedInstanceError: Instance <Mp at 0x5d769b0> is not bound to a Session; attribute refresh operation cannot proceed
				mp = Mp.query.filter_by(weixinhao=weixinhao).first()
			else: 
				print '========== less than 5 mins, not to sync'
#			return jsonify(return_str)
		articles = Article.query.filter(Article.mp_id == mp.id)
		articles_list = [ a.to_json() for a in articles ]
		rsp = {
			'status': 'ok',
			'articles': articles_list,
			'sync_time': time.mktime(mp.sync_time.timetuple()) + 3600*8	# GMT+8
		}
	#	print articles_list
		return jsonify(rsp)
	else:
		rsp = {
			'status': 'mp not found!'
		}
		return jsonify(rsp)

