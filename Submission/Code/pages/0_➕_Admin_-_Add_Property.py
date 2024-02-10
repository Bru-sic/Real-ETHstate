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

contract = st.session_state.contract

#######
### Main code section of this module
#######

## Set the page configuration to show a title and icon in the brower's tab
st.set_page_config(page_title="Real-ETHstat - Add a Property", page_icon="➕")

st.markdown("# Add a Property")
st.markdown("Use this function once a property owner has provided all the required details of themselves and their property to Real-ETHstate. You will need:")
st.markdown("1. Details of the property")
st.markdown("2. Property Owner's Account Number")

#accounts = w3.eth.accounts
#property_eoa_address = st.selectbox("Select Admin Account", options=accounts)

# Capture the Property's EOA address
property_eoa_address = st.text_input("Owner's EOA Account",
                                     max_chars=42,
                                     placeholder= "E.g. 0x1234567890abcdefABCDEF1234567890abcdefAB",
                                     help="""Owner's EOA Account. An EOA Account is prefixed with `0x` followed by 40 hexadecimal case sensitive characters
                                     E.g. `0x1234567890abcdefABCDEF1234567890abcdefAB`""");

# Use a regular expression with the match function to validate that the EOA Account Address conforms to a valid address.
# The address must start with `0x` followed by 40 hexadecimal case sensitive characters
property_eoa_address_valid = re.match(r"0x[a-fA-F0-9]{40}$", property_eoa_address) and not re.match(r"0x[0]{40}$", property_eoa_address)
if not property_eoa_address_valid:
    st.error("Owner's EOA Account is invalid", icon="❗")    

st.markdown("---")

################################################################################
# Register New Artwork
################################################################################
st.markdown("## Register a Property")

# /// @dev Address Line 1. E.g.: `Block C Unit 1, 234 Bridge Road Annandale NSW 2008 Australia`
street_address = st.text_input("Property Location,", placeholder= "Unit/Street Number and Name, Suburb State Postcode Country", help="Unit/Street Number and Name, Suburb State Postcode Country E.g.: `Block C Unit 1, 234 Bridge Road Annandale NSW 2008 Australia`");
# /// @dev Land registry Lot / Plan number reference. E.g.: `1863/1000001`, or `35/G/5720` or `1/SP`
#string lot_plan_number;
#/// @dev Asking Rent - the weekly rent amount being requested
#uint256 askingRent; Set by the property owner

lot_plan_number = st.text_input("Property Title Reference", placeholder= "Lot/Plan Number", help="Land registry Lot / Plan number reference. E.g.: `1863/1000001`, or `35/G/5720` or `1/SP`");
property_uri = st.text_input("Property URI")

# Set the asking rent to 0 when minting as the owner will set it for themselves when activating the property for rent
askingRent = 0

inputs_complete = (property_eoa_address_valid and street_address and lot_plan_number and property_uri)
register_button = st.button("Register Property",
                            disabled= not inputs_complete)

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

