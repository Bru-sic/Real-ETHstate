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


st.title("Real-ETHstate")
st.markdown("# Welcome to Real-ETHstate")

