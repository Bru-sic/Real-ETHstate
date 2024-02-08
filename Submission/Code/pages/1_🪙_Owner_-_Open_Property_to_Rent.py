import streamlit as st
import numpy as np


#######
### Main code section of this module
#######

## Set the page configuration to show a title and icon in the brower's tab
st.set_page_config(page_title="Real-ETHstat - Open Property to Rent", page_icon="🪙")

header = st.container()
body = st.container()
footer = st.container()

header.markdown("# This is Page 3333 content")
st.sidebar.header("Page 1 Header")
body.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

footer.markdown("---")
footer.markdown("(C) Copyright 2024 Real-ETHstate Inc      [Terms and Conditions](http://./toc.html)")
