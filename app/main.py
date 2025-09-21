import os
import requests
from fastapi import FastApi, Request
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv()
app=FastApi()

CLIENT_ID=os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET=os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI=os.getenv("SPOTIFY_REDIRECT_URI")

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SCOPE = "user-read-email user-library-read"

#endpoint para el login
@app.get("/login")
def login():
  auth_url=(
    f"{SPOTIFY_AUTH_URL}"
    f"?response_type=code"
    f"&scope={SCOPE}"
    f"&redirect_uri={REDIRECT_URI}"
  )
  return RedirectResponse(auth_url)

#callback de spotigy
@app.get("/callback")
def callback(code:str):
  payload={
    "grant_type":"authorization_code",
    "code":code,
    "redirect_uri":REDIRECT_URI,
    "client_id":CLIENT_ID,
    "client_secret":CLIENT_SECRET,
  }
  response=requests.post(SPOTIFY_TOKEN_URL, data=payload)
  tokens=response.json()
  
  access_token=tokens.get("access_token")
  
  #obtengo los datos del user
  user_info=requests.get(
    "https://api.spotify.com/v1/me",
    headers={"Authorization":f"Bearer {access_token}"}
  ).json()
  return {"tokens":tokens, "user_info":user_info}