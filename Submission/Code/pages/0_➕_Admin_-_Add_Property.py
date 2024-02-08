import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

#######
### Main code section of this module
#######

## Set the page configuration to show a title and icon in the brower's tab
st.set_page_config(page_title="Real-ETHstat - Add a Property", page_icon="➕")

st.markdown("# Add a Property")
st.markdown("Use this function once a property owner has provided all the required details of themselves and their property to Real-ETHstate. You will need:")
st.markdown("1. Details of the property")
st.markdown("2. An Admin Account")
st.markdown("3. Account Number of the Owner")

accounts = w3.eth.accounts
address = st.selectbox("Select Admin Account", options=accounts)
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

if st.button("Register Artwork"):
    tx_hash = contract.functions.registerArtwork(
        address,
        artwork_name,
        artist_name,
        int(initial_appraisal_value),
        artwork_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
st.markdown("---")


################################################################################
# Appraise Art
################################################################################
st.markdown("## Appraise Artwork")
tokens = contract.functions.totalSupply().call()
token_id = st.selectbox("Choose an Art Token ID", list(range(tokens)))
new_appraisal_value = st.text_input("Enter the new appraisal amount")
report_uri = st.text_area("Enter notes about the appraisal")
if st.button("Appraise Artwork"):

    # Use the token_id and the report_uri to record the appraisal
    tx_hash = contract.functions.newAppraisal(
        token_id,
        int(new_appraisal_value),
        report_uri
    ).transact({"from": w3.eth.accounts[0]})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt)
st.markdown("---")

################################################################################
# Get Appraisals
################################################################################
st.markdown("## Get the appraisal report history")
art_token_id = st.number_input("Artwork ID", value=0, step=1)
if st.button("Get Appraisal Reports"):
    appraisal_filter = contract.events.Appraisal.createFilter(
        fromBlock=0,
        argument_filters={"tokenId": art_token_id}
    )
    appraisals = appraisal_filter.get_all_entries()
    if appraisals:
        for appraisal in appraisals:
            report_dictionary = dict(appraisal)
            st.markdown("### Appraisal Report Event Log")
            st.write(report_dictionary)
            st.markdown("### Appraisal Report Details")
            st.write(report_dictionary["args"])
    else:
        st.write("This artwork has no new appraisals")
