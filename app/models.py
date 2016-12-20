# encoding: utf-8
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager

# 订阅公众号和User是多对多关系
class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    # follower_id
    subscriber_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    # followed_id
    mp_id = db.Column(db.Integer, db.ForeignKey('mps.id'),
                            primary_key=True)
    subscribe_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    mps = db.relationship('Subscription',
                               foreign_keys=[Subscription.subscriber_id],
                               backref=db.backref('subscriber', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def subscribe(self, mp):
        if not self.is_subscribing(mp):
            f = Subscription(subscriber_id=self.id, mp_id=mp.id)
            db.session.add(f)

    def unsubscribe(self, mp):
        f = Subscription.filter_by(subscriber_id=self.id, mp_id=mp.id).first()
        if f:
            db.session.delete(f)

    def is_subscribing(self, mp):
        return self.mps.filter_by(mp_id=mp.id).first() is not None

    @property
    def subscribed_mps(self):
        return Mp.query.join(Subscription, Subscription.mp_id == Mp.id)\
            .filter(Subscription.subscriber_id == self.id)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts': url_for('api.get_user_posts', id=self.id, _external=True),
            'followed_posts': url_for('api.get_user_followed_posts',
                                      id=self.id, _external=True),
            'post_count': self.posts.count()
        }
        return json_user

    def __repr__(self):
        return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 公众号
class Mp(db.Model):
    __tablename__ = 'mps'
    id = db.Column(db.Integer, primary_key=True)
    weixinhao = db.Column(db.Text)
    image = db.Column(db.Text)
    summary = db.Column(db.Text)
    sync_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    articles = db.relationship('Article', backref='mp', lazy='dynamic')
    subscribers = db.relationship('Subscription',
                               foreign_keys=[Subscription.mp_id],
                               backref=db.backref('mp', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True),
            'comments': url_for('api.get_post_comments', id=self.id,
                                _external=True),
            'comment_count': self.comments.count()
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Post(body=body)

# 公众号的文章
class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    image = db.Column(db.Text)
    summary = db.Column(db.Text)
    url = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    mp_id = db.Column(db.Integer, db.ForeignKey('mps.id'))

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id, _external=True),
            'post': url_for('api.get_post', id=self.post_id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True),
        }
        return json_comment

    @staticmethod
    def from_json(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise ValidationError('comment does not have a body')
        return Comment(body=body)

"""
In [1]: u=User()

In [2]: u
Out[2]: <User None>

In [3]: u.password="cat"

In [4]: u.password_hash
Out[4]: 'pbkdf2:sha1:1000$7QUJktd8$4c947175478983d70c939512d22b43d54d9b6e57'

In [5]: u2=User()

In [7]: u2.password="cat"

In [8]: u2.password_hash
Out[8]: 'pbkdf2:sha1:1000$HLSGLeRg$461c67ddf0f78fda561f74ffd94374d215009593'

In [10]: db.session.add(u)
In [11]: db.session.add(u2)
In [13]: db.session.commit()

In [1]: f= User.query.filter_by(id='1').first()
In [15]: f
Out[15]: <User u'Kevin'>

In [9]: f.subscribed_mps.count()
Out[9]: 2

In [16]: f.subscribed_mps.all()[0].id
Out[16]: 2

In [23]: b= Mp.query.filter_by(id='2').first()

In [24]: b.articles
Out[24]: <sqlalchemy.orm.dynamic.AppenderBaseQuery at 0x6ba69e8>

In [25]: b.articles.
b.articles.add_column          b.articles.exists              b.articles.merge_result        b.articles.statement
b.articles.add_columns         b.articles.extend              b.articles.offset              b.articles.subquery
b.articles.add_entity          b.articles.filter              b.articles.one                 b.articles.suffix_with
b.articles.all                 b.articles.filter_by           b.articles.one_or_none         b.articles.union
b.articles.append              b.articles.first               b.articles.options             b.articles.union_all
b.articles.as_scalar           b.articles.first_or_404        b.articles.order_by            b.articles.update
b.articles.attr                b.articles.from_self           b.articles.outerjoin           b.articles.value
b.articles.autoflush           b.articles.from_statement      b.articles.paginate            b.articles.values
b.articles.column_descriptions b.articles.get                 b.articles.params              b.articles.whereclause
b.articles.correlate           b.articles.get_or_404          b.articles.populate_existing   b.articles.with_entities
b.articles.count               b.articles.group_by            b.articles.prefix_with         b.articles.with_for_update
b.articles.cte                 b.articles.having              b.articles.query_class         b.articles.with_hint
b.articles.delete              b.articles.instance            b.articles.remove              b.articles.with_labels
b.articles.dispatch            b.articles.instances           b.articles.reset_joinpoint     b.articles.with_lockmode
b.articles.distinct            b.articles.intersect           b.articles.scalar              b.articles.with_parent
b.articles.enable_assertions   b.articles.intersect_all       b.articles.select_entity_from  b.articles.with_polymorphic
b.articles.enable_eagerloads   b.articles.join                b.articles.select_from         b.articles.with_session
b.articles.except_             b.articles.label               b.articles.selectable          b.articles.with_statement_hint
b.articles.except_all          b.articles.limit               b.articles.session             b.articles.with_transformation
b.articles.execution_options   b.articles.logger              b.articles.slice               b.articles.yield_per
"""