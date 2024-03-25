import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from login_to_sheets_account import loginToSheets

from models import Indexes

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
collumns = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
            "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", 'z']
# The ID and range of a sample spreadsheet.


def pushToSheets(data: list, indexes: Indexes, suspectsUsers: list, suspectsUsersDic: dict[int], suspectsCards: list, suspectsCardsDic: dict[int]) -> None:
    SAMPLE_SPREADSHEET_ID = "16Jc8QNSbyZGZLPcl4qIiG32g1b6XNB1tnHzivA0zNcw"
    # Create the range of tables, based on the keys of each list
    DATA_RANGE = f"Data!A2:{collumns[len(data[0])+1]}"
    USER_ANALYSIS_RANGE = f"Users Analysis!A23:{collumns[len(suspectsUsers[0])-1]}"
    CARD_ANALYSIS_RANGE = f"Cards Analysis!A18:{collumns[len(suspectsCards[0])-1]}"
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
            row[indexes.transaction_amount] = row[indexes.transaction_amount].replace(
                '.', ',')

            userId = row[indexes.user_id]
            cardNumber = row[indexes.card_number]

            # Add recommendation to the row if the user is suspicious
            if userId not in suspectsUsersDic and cardNumber not in suspectsCardsDic:
                row.insert(indexes.recommendation, "Approve")

            else:
                recommendationAdded = False
                if userId in suspectsUsersDic:
                    user = suspectsUsersDic[userId]
                    recommendationAdded = True

                    if user['score'] < 50:
                        row.insert(indexes.recommendation, "Approve")
                    elif user['score'] < 75:
                        row.insert(indexes.recommendation,
                                   "Suggestted Rejection")
                    else:
                        row.insert(indexes.recommendation, "Reject")

                if cardNumber in suspectsCardsDic:
                    card = suspectsCardsDic[cardNumber]

                    if recommendationAdded:
                        row[indexes.recommendation] = "Reject"
                    else:
                        if card['score'] < 75:
                            row.insert(indexes.recommendation,
                                       "Suggestted Rejection")
                        else:
                            row.insert(indexes.recommendation, "Reject")

        # Update the spreadsheet Data page with the new values
        result = (
            sheet.values()
            .update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=DATA_RANGE, valueInputOption="USER_ENTERED", body={"values": data})
            .execute()
        )

        # Update the spreadsheet User Analysis page with the new values
        (
            sheet.values()
            .update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=USER_ANALYSIS_RANGE, valueInputOption="USER_ENTERED", body={"values": suspectsUsers})
            .execute()
        )

        # Update the spreadsheet Card Analysis page with the new values
        (
            sheet.values()
            .update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=CARD_ANALYSIS_RANGE, valueInputOption="USER_ENTERED", body={"values": suspectsCards})
            .execute()
        )

        print(f"{result.get('updatedCells')} células atualizadas, na página de Dados.")
    except HttpError as err:
        print("Erro ao atualizar planilha")
        print(err)
