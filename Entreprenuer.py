import pyrebase
import streamlit as st
from datetime import datetime
import json
from google.cloud import firestore
from google.oauth2 import service_account
from streamlit_elements import elements
from streamlit_elements import html
from streamlit_elements import mui



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
        user = auth.create_user_with_email_and_password(email,password)
        st.success('Your account has been created successfully')
        st.balloons()
        # Sign In
        user = auth.sign_in_with_email_and_password(email,password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("Id").set(user['localId'])
        st.title('Welcome ' + handle)
        st.info('Login via login drop down')

if choice=='Login':
    login = st.sidebar.button('Login')
    if login:
        try:
            user=auth.sign_in_with_email_and_password(email,password)
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            bio = st.radio('Jump to',['Home','My feed','Settings'])
            
        except:
            st.sidebar.header("Invalid Credentials")

        if bio == 'Home':
          @st.experimental_singleton
          def get_db():
            key_dict = json.loads(st.secrets["textkey"])
            creds = service_account.Credentials.from_service_account_info(key_dict)
            db = firestore.Client(credentials=creds, project="hackathon-57ace")
            return db


          @st.experimental_memo
          def get_all_messages():
            db = get_db()
            all_messages = db.collection("messages").stream()
            return [m.to_dict() for m in all_messages]


          def main():
           if "page" not in st.session_state:
            st.session_state.page = 0

          def handle_change(_, page):
            st.session_state.page = page - 1

          all_messages = get_all_messages()

          st.title(":balloon: App| Admin dashboard")

        with elements("main"):
             mui.Divider()

             message = all_messages[st.session_state.page]["message"]
             author = all_messages[st.session_state.page]["name"]
             author = author if author != "" else "anonymous"

        with mui.Box(
              sx={
                  "my": 3,
                  "p": 3,
                  "bgcolor": "background.paper",
                  "boxShadow": 1,
                  "borderRadius": 2,
               }
           ):
              mui.Typography(message)
              mui.Typography(
                  f"by {author}",
                  typography="subtitle2",
                  fontWeight="light",
                  textAlign="right",
                  sx={"mt": 3},
               )

              mui.Pagination(count=len(all_messages), defaultPage=1, onChange=handle_change)


        if __name__ == "__main__":
            st.set_page_config(page_title="Web App | Admin", page_icon=":balloon:")
            main()
 