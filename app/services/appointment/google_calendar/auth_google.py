from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=8188)

with open("token.json", "w") as token:
    token.write(creds.to_json())

print("Autenticação feita com sucesso. token.json gerado!")