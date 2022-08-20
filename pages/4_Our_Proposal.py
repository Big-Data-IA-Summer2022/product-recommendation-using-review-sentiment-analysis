
import streamlit as st
from PIL import Image

("# Proposal")
st.write("")
st.markdown('If you prefer read in codelab please use this link: https://codelabs-preview.appspot.com/?file_id=1RJvR5MxeKuZ-XPl1D1SU9AP7VFfbj3VkLmXqpXA8nXo#0 ')

st.subheader('Overview:')
with st.container():
    st.write("One of the most important problems in e-commerce is that it is easy for users to feel \
            disoriented. When users are dazzled, they can't quickly get the relevant information \
            they want on a product page. Users must read through all ratings and reviews to get \
            results. Looking at just one product may not reveal the severity of the problem, but \
            with multiple products,it can be time-consuming.")
    st.write("Imagine you're looking for a product on a website, and you don't have a specific goal \
            but instead search for the right product to buy. Usually, at this time, you will open \
            countless product pages and check all the information and ratings of the product and \
            user reviews. At this time, you may not have enough time to check all the user reviews \
            to decide which product to buy.")
st.write('         ')
st.subheader('Our Goal:')
with st.container():
    st.write("Our goal is to quickly analyze all the user reviews on a product based on the sentiment\
             in the reviews.The ways a user can have access to those is by:")
    st.write('**For specific products:**')
    st.write('          ◾️         Pasting the link to the product to our API.')
    st.write('          ◾️         Pasting the ASIN number of the product to our API.')
    st.write('**For best-sellers:**')
    st.write("          ◾️         Users have the option to select from a dropdown, categories of best selling \
                        products and get the positive review percentages on products in a descending \
                        order through which the customer can see all the best selling products under \
                        that category and select the product that best suits them. The Selected product\
                        would then redirect the user to the product webpage.")

st.write('         ')
st.subheader('Use Cases:')
with st.container():
        st.write("**Convenient for time-critical users:** Use data visualizations to understand user reviews \
                on top-selling pages or user reviews on product links to decide what to purchase quickly.")
        st.write("**Increase sales on e-commerce sites:** Increase customer pageviews to drive traffic and \
                increase sales")
        st.write("**Any company with user reviews:** Reduce manual labor, use models to determine user review \
                sentiment (positive/negative)")

st.write('         ')
st.subheader('Data:')
st.write("""

This dataset consists of a few million Amazon customer reviews (input text) and star \
ratings (output labels) for learning how to train fastText for sentiment analysis.
 
The data is in the following format:
__label__<X> __label__<Y> ... <Text>

where X and Y are the class names. No quotes, all on one line.

In this case, the classes are __label__1 and __label__2, and there is only one class per row.
 
__label__1 corresponds to 1 and 2 star reviews, and __label__2 corresponds to 4 and 5 star reviews.
(3-star reviews with neutral sentiment were not included in the original)


""")
st.subheader('DataSource Link:')
st.markdown('https://www.kaggle.com/datasets/tarkkaanko/amazon')
st.write('         ')
st.subheader('Process Outline:')

st.write("◾️  Training the CNN model and generating the model(HDF5) and tokenizer(Pickle) on the Amazon review dataset.")

st.write("◾️  Create an API using the model to pass in review text and get positive or negative as an output.")

st.write("◾️ Next would be creating a function which scrapes all the reviews once it's given a product link and stores \
  it locally/ BigQuery, then for each review calls the first API for sentiment analysis and creates a confusion \
  matrix/ Percentage for positive and negative reviews on the specific product.")

st.write("◾️ Scrape all the products in different best-seller categories and get product details and URL's of the products.")

st.write("◾️ Create a function to pass in each product within a category, scrape all the reviews using URL and create a \
 sentiment percentage of the reviews for the products using our API.")

st.write("◾️ Store all the product information in a database to query the data as soon as the user selects the products.")

st.write("◾️ Create an AIRFLOW dag and schedule it daily which creates a pipeline for scraping all the products in different \
 categories, passes URL to the API and scrapes all the reviews for the product and calls the first API for every \
 review and gets a percentage of positive sentiments for every product. Save all the data into the database.")

st.write("◾️ Create a front end such that the front end queries the database or API which can query the database to get the \
  results for the user.")

st.write('         ')
st.subheader('Deployment Details:')
st.write("◾️ **Model:** NLP")
st.write("◾️ **Language:** Python")
st.write("◾️ **Pipeline:** Airflow")
st.write("◾️ **Container:** Docker")
st.write("◾️ **Cloud Tools:** Google Cloud Platform")
st.write('         ')

st.subheader('Design Diagram:')
img = Image.open("design_diagram.png")
st.image(img)
