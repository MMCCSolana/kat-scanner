
import streamlit as st
import MMCC
import check
import royalty_check
import MMCC_act

st.set_page_config(
    page_title="Meerkat Tracker",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon= 'favicon.png'
)

#Streamlit commands

st.write("""
# MMCC and NMBC Sales and Royalties Tracker

NOTE: This reads data directly from api's which tend to be slow/unstable at times and will pull new data every ~2 minutes!

""")

PAGES = {
"Rewards Checker": check,
"ClubDAO Treasury": royalty_check,
"MMCC Listings": MMCC,
"MMCC Activity": MMCC_act
#"Naked Meerkat Beach Club": NMBC,
#"Rewards Checker - DEV": checkdev
}

selection = st.radio("Page to view:", list(PAGES.keys()))
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
page = PAGES[selection]

page.app()
