#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint # logを出力
import twitter # python-twitterライブラリを読み込んでいる
import time

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# TwitterAPI認証
api = twitter.Api(
	consumer_key=os.environ.get("API_KEY"),
	consumer_secret=os.environ.get("API_SECRET"),
	access_token_key=os.environ.get("ACCESS_TOKEN"),
	access_token_secret=os.environ.get("ACCESS_SECRET")
)

# どのユーザーで認証しているのか確認する
# CheckAuthUser
user = api.VerifyCredentials() 
pprint.pprint(user)

# ツイートする
count = 0
while count < 30:
	count += 1
	api.PostUpdate('Hello world '+str(time.time()))


ratelimit = twitter.ratelimit.RateLimit()
def getTweet(max_id):
	# ツイートを取得する
	# ツイートは配列
	mytweets = api.GetUserTimeline(screen_name='todesking', max_id=max_id)
	pprint.pprint(len(mytweets))
	# 取得した中で一番過去のツイート
	oldTweet = None
	for tweet in mytweets:
		pprint.pprint(tweet.text)
		#pprint.pprint(tweet.id)
		oldTweet = tweet
		#api.DestroyStatus(tweet.id)
		try:
			api.CreateFavorite(tweet)
		except Exception as e:
			pprint.pprint(e)
	
	print('update limit: '+str(ratelimit.get_limit('/statuses/update.json')))
	print('timeline limit: '+str(ratelimit.get_limit('/statuses/user_timeline.json')))
	# 再帰
	# 関数の中で関数を呼び出すと無限ループになる
	if oldTweet is not None and len(mytweets) != 1:
		getTweet(oldTweet.id)

getTweet(None)



"""
# todeskingのツイートを取得する
todeskingtweets = api.GetUserTimeline(screen_name="todesking")
# for...in文でループする
for tweet in todeskingtweets:
	pprint.pprint(tweet.text)
	pprint.pprint(tweet.id)
	# api.CreateFavorite(tweet)
	api.PostRetweet(tweet.id)
"""

"""
 
#CSVの読み込み
csvReader = csv.reader(open('ファイル名.csv', 'r'))
 
#CSVを一行ずつ処理
for row in csvReader:
	print(row[0], "/", row[2])	#TweetIDと内容を表示
 
	#RTは全削除
	if "RT @" in row[2]:
		#例外処理
		try:
			api.DestroyStatus(row[0])	#ツイートの削除を試みる
			print(u"■RT削除成功！")
		except:
			print(u"■既に削除済みのようです")
 
	#画像つきツイートは削除しない
	elif "pic.twitter.com" in row[2]:
		print(u"■けさないよ！")
 
	#画像なしツイートは削除
	else:
		#例外処理
		try:
			api.DestroyStatus(row[0])	#ツイートの削除を試みる
			print(u"■削除成功！")
		except:
			print(u"■既に削除済みのようです")
 
#処理が終わった時の処理
else:
	print(u"■おしまい！")
"""