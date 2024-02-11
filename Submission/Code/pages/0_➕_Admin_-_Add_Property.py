import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
# Import Regular Expression Module (RE)
import re

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

## Set the page configuration to show a title and icon in the brower's tab
st.set_page_config(page_title="Real-ETHstat - Add a Property", page_icon="➕", layout="wide")

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


# Footer content
page_footer.markdown("---")
page_footer.markdown("(C) Copyright 2024 Real-ETHstate Inc \t[Terms and Conditions](http://./toc.html)")


page_body.markdown("# Add a Property")
page_body.markdown("Use this function once a property owner has provided all the required details of themselves and their property to Real-ETHstate. You will need:")
page_body.markdown("1. Details of the property")
page_body.markdown("2. Property Owner's Account Number")

accounts = w3.eth.accounts
property_eoa_address = page_body.selectbox("Select your EOA Account as Owner of the Property", options=accounts)

# # Capture the Property's EOA address
# property_eoa_address = page_body.text_input("Owner's EOA Account",
#                                      max_chars=42,
#                                      placeholder= "E.g. 0x1234567890abcdefABCDEF1234567890abcdefAB",
#                                      help="""Owner's EOA Account. An EOA Account is prefixed with `0x` followed by 40 hexadecimal case sensitive characters
#                                      E.g. `0x1234567890abcdefABCDEF1234567890abcdefAB`""");

# Use a regular expression with the match function to validate that the EOA Account Address conforms to a valid address.
# The address must start with `0x` followed by 40 hexadecimal case sensitive characters
property_eoa_address_valid = re.match(r"0x[a-fA-F0-9]{40}$", property_eoa_address) and not re.match(r"0x[0]{40}$", property_eoa_address)
if not property_eoa_address_valid:
    page_body.error("Owner's EOA Account is invalid", icon="❗")    

# page_body.markdown("---")

################################################################################
# Register a new property
################################################################################
page_body.markdown("## Register a Property")

# /// @dev Address Line 1. E.g.: `Block C Unit 1, 234 Bridge Road Annandale NSW 2008 Australia`
street_address = page_body.text_input("Property Location", placeholder= "Unit/Street Number and Name, Suburb State Postcode Country", help="Unit/Street Number and Name, Suburb State Postcode Country E.g.: `Block C Unit 1, 234 Bridge Road Annandale NSW 2008 Australia`");
# /// @dev Land registry Lot / Plan number reference. E.g.: `1863/1000001`, or `35/G/5720` or `1/SP`
#string lot_plan_number;
#/// @dev Asking Rent - the weekly rent amount being requested
#uint256 askingRent; Set by the property owner

lot_plan_number = page_body.text_input("Property Title Reference", placeholder= "Lot/Plan Number", help="Land registry Lot / Plan number reference. E.g.: `1863/1000001`, or `35/G/5720` or `1/SP`");
property_uri = page_body.text_input("Property URI")

# Set the asking rent to 0 when minting as the owner will set it for themselves when activating the property for rent
askingRent = 0

inputs_complete = (property_eoa_address_valid and street_address and lot_plan_number and property_uri)
register_button = page_body.button("Register Property", type="primary", disabled= not inputs_complete)

if register_button:
    tx_hash = contract.functions.safeMint(
        property_eoa_address,
        street_address,
        lot_plan_number,
        property_uri
    ).transact({'from': property_eoa_address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
st.markdown("---")

