from turtle import color
from unicodedata import decimal
import numpy as np
import pandas as pd
import streamlit as st
import pandas_gbq
from google.oauth2 import service_account
from IPython.display import HTML
import requests
from PIL import Image
import json
import random
import string

"# 💖 Hope it makes your life easier 🥰"

st.write("")

credentials = service_account.Credentials.from_service_account_file('key.json')




choice=st.sidebar.radio("Pick one to start your journey with us:",["Find your interested product by Best Seller Category","Find by a Product Link","Find by a Product Name","Find by a Product ASIN"])

if choice == "Find your interested product by Best Seller Category":
    st.subheader('Please select a Amazon Best Seller Department from the list')
    topic = pandas_gbq.read_gbq(

    'SELECT  replace(replace(topic,",",""),"&","and") as topic FROM `defect-detection-356414.for_logs.best-seller` group by 1 order by 1 asc',project_id='defect-detection-356414', credentials=credentials)
    category = st.selectbox("Department",(topic),index=0)
    btn = st.button(label = 'Search',key='1', disabled=False)
    with st.spinner('Generating ...'):
        if btn:
            tab1,tab2 = st.tabs(["📈 Insights","🗃 Details"])
            df = f'SELECT * FROM `defect-detection-356414.for_logs.best-seller-with-ratings-{category}` order by review_rating desc '
            data= pandas_gbq.read_gbq(df,project_id='defect-detection-356414', credentials=credentials)
            with tab1:
                average= data['Rating_out_of_5'].mean().round(decimals = 2)
                min_price= data['Minimum_price'].min()
                max_price=data['Maximum_price'].max()
                col1, col2, col3 = st.columns(3)
                col1.metric("🌟 Average Rating in the Category", average)
                col2.metric("💵 Minimum Price in the Category", min_price)
                col3.metric("💸 Maximum Price in the Category", max_price)
                tab1.subheader(f"Customer Rating Distribution in **{category}** Department")
                st.write('    ')
                chart_data = data['Rating_out_of_5'].value_counts()
                tab1.bar_chart(chart_data)
            with tab2:
                tab2.subheader("Customer Review Details")
                st.write('    ')
                data['Item_Url'] = 'http://' + data['Item_Url'].astype(str)
                tab2.write(HTML(data.to_html(render_links=True, escape=False)))
elif choice == "Find by a Product Link":
    st.subheader('Please paste in a accurate Amazon product link and select a page number:')
    link = st.text_input('product link', '')
    page_link = st.number_input('page number: ', max_value = 9, min_value = 1, step = 1)
    col1, col2,col3 = st.columns(3)
    with col1:
        btn_api = st.button(label = 'Step 1: Call API',key='3', disabled=False)
        if btn_api:
            with st.spinner('Calling the API ...'):
                payload= {'text': link,'page':page_link}
                url=f"https://damg7245-finalproject-sentiment-analysis-fol52rb4xq-ue.a.run.app/scrape_product_using_product_url?url={payload['text']}&pages={payload['page']}"
                response = requests.request("POST", url, params=payload)
    with col2:
        btn_dag = st.button(label = 'Step 2: Dag Trigger',key='4', disabled=False)
        if btn_dag:
            with st.spinner('Triggering the Dag ...'):
                letters = string.ascii_lowercase
                url = "http://35.196.111.228:8080/api/v1/dags/scraperforurl/dagRuns"
                payload = json.dumps({"dag_run_id": ''.join(random.choice(letters) for i in range(10))})
                headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Authorization': 'Basic YWlyZmxvdzphaXJmbG93',
                'Content-Type': 'application/json',
                'Cookie': 'session=fa4019dc-3e32-4785-babe-f1881bcdcbd2.0MZlc2KPl0AqtG4de855trFvA9w'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                if response.status_code == 200:
                    st.write("Dag has been trigged")
                else:
                    st.write("Unable to trigger the dag")
    with col3:
        btn_link = st.button(label = 'Step 3: Display Analysis',key='5', disabled=False)
    if btn_link:
                tab1,tab2 = st.tabs(["📈 Insights","🗃 Details"])
                df = 'SELECT * FROM `defect-detection-356414.for_logs.product-url-ratings`'
                data= pandas_gbq.read_gbq(df,project_id='defect-detection-356414', credentials=credentials)
                with tab1:
                    tab1.subheader('Product Insights')
                    st.write('    ')
                    # product_name=data['product'][0]
                    # st.write(f'**Product Description:**  {product_name}')
                    rating= data['rating'].mean()
                    variant= data['variant'][0]
                    review=data['review_rating'].max().round(decimals=2)
                    product_link=data['url'][0]
                    col_1, col_2 = st.columns(2)
                    with col_1:
                        if data['images'][0] is None:
                            st.write('**No Image**')
                        else:
                            ch = "\n"
                            img = data['images'][0].split(ch, 1)[0]
                            st.image(img,use_column_width='always')
                    with col_2:
                        product_name=data['product'][0]
                        st.write(f'**Product Description:**  {product_name}')
                        st.write('    ')
                        st.write('   ')
                        st.write('     ')
                        st.markdown(f'**Product Link:**  {product_link}')
                    st.write('    ')
                    st.write('    ')
                    col1, col2, col3 = st.columns(3)
                    col1.metric("⭐️ Product Rating", rating)
                    col3.metric("💁‍♀️ Product Variant", variant)
                    col2.metric("📃 Review Rating", review)
                with tab2:
                    tab2.subheader("Product Details")
                    st.write('    ')
                    tab2.write(HTML(data.to_html(render_links=True)))
