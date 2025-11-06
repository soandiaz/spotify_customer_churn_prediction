import streamlit as st
import pickle
import warnings
import base64

def add_bg_image(image_file):
    with open(image_file, "rb") as img_file:
        encoded_img = base64.b64encode(img_file.read()).decode()
    page_bg = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_img}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position:center;

        
    }}
    h1, h2, h3, h4, h5, h6 {{
    color: #0cad17 !important; 
    text-align: left;      
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

def main():
    add_bg_image("spotify.jpg")
    warnings.filterwarnings('ignore')
    scaler = pickle.load(open('scaler.sav', 'rb'))
    encoder = pickle.load(open('encoder.sav', 'rb'))
    model = pickle.load(open('model.sav', 'rb'))
    if "page" not in st.session_state:
        st.session_state.page = "input"
    if st.session_state.page == "input":
        st.title('Spotify Customer Churn')
        gender = encoder[0].transform([st.selectbox(label='Gender of the customer: ', options=['Male', 'Female','Other'])])[0]
        age = st.text_input("Age of the customer: ")
        country_map = {
            'Canada': 'CA',
            'Germany': 'DE',
            'Australia': 'AU',
            'United States': 'US',
            'United Kingdom': 'UK',
            'India': 'IN',
            'France': 'FR',
            'Pakistan': 'PK'
        }
        selected_country = st.selectbox(label='Select the country the customer is in: ',options= list(country_map.keys()))
        country_code = country_map[selected_country]
        country= encoder[1].transform([country_code])[0]
        sub_type = encoder[2].transform([st.selectbox(label='Subscription type: ', options=['Free', 'Family', 'Premium', 'Student'])])[0]
        listen_time = st.text_input("Listening time of the customer in minutes: ")
        songs_played_per_day = st.text_input("Songs played per day by the customer: ")
        skip_rate_input= st.text_input("Percentage of songs skipped by the customer: ")
        if skip_rate_input:
            skip_rate = float(skip_rate_input) / 100
        else:
            skip_rate = 0.0
        Device_type = encoder[3].transform([st.selectbox(label='Device type: ', options=['Desktop', 'Web', 'Mobile'])])[0]
        ofl_ls={
            "Offline":1,
            "Online":0
        }
        offline_listening =ofl_ls[st.selectbox(label="Offline listening or online listening: ",options=list(ofl_ls.keys()))]
        features=[gender,age,country,sub_type,listen_time,songs_played_per_day,skip_rate,Device_type,offline_listening]
        pred = st.button("PREDICT")
        if pred:
            result = model.predict(scaler.transform([features]))[0]
            st.session_state.result = result
            st.session_state.page = "result"
            st.rerun()
    elif st.session_state.page == "result":

        if st.session_state.result:
            st.title(":red[Prediction Result]")
            st.error("This customer is **Churned**")
        else:
            st.title(":green[Prediction Result]")
            st.success("This customer is **Not Churned**")
        back=st.button("Go Back")
        if back:
            st.session_state.page="input"
            st.rerun()

main()