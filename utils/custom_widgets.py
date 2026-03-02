import streamlit as st
import pandas as pd
import seaborn as sns
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


### KPI visualizations ###
def number_card(toptxt, subtext):
    st.markdown("""
    <style>
    .big-font {
        font-size:60px !important;
        line-height:45%;
        text-align:center;
        color:#CDE8E5;
    }
    .under-font {
        font-size:15px;
        text-align:center;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="big-font">' + str(toptxt) + '</p>', unsafe_allow_html=True)
    st.markdown('<p class="under-font">' + str(subtext) + '</p>', unsafe_allow_html=True)


def number_card_tworow(toptxt, infotext, subtext):
    st.markdown("""
    <style>
    .big-font-two-row {
        font-size:60px !important;
        line-height:45%;
        text-align:center;
        color:#CDE8E5;
    }
    .mid-font {
        font-size:20px;
        text-align:center;
        line-height:100%;
        color:#E4E6EB;
    }
    .under-font {
        font-size:15px;
        text-align:center;
        line-height:100%;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="big-font-two-row">' + str(toptxt) + '</p>', unsafe_allow_html=True)
    st.markdown('<p class="mid-font">' + str(infotext) + '</p>', unsafe_allow_html=True)
    st.markdown('<p class="under-font">' + str(subtext) + '</p>', unsafe_allow_html=True)