elif choice == "Find by a Product Name":
    st.subheader('Please type in a product name and select a page number:')
    title = st.text_input('product name', '')
    page = st.number_input('page number: ', max_value = 9, min_value = 1, step = 1)
    col1, col2,col3 = st.columns(3)
    with col1:
        btn_api_1 = st.button(label = 'Step 1: Call API',key='6', disabled=False)
        if btn_api_1:
            with st.spinner('Calling the API ...'):
                payload= {'text': title,'page':page}
                url=f"https://damg7245-finalproject-sentiment-analysis-fol52rb4xq-ue.a.run.app/scrape_product_using_product_search?search_key={payload['text']}&pages={payload['page']}"
                response = requests.request("POST", url, params=payload)
    with col2:
        btn_dag_1 = st.button(label = 'Step 2: Dag Trigger',key='7', disabled=False)
        if btn_dag_1:
            with st.spinner('Triggering the Dag ...'):
                letters = string.ascii_lowercase
                url = "http://35.196.111.228:8080/api/v1/dags/product_search/dagRuns"
                payload = json.dumps({"dag_run_id": ''.join(random.choice(letters) for i in range(10))})
                headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Authorization': 'Basic YWlyZmxvdzphaXJmbG93',
                'Content-Type': 'application/json',
                'Cookie': 'session=fa4019dc-3e32-4785-babe-f1881bcdcbd2.0MZlc2KPl0AqtG4de855trFvA9w'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                if response.status_code == 200:
                    st.write("Dag has been trigged")
                else:
                    st.write("Unable to trigger the dag")
    with col3:
        btn_name = st.button(label = 'Step 3: Display Analysis',key='8', disabled=False)
        st.spinner('Generating ...')
    if btn_name:
                tab1,tab2 = st.tabs(["📈 Insights","🗃 Details"])
                df = 'SELECT product,left(rating,3) as rating,	price,	product_url,	round(review_rating,2) as review_rating FROM `defect-detection-356414.for_logs.product-search-ratings` order by 5 desc'
                data= pandas_gbq.read_gbq(df,project_id='defect-detection-356414', credentials=credentials)
                with tab1:
                    if data.empty:
                        'DataFrame is not ready'
                    else:
                        tab1.subheader('Product Insights')
                        rating= data['rating'].astype(float)
                        avg= rating.mean().round(decimals = 2)
                        avg_price= data['price'].mean().round(decimals = 2)
                        review=data['review_rating'].max()
                        col1, col2, col3 = st.columns(3)
                        col1.metric("🌟 Average Product Rating", avg)
                        col2.metric(f"💸 Average Price in {title}", avg_price)
                        col3.metric("📃 Maximum Review Rating", review)
                        tab1.subheader(f"Review Rating Distribution in **{title}** ")
                        st.write('    ')
                        chart_data = data['review_rating'].value_counts()
                        tab1.bar_chart(chart_data)
                with tab2:
                    tab2.subheader("Product Details")
                    st.write('    ')
                    tab2.write(HTML(data.to_html(render_links=True, escape=False)))
        
