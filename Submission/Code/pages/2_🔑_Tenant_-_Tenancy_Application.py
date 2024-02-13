#######
### Main code section of this module
# Allows a Prospective Renter to submit a Tenancy Agreement
# 1. Renter selects a property
# 2. Details of the property are displayed including the rent
# 3. If property is available for rent lets applicant fill in details and confirm
# 3.1.  Calculates the bond needed = 4 x Rent
# 3.2.  Allows Renter to specify duration of contract (6, 12, 18, 24 months). For testing a shorter period such as 2 minutes is needed
# 3.3.  Renter selects their EOA
# 3.4.  If all valid then sign contract button is enabled
# 3.5.  If sign contract button is pushed 
# 3.5.1. Sets the Property's contract as Rented  
# 3.5.2. Sets Renter as a User of the Property and the Expiry Date
# 3.5.3. Notifies successful application, sends event notification
# 3.5.4. TO DO in future implementation: Identity Check, e.g. using ConnectID or other third party provider API
# 3.5.5. TO DO in future implementation: Credit Check, e.g. using EquiFax or other third party provider API
# 3.5.6. If Successful Identity Check and Credit Checks received:
# 3.5.7.     Renter is assigned as a user of the Proptery (set as user on the 4907 token)
# 
#######


import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import time
import datetime
# Import Regular Expression Module (RE)
import re
import numpy as np

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

## Set the page configuration to show a title and icon in the brower's tab
st.set_page_config(page_title="Real-ETHstat - Tenancy Application", page_icon="🔑", layout="wide")

# Retrieve the contract connection details from the Cache
contract = st.session_state.contract

# Provision / Render Page Layout

# Define an upper zone and a lower zone on the screen realestate 
page_header = st.container()
page_body = st.container(border=True)
page_footer = st.container(border=False)

# Present the header content
header_col = page_header.columns([.1,.7,.1,.1]) # Create sections in the header for content

# Header text
header_col[0].image('../Resources/Real-ETHstate_logo.png')
header_col[1].markdown("Discover your Dream Property with Real-ETHstate Inc.")
header_col[3].markdown("User: Jane Smith")

# Footer content
st.markdown("---")
with page_footer:
    footer_cols = st.columns(5)
    footer_cols[0].markdown("(C) Copyright 2024 Real-ETHstate Inc.")
    footer_cols[2].markdown("[Terms and Conditions](http://localhost:8502/terms)")
    footer_cols[4].image('../Resources/socialmedia.png')

page_body.markdown("# Tenancy Application")

# Simulate fetching from a DB
property_id = 0x33d1f7f5e0
propertyTokenId = 1
lot_plan_number = "1863/1000001"
street_address = "25 Wentworth Street, Manly NSW 2095 Australia"
rent = 500000000000000000 # Rent in Wei
min_rental_duration=24 # minimum rental period in weeks.
max_rental_duration=96 # maximum rental period in months.
bedrooms=4
bathrooms=3
floor_space=180


# conversion rates
one_eth_in_wei = 1000000000000000000
eth_to_usd = 2649.84
eth_to_aud = 4063.86

with page_body:
    body_cols = st.columns(2)

    # Use the propert box 
#    body_cols[0].markdown(f"Property: {lot_plan_number}")
    body_cols[0].markdown(f"Property ID: {property_id}")
    body_cols[0].markdown(f"Property Address: {street_address}")
    body_cols[0].markdown(f"Bedrooms: {bedrooms}")
    body_cols[0].markdown(f"Bathrooms: {bathrooms}")
    body_cols[0].markdown(f"Internal Floor Space: {floor_space} m2")

    body_cols[0].markdown(f"Weekly Rent (ETH):{rent/one_eth_in_wei:,}") 
    body_cols[0].markdown(f"Weekly Rent (USD):{rent/one_eth_in_wei*eth_to_usd:,}")
    body_cols[0].markdown(f"Weekly Rent (AUD):{rent/one_eth_in_wei*eth_to_aud:,}")

    body_cols[1].image('../Resources/property_0001.png', caption="Seaside Serenity Villa" )
    body_cols[1].markdown("A stunning 4-bedroom, 3-bathroom villa in a peaceful suburban neighbourhood.")

duration = page_body.slider("Rental duration (weeks)", min_rental_duration, max_rental_duration, min_rental_duration)

end_date = datetime.datetime.now() + datetime.timedelta(weeks=duration)
page_body.text(f"Contract End: {end_date.date()}")

# Capture the Renter's EOA address
renter_eoa_address = page_body.text_input("Select your EOA Account",
                                      max_chars=42,
                                      placeholder= "E.g. 0x1234567890abcdefABCDEF1234567890abcdefAB",
                                      help="""Owner's EOA Account. An EOA Account is prefixed with `0x` followed by 40 hexadecimal case sensitive characters
                                      E.g. `0x1234567890abcdefABCDEF1234567890abcdefAB`""");

# Use a regular expression with the match function to validate that the EOA Account Address conforms to a valid address.
# The address must start with `0x` followed by 40 hexadecimal case sensitive characters
renter_eoa_address_valid = re.match(r"0x[a-fA-F0-9]{40}$", renter_eoa_address) and not re.match(r"0x[0]{40}$", renter_eoa_address)
if renter_eoa_address and not renter_eoa_address_valid:
    page_body.error("EOA Account is invalid", icon="❗")    

rent_button = page_body.button("Rent Property", type="primary", disabled=not renter_eoa_address_valid) # Allows Renting if all inputs are provided
if rent_button:
    tx_hash = contract.functions.setUser( # Set the renter's as user
        int(propertyTokenId),
        renter_eoa_address,
        int(end_date.timestamp())
    ).transact({'from': st.session_state.property_eoa_address, 'gas': 1000000})

    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
st.markdown("---")

