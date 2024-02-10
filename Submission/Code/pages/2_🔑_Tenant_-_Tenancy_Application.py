import streamlit as st
import numpy as np


#######
### Main code section of this module
#######

## Set the page configuration to show a title and icon in the brower's tab
st.set_page_config(page_title="Real-ETHstat - Tenancy Application", page_icon="🔑")

header = st.container()
body = st.container()
footer = st.container()

header.markdown("# Real-ETHstat - Open Property to Rent")
body.write("This is where you can allow your property to be rented")


footer.markdown("---")
footer.markdown("(C) Copyright 2024 Real-ETHstate Inc \t[Terms and Conditions](http://./toc.html)")
