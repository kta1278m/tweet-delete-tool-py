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

def getTweet(max_id):
  statuses = api.GetUserTimeline(screen_name=user.screen_name, max_id=max_id)
  # for...in文でループする
  oldestTweet = None
  for status in statuses:
    pprint.pprint(status.text)
    pprint.pprint(status.id)
    api.DestroyStatus(status.id)
    oldestTweet = status
  if oldestTweet is not None and len(statuses) != 1:
    getTweet(oldestTweet.id)

getTweet(None)