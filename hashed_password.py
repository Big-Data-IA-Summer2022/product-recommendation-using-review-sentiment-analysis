import pickle
from pathlib import Path

import streamlit_authenticator as stauth
passwords=['adina','abhijit','ta','professor','user']
hashed_passwords = stauth.Hasher(passwords).generate()
print(hashed_passwords)