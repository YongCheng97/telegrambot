from __future__ import print_function
import pickle
import os.path
import gspread
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint
import main as botmain
from datetime import datetime, timedelta
import pytz


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
"""
def monthYear():
    tz= pytz.timezone('Asia/Singapore')
    date = datetime.now(tz).date().strftime("%d/%m/%Y")
    monthYear = date[3:10]
    checker = None
    if service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data):
        checker = true

    if not checker:
        spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
"""

def monthYear():
    tz= pytz.timezone('Asia/Singapore')
    date = str(datetime.now(tz).date())
    monthYear = date[0:7]
    return monthYear

currentMonthYear = "2019-09"

# The ID and range of a sample spreadsheet.
spreadsheet_id = '1Xvfrph-td1ScQnavx9a8caDMYnugOM9bQ_1h0rujZ_A'
range_ = monthYear() + "!A1:E9"
include_grid_data = False

# How the input data should be interpreted.
value_input_option = 'RAW'  # TODO: Update placeholder value.

# How the input data should be inserted.
insert_data_option = 'INSERT_ROWS'  # TODO: Update placeholder value.


spreadsheet = {
    'properties': {
        'title': monthYear()
    }
} 

batch_update_spreadsheet_request_body = {
    # A list of updates to apply to the spreadsheet.
    # Requests will be applied in the order they are specified.
    # If any request is not valid, no requests will be applied.
    'requests': [
        {
            "addSheet": {
                "properties": {
                    "title": monthYear(),
                }
            }
        }
    ], # TODO: Update placeholder value.

    # TODO: Add desired entries to the request body.
}

def generateBody():
    value_range_body = {
        # TODO: Add desired entries to the request body.
        "range": monthYear() + "!A1:E9",
        "majorDimension": 'ROWS',
        "values": [
            botmain.arr()
        ]
    }
    return value_range_body

def generateTopRow(): 
    value_range_body= {
        #TODO:Add desired entried to the request body.
        "range": monthYear() + "!A1:E9",
        "majorDimension": 'ROWS',
        "values": [
            ["Username", "Date", "Clock-in/Clock-out", "Time", "Activites"]
        ]
    }
    return value_range_body

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    #sheet = service.spreadsheets()
    #result = sheet.values().get(spreadsheetId=spreadsheet_Id,
                                #range=range_.execute()
    #values = result.get('values', [])
    global currentMonthYear
    #spreadSheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=range_, includeGridData=include_grid_data)
    #spreadSheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_, valueRenderOption=value_render_option, dateTimeRenderOption=date_time_render_option).execute()
    #print(spreadSheet)

    if currentMonthYear == monthYear():
        request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=generateBody())
        response = request.execute()
        pprint(response)

    else:
        request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=batch_update_spreadsheet_request_body).execute()
        request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=generateTopRow()).execute()
        currentMonthYear = monthYear()
        request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=generateBody())
        response = request.execute()
        pprint(response)


if __name__ == '__main__':
    main()