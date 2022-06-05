import requests
import streamlit as st
import pandas as pd
import os
import json
import defi.defi_tools as dft
from dotenv import load_dotenv
from csv import writer
from pycoingecko import CoinGeckoAPI
import tweepy
import matplotlib.pyplot as plt

load_dotenv()

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
defi_twitter = os.getenv("TWITTER_USERS")
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# The Twitter API might be better to follow along with, feel there is more control there!
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
# user = defi_twitter
limit=500
keywords = "#ETH"
cg = CoinGeckoAPI()
container = st.container()


st.title("The Real Crypto Twitter")
st.sidebar.title("Options")
option = st.sidebar.selectbox("What are you looking for?", ("Search Defi", "Tweets", "News", "Top Defi Dapps", "DeFi Protocols"))

st.header(option)




if option == "Search Defi":
    user = st.sidebar.text_input("Enter a Twitter username", value="bantg")
    st.subheader("Defi Traders")
    # tweets = api.user_timeline(screen_name=user, count=limit, tweet_mode='extended')
    tweeter = tweepy.Cursor(api.user_timeline, screen_name=user, count=200, tweet_mode='extended').items(limit)
    for tweet in tweeter:
        if '$' in tweet.full_text:
            words = tweet.full_text.split(" ")
            for word in words:
                if word.startswith("$") and word[1:].isalpha():
                    symbol = word[1:]
                    st.image(tweet.user.profile_image_url)
                    st.subheader(tweet.user.screen_name)
                    st.markdown(tweet.created_at)
                    st.write(f"crypto ticker {symbol}")
                    if not tweet.truncated:
                        st.markdown(tweet.full_text)
                    else:
                        st.markdown(tweet.extended['full_text'])

    # hashtags = st.sidebar.text_input("Enter a hashtag # ")
    # tweets = tweepy.Cursor(api.search_tweets, q=hashtags, count=200, tweet_mode='extended').items(limit)
    
    
    


if option == "Tweets":

    tweets = st.sidebar.text_input("What tokens are you looking for?", value="ETH")
    st.subheader("Crypto Tweets")
    # tweets = api.user_timeline(screen_name=user, count=limit, tweet_mode='extended')
    tweets = tweepy.Cursor(api.search_tweets, q=keywords, count=5, tweet_mode='extended', lang='en')
    
    for tweet in tweets.items():
            if '#' in tweet.full_text:
                words = tweet.full_text.split(" ")
                for word in words:
                    if word.startswith("#") and word[1:].isalpha():
                        symbol = word[1:]
                        st.image(tweet.user.profile_image_url)
                        st.subheader(tweet.user.screen_name)
                        st.write(f"crypto ticker {symbol}")
                        st.markdown(tweet.full_text)
                        st.markdown(tweet.created_at)
            # st.image(tweet.user.profile_image_url)
            # st.subheader(tweet.user.screen_name)
            # # st.write(f"crypto ticker {keyword}")
            # st.markdown(tweet.full_text)
            # st.markdown(tweet.created_at)
    # st.sidebar.text_input("Enter a hashtag # ")
    # st.markdown(tweets.full_text)


if option == "Top Defi Dapps":
    df = dft.getProtocols()
    fig, ax = plt.subplots(figsize=(12,6))
    n = 50 # quantity to show
    pools = st.sidebar.text_input(f"Select the number of pools {n}")
    top = df.sort_values('tvl', ascending=False).head(n)
    chains = top.groupby('chain').size().index.values.tolist()
    for chain in chains:
        filtro = top.loc[top.chain==chain]
        ax.bar(filtro.index, filtro.tvl, label=chain)
    
    ax.set_title(f'Top {n} dApp TVL, groupBy dApp main Chain', fontsize=14)
    ax.grid(alpha=0.5)
    plt.legend()
    plt.xticks(rotation=90)
    st.pyplot(fig)

# if option == "DeFi Protocols":
    
#     defi_pair = st.sidebar.text_input("Select a pair", value='huobi-token','tether')
#     defi_apr = st.sidebar.text_input("Select a APR", value=10)
#     pair = ['crv','DAI']

#     st.subheader("DeFi Protocols")
#     apr = 10

#     st.dataframe(dft.farmSimulate(pair, apr, start='2022-05-05'))