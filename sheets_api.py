import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from login_to_sheets_account import loginToSheets

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
collumns = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
            "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", 'z']
# The ID and range of a sample spreadsheet.


def pushToSheets(data: list, currencyPosition: int) -> None:
    SAMPLE_SPREADSHEET_ID = "16Jc8QNSbyZGZLPcl4qIiG32g1b6XNB1tnHzivA0zNcw"
    SAMPLE_RANGE_NAME = f"Data!A2:{collumns[len(data[0])]}"
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        loginToSheets()

    try:
        print("Atualizando planilha")
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()

        for row in data:
            # Spreadsheet only understands it as a number if it has a comma instead of a dot, here I make this change
            row[currencyPosition] = row[currencyPosition].replace('.', ',')

        # Update the spreadsheet with the new values
        result = (
            sheet.values()
            .update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption="USER_ENTERED", body={"values": data})
            .execute()
        )

        print(f"{result.get('updatedCells')} células atualizadas.")
    except HttpError as err:
        print("Erro ao atualizar planilha")
        print(err)