elif choice == "Find by a Product ASIN":
    st.subheader('Please type in a product ASIN and select a page number:')
    asin = st.text_input('product ASIN', '')
    page_asin = st.number_input('page number: ', max_value = 9, min_value = 1, step = 1)
    col1, col2,col3 = st.columns(3)
    with col1:
        btn_api_2 = st.button(label = 'Step 1: Call API',key='9', disabled=False)
        if btn_api_2:
            with st.spinner('Calling the API ...'):
                payload= {'text': asin,'page':page_asin}
                url=f"https://damg7245-finalproject-sentiment-analysis-fol52rb4xq-ue.a.run.app/scrape_product_using_product_asin?asin={payload['text']}&pages={payload['page']}"
                response = requests.request("POST", url, params=payload)
    with col2:
        btn_dag_2 = st.button(label = 'Step 2: Dag Trigger',key='10', disabled=False)
        if btn_dag_2:
            with st.spinner('Triggering the Dag ...'):
                letters = string.ascii_lowercase
                url = "http://35.196.111.228:8080/api/v1/dags/review_rating_using_asin/dagRuns"
                payload = json.dumps({"dag_run_id": ''.join(random.choice(letters) for i in range(10))})
                headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Authorization': 'Basic YWlyZmxvdzphaXJmbG93',
                'Content-Type': 'application/json',
                'Cookie': 'session=fa4019dc-3e32-4785-babe-f1881bcdcbd2.0MZlc2KPl0AqtG4de855trFvA9w'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                if response.status_code == 200:
                    st.write("Dag has been trigged")
                else:
                    st.write("Unable to trigger the dag")
    with col3:
        btn_asin = st.button(label = 'Step 3: Display Analysis',key='11', disabled=False)
    if btn_asin:
                tab1,tab2 = st.tabs(["📈 Insights","🗃 Details"])
                df = 'SELECT * FROM `defect-detection-356414.for_logs.product-asin-ratings`'
                data= pandas_gbq.read_gbq(df,project_id='defect-detection-356414', credentials=credentials)
                with tab1:
                    tab1.subheader('Product Insights')
                    st.write('    ')
                    # product_name=data['product'][0]
                    # st.write(f'**Product Description:**  {product_name}')
                    rating= data['rating'].mean()
                    variant= data['variant'][0]
                    review=data['review_rating'].max().round(decimals=2)
                    product_link=data['url'][0]
                    col_1, col_2 = st.columns(2)
                    with col_1:
                        if data['images'][0] is None:
                            st.write('**No Image**')
                        else:
                            ch = "\n"
                            img = data['images'][0].split(ch, 1)[0]
                            st.image(img,use_column_width='always')
                    with col_2:
                        product_name=data['product'][0]
                        st.write(f'**Product Description:**  {product_name}')
                        st.write('    ')
                        st.write('   ')
                        st.write('     ')
                        st.markdown(f'**Product Link:**  {product_link}')
                    st.write('    ')
                    st.write('    ')
                    col1, col2, col3 = st.columns(3)
                    col1.metric("⭐️ Product Rating", rating)
                    col2.metric("📃 Review Rating", review)
                    col3.metric("💁 Product Variant", variant)
                    st.write('    ')
                    st.write('    ')
                    
                with tab2:
                    tab2.subheader("Product Details")
                    st.write('    ')
                    tab2.write(HTML(data.to_html(render_links=True, escape=False)))


