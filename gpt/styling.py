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


/* giant diagonal DNA background image */

.stApp:before{
content:"";
position:fixed;
top:-10%;
right:-5%;
width:900px;
height:1400px;
background-image:
url("https://images.unsplash.com/photo-1532187643603-ba119ca4109e");
background-size:cover;
opacity:.22;
transform:
rotate(-18deg);
z-index:-2;
filter:blur(1px);
}


/* left nav */

.sidebar-box{
position:fixed;
left:30px;
top:35px;
width:250px;
height:88vh;

background:
rgba(255,255,255,.55);

backdrop-filter:blur(20px);

border-radius:30px;

padding:35px;

box-shadow:
0 10px 50px rgba(0,0,0,.08);

z-index:999;
}


/* main content shifted */
.block-container{
margin-left:310px;
max-width:1200px;

background:
rgba(255,255,255,.45);

backdrop-filter:blur(20px);

border-radius:30px;

padding:3rem;

box-shadow:
0 10px 45px rgba(0,0,0,.08);
}


/* cards */

.metric-card{
background:white;
padding:28px;
border-radius:24px;
box-shadow:
0 8px 30px rgba(0,0,0,.06);
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
padding:.8rem 1.8rem;
font-weight:700;
}


/* titles */

h1{
font-size:48px;
font-weight:800;
color:#1e293b;
}

h2{
font-size:30px;
font-weight:700;
}

</style>


<div class='sidebar-box'>
<h2>StemQuant</h2>

<br>

<p>🏠 Dashboard</p>
<p>🧬 Prediction</p>
<p>ℹ About</p>
<p>📜 History</p>
<p>⚙ Settings</p>

</div>

""",
unsafe_allow_html=True)
 def load_style():
    load_css()