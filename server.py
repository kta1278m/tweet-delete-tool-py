import os
import json
from urllib.parse import parse_qsl

from flask import Flask, jsonify, request
from requests_oauthlib import OAuth1Session

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)


consumer_key = os.environ.get("API_KEY")
consumer_secret = os.environ.get("API_SECRET")"


base_url = 'https://api.twitter.com/'

request_token_url = base_url + 'oauth/request_token'
authenticate_url = base_url + 'oauth/authenticate'
access_token_url = base_url + 'oauth/access_token'

base_json_url = 'https://api.twitter.com/1.1/%s.json'
user_timeline_url = base_json_url % ('statuses/user_timeline')


# 認証画面（「このアプリと連携しますか？」の画面）のURLを返すAPI
@app.route('/twitter/request_token', methods=['GET'])
def get_twitter_request_token():

    # Twitter Application Management で設定したコールバックURLsのどれか
    oauth_callback = request.args.get('oauth_callback')

    twitter = OAuth1Session(consumer_key, consumer_secret)

    response = twitter.post(
        request_token_url,
        params={'oauth_callback': oauth_callback}
    )

    request_token = dict(parse_qsl(response.content.decode("utf-8")))

    # リクエストトークンから認証画面のURLを生成
    authenticate_endpoint = '%s?oauth_token=%s' \
        % (authenticate_url, request_token['oauth_token'])

    request_token.update({'authenticate_endpoint': authenticate_endpoint})

    return jsonify(request_token)


# アクセストークン（連携したユーザーとしてTwitterのAPIを叩くためのトークン）を返すAPI
@app.route('/twitter/access_token', methods=['GET'])
def get_twitter_access_token():

    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')

    twitter = OAuth1Session(
        consumer_key,
        consumer_secret,
        oauth_token,
        oauth_verifier,
    )

    response = twitter.post(
        access_token_url,
        params={'oauth_verifier': oauth_verifier}
    )

    access_token = dict(parse_qsl(response.content.decode("utf-8")))

    return jsonify(access_token)



@app.route('/twitter/user_timeline', methods=['GET'])
def get_twitter_user_timeline():

    access_token = request.args.get('access_token')

    params = {
        'user_id': request.args.get('user_id'),
        'exclude_replies': True,
        'include_rts': json.get('include_rts', False),
        'count': 20,
        'trim_user': False,
        'tweet_mode': 'extended',    # full_textを取得するために必要
    }

    twitter = OAuth1Session(
        consumer_key,
        consumer_secret,
        access_token['oauth_token'],
        access_token['oauth_token_secret'],
    )

    response = twitter.get(user_timeline_url, params=params)
    results = json.loads(response.text)

    return jsonify(results)

if __name__ == "__main__":
    port = os.environ.get('PORT', 3333)
    app.run(
        host='0.0.0.0',
        port=port,
    )