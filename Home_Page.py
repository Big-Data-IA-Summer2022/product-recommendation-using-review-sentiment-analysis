import streamlit as st
from PIL import Image
import pandas as pd  
import plotly.express as px  
import streamlit as st 
import streamlit_authenticator as stauth
#import streamlit_authenticator as stauth  
import yaml
from yaml import SafeLoader


st.set_page_config(page_title="# Amazon Sentiment Review Analysis", page_icon=":bar_chart:", layout="wide")

"# Amazon Sentiment Review Analysis"

st.write("")




col1, col2 = st.columns(2)
img = Image.open("image.png")
# reference:https://www.clickworker.com/sentiment-analysis/
with col1:
    st.image(img, use_column_width = 'always')

# --- USER AUTHENTICATION ---
with col2:
    with open('config.yaml') as file:
        config = yaml.load(file, Loader = SafeLoader)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
        )
    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        authenticator.logout('Logout', 'main')
        st.write(f'Welcome *{name}*')
        st.write(" It's good to have you here today")
        st.write(' Please use the Sentiment Analysis in the Analysis page')

    elif authentication_status == False:
        st.error('Username/password is incorrect!')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
        
