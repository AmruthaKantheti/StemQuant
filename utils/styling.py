import streamlit as st


def load_css():

    st.markdown("""
<style>

.stApp{
background:
linear-gradient(
135deg,
#eef2ff,
#f7f2ff
);
font-family:Segoe UI;
}


/* DNA */

.stApp:before{
content:"";
position:fixed;
top:-15%;
right:-6%;
width:950px;
height:1500px;

background:
url("https://images.unsplash.com/photo-1532187643603-ba119ca4109e?w=1400")
center/cover no-repeat;

opacity:.35;

transform:rotate(-18deg);

z-index:-2;

animation:
dnafloat 18s ease-in-out infinite alternate;
}


@keyframes dnafloat{
from{
transform:
rotate(-18deg)
translateY(0);
}
to{
transform:
rotate(-18deg)
translateY(60px);
}
}



/* panels */

.block-container{
max-width:1200px;
background:rgba(255,255,255,.42);
backdrop-filter:blur(18px);
border-radius:30px;
padding:3rem;
}



/* buttons */

.stButton button{
background:
linear-gradient(
90deg,
#6366f1,
#a855f7
);
color:white;
border:none;
border-radius:16px;
}


/* hide only menu/footer */
#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

/* KEEP HEADER */
header{
visibility:visible !important;
}

/* sidebar styling only
NO forced widths */
[data-testid="stSidebar"]{
background:
rgba(255,255,255,.60);
backdrop-filter:blur(18px);
}
                /* Lock sidebar open permanently */
section[data-testid="stSidebar"]{
min-width:320px !important;
max-width:320px !important;
}

/* Hide collapse control */
button[kind="header"]{
display:none !important;
}

</style>
""",
unsafe_allow_html=True)


def load_style():
    load_css()