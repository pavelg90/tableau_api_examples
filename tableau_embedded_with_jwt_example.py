from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, HTTPException
import uvicorn
import xml.etree.ElementTree as ET
import jwt
import datetime
import uuid
import requests

app = FastAPI()


"""

  It's a workling example wrapped in FastAPI for like... faster reaction.
  The homepage is wierd to the right page...
  
"""

@app.get("/")
def read_root():
    #return {"message": "Hello World"}
    return RedirectResponse(url="/tableau_embed")


def get_token(jwt_token):
    # The URL for the Tableau auth endpoint (adjust for your Tableau Server/Cloud instance)
    auth_url = "https://<your_site_url>.online.tableau.com/api/3.7/auth/signin"
    headers = {
        "X-Tableau-Auth": "your_connected_app_client_id",
        "Content-Type": "application/json",
    }
    payload = {
        "credentials": {
            "jwt": jwt_token,
            "site": {
                "contentUrl": "your_site"
            }
        }
    }
    response = requests.post(auth_url, json=payload, headers=headers)
    response_text = response.text
    if response.status_code == 200:
        root = ET.fromstring(response_text)
        namespaces = {'t': 'http://tableau.com/api'}
        token = root.find('.//t:credentials', namespaces=namespaces).attrib['token']
        site_id = root.find('.//t:site', namespaces=namespaces).attrib['id']
    else:
        token = None
    return token


def generate_jwt():
    secretId = "secretId"
    secretValue = "secretValue"
    clientId = "clientId"
    username = "username"
    tokenExpiryInMinutes = 1  # Max of 10 minutes.

    scopes = ["tableau:views:embed"]

    kid = secretId
    iss = clientId
    sub = username
    aud = "tableau"
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=tokenExpiryInMinutes)
    jti = str(uuid.uuid4())
    scp = scopes

    userAttributes = {
        # User attributes are optional.
        # Add entries to this dictionary if desired.
        # "[User Attribute Name]": "[User Attribute Value]",
    }

    payload = {
                  "iss": clientId,
                  "exp": exp,
                  "jti": jti,
                  "aud": aud,
                  "sub": sub,
                  "scp": scp,
              } | userAttributes

    token = jwt.encode(
        payload,
        secretValue,
        algorithm="HS256",
        headers={
            "kid": kid,
            "iss": iss,
        },
    )

    return token


@app.get("/tableau_embed")
def tableau_embed():
    signed_jwt = generate_jwt()
    resp_token = get_token(signed_jwt)

    tableau_url = f"https://tableau_url.online.tableau.com/t/sittableaudemo/views/tableau_url/tableau_url_sheet_01"
    """
        Below is an HTML from Tableau Playground with minor changes...
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your Embed Project</title>
        <!--- Load Tableau JavaScript API V3  --->
        <script type="module" src="https://embedding.tableauusercontent.com/tableau.embedding.3.1.0.min.js"></script>
    </head>
    <body>
    
    <!--- Viz Component - renders on page load --->
    
         <tableau-viz
            id="tableauViz"
            width="1000"
            height="1000"
            hide-tabs=false
            touch-optimize=false
            disable-url-actions=false
            debug=false
            src="{tableau_url}"
            device="Desktop"
            toolbar="bottom"
            token= "{signed_jwt}"
            >   
        </tableau-viz>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # uvicorn main:app --reload  # Run it from terminal (call this file main.py)
