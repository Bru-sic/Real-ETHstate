import streamlit as st
import numpy as np


#######
### Main code section of this module
#######

## Set the page configuration to show a title and icon in the brower's tab
st.set_page_config(page_title="Real-ETHstat - Open Property to Rent", page_icon="🪙", layout="wide")

header = st.container()
body = st.container()
footer = st.container()

header.markdown("# Real-ETHstat - Open Property to Rent")
body.write(
    """This is where you can change your property's rental status
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)



################################################################################
# Appraise Art
################################################################################
# st.markdown("## Appraise Artwork")
# tokens = contract.functions.totalSupply().call()
# token_id = st.selectbox("Choose an Art Token ID", list(range(tokens)))
# new_appraisal_value = st.text_input("Enter the new appraisal amount")
# report_uri = st.text_area("Enter notes about the appraisal")
# if st.button("Appraise Artwork"):

#     # Use the token_id and the report_uri to record the appraisal
#     tx_hash = contract.functions.newAppraisal(
#         token_id,
#         int(new_appraisal_value),
#         report_uri
#     ).transact({"from": w3.eth.accounts[0]})
#     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     st.write(receipt)
st.markdown("---")

################################################################################
# Get Appraisals
################################################################################
# st.markdown("## Get the appraisal report history")
# art_token_id = st.number_input("Artwork ID", value=0, step=1)
# if st.button("Get Appraisal Reports"):
#     appraisal_filter = contract.events.Appraisal.createFilter(
#         fromBlock=0,
#         argument_filters={"tokenId": art_token_id}
#     )
#     appraisals = appraisal_filter.get_all_entries()
#     if appraisals:
#         for appraisal in appraisals:
#             report_dictionary = dict(appraisal)
#             st.markdown("### Appraisal Report Event Log")
#             st.write(report_dictionary)
#             st.markdown("### Appraisal Report Details")
#             st.write(report_dictionary["args"])
#     else:
#         st.write("This artwork has no new appraisals")



footer.markdown("---")
footer.markdown("(C) Copyright 2024 Real-ETHstate Inc \t[Terms and Conditions](http://./toc.html)")
