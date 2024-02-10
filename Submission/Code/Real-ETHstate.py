################################################################################
# Real-ETHstate main module
# 
################################################################################

import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

## Set the page configuration to show a title and icon in the brower's tab
st.set_page_config(page_title="Real-ETHstat - Home", page_icon=":house:", layout="wide")


################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


#@st.cache(allow_output_mutation=True)
@st.cache_resource()
def load_contract():
    # Define and connect a new Web3 provider
    w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

    # Load the contract ABI
    with open(Path('./contracts/compiled/Real-ETHstate.json')) as f:
        contract_abi = json.load(f)

    # Get the deployed contract's address from the value associated with the key "SMART_CONTRACT_ADDRESS" in the .env file
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract




# Load the contract
if "contract" not in st.session_state:
    st.session_state.contract = load_contract()

# Provision / Render Page Layout

# Define an upper zone and a lower zone on the screen realestate 
page_header = st.container()
page_body = st.container(border=True)
page_body_left, page_body_right = page_body.columns([0.6,0.4])
page_footer = st.container(border=False)

# Present the header content
header_col = page_header.columns([.8,.1,.1]) # Create 3 sections in the header. One of 80% width, the others of 10% each.

# Header text
header_col[0].markdown("Discover your Dream Property with Real-ETHstate Inc. [Learn More](http://localhost:8502/Learn_More)")

# Sign In push button
if header_col[1].button("Sign In", type="secondary"):
            st.info('Coming soon', icon="ℹ️")

# Join push button
if header_col[2].button("Join", type="primary"):
            st.info('Coming soon', icon="ℹ️")

# Background image on right side of page
page_body_right.image('../Resources/Img_001.png')


#st.page_link("pages/learn_more.py", label="Learn More", icon="")
page_body_left.markdown("# Discover your Dream Property with Real‑ETHstate Inc.")
page_body_left.markdown("Your journey to finding the perfect property begins here. Explore our listing to find the home that matches your dreams")

with page_body_left:
    button_row = page_body_left.columns([.15,.2,.65])

    with button_row[0]:
        if st.button("Learn More", type="secondary"):
            st.info('Coming soon', icon="ℹ️")

    with button_row[1]:
        if st.button("Browse Properties", type="primary"):
            st.info('Coming soon', icon="ℹ️")

# Create 3 Info tiles with statistics
tile = page_body_left.columns(3)

with tile[0]:
    with st.container(border=True):
        st.markdown("## 200+")
        st.markdown("Happy Customers")

with tile[1]:
    with st.container(border=True):
        st.markdown("## 10k+")
        st.markdown("Client Properties")

with tile[2]:
    with st.container(border=True):
        st.markdown("## 16+")
        st.markdown("Years of Experience")

page_body_rightleft = page_body.container(border=True)

page_footer.markdown("---")
page_footer.markdown("(C) Copyright 2024 Real-ETHstate Inc \t[Terms and Conditions](http://./toc.html)")
