import streamlit as st


def load_css():
    st.markdown("""
    <style>

    /* Hide Streamlit branding */
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}

    .block-container{
        padding-top:1.5rem;
        padding-bottom:1rem;
        max-width:95%;
    }

    html,body,[class*="css"]{
        font-family:Inter,Segoe UI,sans-serif;
    }

    h1{
        font-size:42px;
        font-weight:700;
        letter-spacing:-1px;
        color:white;
    }

    h2{
        color:white;
        font-weight:600;
    }

    h3{
        color:white;
        font-weight:500;
    }

    p{
        color:#B8C1CC;
    }

    /* KPI Card */

    .metric-card{
        background:#171C26;
        border:1px solid #242D3A;
        border-radius:14px;
        padding:22px;
        transition:0.25s;
        height:130px;
    }

    .metric-card:hover{
        border:1px solid #3478F6;
        transform:translateY(-2px);
    }

    .metric-title{
        color:#9CA3AF;
        font-size:15px;
    }

    .metric-value{
        color:white;
        font-size:34px;
        font-weight:700;
        margin-top:8px;
    }

    /* Panels */

    .panel{
        background:#171C26;
        border-radius:14px;
        border:1px solid #242D3A;
        padding:22px;
        margin-top:18px;
    }

    /* Sidebar */

    section[data-testid="stSidebar"]{
        background:#12161F;
    }

    section[data-testid="stSidebar"] *{
        color:white;
    }

    /* Tables */

    div[data-testid="stDataFrame"]{
        border-radius:12px;
        overflow:hidden;
    }

    /* Buttons */

    .stButton>button{

        width:100%;

        background:#3478F6;

        color:white;

        border:none;

        border-radius:8px;

        padding:10px;

        font-weight:600;

    }

    .stButton>button:hover{

        background:#245BD6;

    }

    </style>
    """, unsafe_allow_html=True)