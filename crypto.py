import requests
import pandas as pd
import os
import json
from dotenv import load_dotenv
from csv import writer
import requests
import streamlit as st
load_dotenv()



id = 'bitcoin'

# coingecko API is easier to follow along with than pycoingecko following that! 

r = requests.get(f'https://api.coingecko.com/api/v3/coins/{id}')
st.write(r.json())