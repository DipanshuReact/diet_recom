import streamlit as st
import base64

logo = """
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="white"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
    class="h-6 w-6"
    >
    <path d="M7 21h10"></path>
    <path d="M12 21a9 9 0 0 0 9-9H3a9 9 0 0 0 9 9Z"></path>
    <path
        d="M11.38 12a2.4 2.4 0 0 1-.4-4.77 2.4 2.4 0 0 1 3.2-2.77 2.4 2.4 0 0 1 3.47-.63 2.4 2.4 0 0 1 3.37 3.37 2.4 2.4 0 0 1-1.1 3.7 2.51 2.51 0 0 1 .03 1.1"
    ></path>
    <path d="m13 12 4-4"></path>
    <path
        d="M10.9 7.25A3.99 3.99 0 0 0 4 10c0 .73.2 1.41.54 2"
    ></path>
</svg>
"""

logo_64 = base64.b64encode(logo.encode()).decode()

st.set_page_config(
    page_title="Diet Recommendation System",
    page_icon=f"data:image/svg+xml;base64,{logo_64}",
    layout="wide",
    initial_sidebar_state="expanded",
)

custom_css = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background: url("https://i.imgur.com/coDI0QL.jpg");
    background-size: cover;
    height: 100vh;
}

[data-testid="stToolbar"] {
right: 2rem;
}

[data-testid="stHeader"] {
background: rgba(0,0,0,0);
}
</style>
"""

# Include custom CSS
st.markdown(custom_css, unsafe_allow_html=True)