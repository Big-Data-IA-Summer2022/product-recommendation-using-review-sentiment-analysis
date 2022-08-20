import streamlit as st

"# User Guide"
st.write("")

choice=st.sidebar.radio("Pick one to start know our process:",["Demo Video","Documentation"])

if choice== "Demo Video":
    st.subheader("A liitle Demo on How to use our API")
    st.write("--------")
    st.write("**comming soon**")
    #st.video("",format="video/mp4")

elif choice=="Documentation":
    st.subheader("Documentation")
    st.write("-------")
    st.write("**comming soon**")
