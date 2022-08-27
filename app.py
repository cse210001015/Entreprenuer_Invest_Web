import pyrebase
import streamlit as st
from datetime import datetime


# Configuration Key
firebaseConfig = {
    'apiKey': "AIzaSyCrji1YWuk7Vgww8ReFlqoPjx9vsh-ZBls",
    'authDomain': "hackathon-57ace.firebaseapp.com",
    'projectId': "hackathon-57ace",
    'databaseURL':"https://console.firebase.google.com/project/hackathon-57ace/database/hackathon-57ace-default-rtdb/data/~2F",
    'storageBucket': "hackathon-57ace.appspot.com",
    'messagingSenderId': "1073013511677",
    'appId': "1:1073013511677:web:5afc7475c42830738ff594",
    'measurementId': "G-YMSF6KKCDD"
  }


# Firebase Configuration
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


# Database
db = firebase.database()
storage = firebase.storage()


st.sidebar.title("Welcome to our app")

# Authentication

choice = st.sidebar.selectbox('Login/Sign Up',['Login','Sign Up'])

email = st.sidebar.text_input('Please enter you E-Mail')
password = st.sidebar.text_input("Password:", value="", type="password")

if choice == 'Sign Up':
    handle = st.sidebar.text_input('Tell us what should we call you', value = 'Default')
    submit = st.sidebar.button('Create Account')

    if submit :
        try:
            user = auth.create_user_with_email_and_password(email,password)
            st.success('Your account has been created successfully')
            st.balloons()
            # Sign In
            user = auth.sign_in_with_email_and_password(email,password)
            db.child(user['localId']).child("Handle").set(handle)
            db.child(user['localId']).child("Id").set(user['localId'])
            st.title('Welcome ' + handle)
            st.info('Login via login drop down')
        except Exception as e:
            e=str(e)
            e=e.split('{')
            e=e[3]
            e=str(e)
            e=e.split(',')
            e=e[0]
            e=str(e)
            e=e.split(':')
            e=e[1]
            e=str(e)
            e=e.split('"')
            e=e[1]
            e=str(e)
            e=e.replace('_',' ')   
            st.sidebar.header(e)

if choice=='Login':
    login = st.sidebar.button('Login')
    if login:
        try:
            user=auth.sign_in_with_email_and_password(email,password)
            bio = st.radio('Jump to',['Home','My feed','Settings'])

        except:
            st.sidebar.header("Invalid Credentials")
    
    

