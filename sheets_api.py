import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from login_to_sheets_account import loginToSheets

from models import Suspect

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
collumns = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
            "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", 'z']
# The ID and range of a sample spreadsheet.


def pushToSheets(data: list, currencyPosition: int, suspects: list[Suspect]) -> None:
    SAMPLE_SPREADSHEET_ID = "16Jc8QNSbyZGZLPcl4qIiG32g1b6XNB1tnHzivA0zNcw"
    # Create the range of tables, based on the keys of each list
    SAMPLE_RANGE_NAME = f"Data!A2:{collumns[len(data[0])]}"
    USER_ANALYSIS_RANGE = f"Users Analysis!A19:{collumns[len(suspects[0])-1]}"
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

        # Update the spreadsheet Data page with the new values
        result = (
            sheet.values()
            .update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption="USER_ENTERED", body={"values": data})
            .execute()
        )

        # Update the spreadsheet User Analysis page with the new values
        (
            sheet.values()
            .update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=USER_ANALYSIS_RANGE, valueInputOption="USER_ENTERED", body={"values": suspects})
            .execute()
        )

        print(f"{result.get('updatedCells')} células atualizadas, na página de Dados.")
    except HttpError as err:
        print("Erro ao atualizar planilha")
        print(err)
