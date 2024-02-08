import streamlit as st
import numpy as np


#######
### Main code section of this module
#######

## Set the page configuration to show a title and icon in the brower's tab
st.set_page_config(page_title="Real-ETHstat - Tenancy Application", page_icon="🔑")

st.markdown("# This is Page 0 content")
st.sidebar.header("Page 0 Header")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

