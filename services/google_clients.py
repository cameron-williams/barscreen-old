import base64
import mimetypes
import os
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from ssl import SSLError
from google.cloud import storage

# This can be turned into a list of scopes if we start
# adding more google services to this API
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/analytics.readonly', 'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.compose']

KEYFILE_DICT = {
    "type": "service_account",
    "project_id": "barscreentv-234500",
    "private_key_id": "a461b461e26ab9b5c9ef0913053e307943d3e1f3",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC6VaCUqzFdBIbD\nUU0e48n2ju5dsNrra78c511PoFK6ENo+zCnQ7K1SvKlhlRBdDEo15bNG9MZ7rFYQ\n4S30XtD2oJ6ss2XJTIvtvWGsz1e1VsiAcmOc3gBmgyL2w86CZ1ONaxk+3x3LY5IR\nIAegguNXB7jOxFhhnsFKvQrzDMqiblVlPGPqm/4FT1NJS4SsrK4z2xj7Kj5FbhhB\ndNCy9Kb3NN621Ahy+GBLYmo14uCZSVfYyJpZFyrdsnZgejQA/DQ0STr9mEqakHpn\nVlCFmhSA3hIAxbXPE4FWSyLiJkbF4zdufc8lpH0QM6QbePyjzt0LhEcpX3TKwthd\nP01pm4XtAgMBAAECggEACVkybUMJfvkzKalyjRIwl8Yj/19YHGeTdwfEjrIkdGFU\nEcJ8dpbpOzVr6hFoeMKdFocnr2+oZZwH1WD2xUPciAMW8uMtQCQvAQZ3WAwvAlIQ\nTSFwDfa1Xm9F2cuJGNHGR1oQMi9Pd1zPfzx0JYFrlno0s2r2ZC9q0y0Y14jUwcFh\nbQ86tjZjl4Kp6nIbxwmfHtUiodfkFICBLYRWsbBhJbkjwc0r00duNW5zIc/u6Bds\n2kSaAWthlNWOSgBTHczA6cGHBVONjQCOm13e1KgkxZ1lN4qaYLL7BD/KvfHlhsmF\nPsECVTtjbXSyo5BJIUqlwVKm+RmiHdABD4dz6+jRAQKBgQDbFz1+DFxXvrWelN4o\nGULqFaH4RGkeza6nIPnIbdt/0EoNJAPPi4erV+5B7uDGUo8fRJ1BvxWxB66wWQgk\n50HgEig9HNJCO7z58RX6t1u/KiYzCOTyMXiu+9SCi0iywyF9dg3uLa7q0/hTbXFq\nYH+koHqdRkXTEEVHCwyEJkhO1QKBgQDZubOMX7hYlJhZXihcfJHF84ldNj8axAEG\nJagsjMzxHCZ/v5Z65LH+EjwOGK1WEenMEUDQWM7KK2pN2XYFR9SW5YU2pgX24wWs\nYVkUNRjZj9qIATwtPyJReqJOS+pjX6ODwmIXS5n1NL9bP42+/KGDefR2hP/X9h76\nn2T4VuNWuQKBgFaA8pKWJs+uSN94P87tSnJKYE06FZdH9rGeX4E3fvcUMmjF04ta\nuBJ7AWOfAbjMWB4sZTrUS6g+NEcEoCaR+HyULrcSbiIgnBjDi74WL29nIPX9iQfn\naJMOc3WnsOiECvESb6We+/VUBDRMff9WYo+JnWADowYW4oOOZT64LsyRAoGAGkB3\n068e7R9Nl0jxGOW0Nef9Yg3OYg3MCc+0jVqUw2Wfhru1CzBT/cx5DUIQdFZImGBk\nLjrnBB1j/esAffaBPYiDHWm7Ql9xKa27LeKREnpz4P41IUeBfc2JkGM66ax4bMSd\nSy3EbHplsDzjfGm9l7q2rSuwJXv5lEJvzDm9w5ECgYA932ge141VNN4B/xjetLK/\nXfT8DdrkCDaOdzps3Ah76mSk8cHVqLtWi5ZsTdEZGukZ0ftf/DFBUc+psLVloTde\nUWQBIodBNNTHRvS0Hwh3545vi0JKDtjTTcLTmoci6qMHpOEfLlt/gks9dDdLO3Gj\n3K3OgbB9Zbbug+ul2ey/uw==\n-----END PRIVATE KEY-----\n",
    "client_email": "barscreen@barscreentv-234500.iam.gserviceaccount.com",
    "client_id": "115300422717438665854",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/barscreen%40barscreentv-234500.iam.gserviceaccount.com"
}

MAX_GOOGLE_API_RETRIES = 2


def get_credentials(delegated_user=None):
    """Uses the JSON client auth file and oauth client to create
    a valid session with google API
    :param delegated_user: Optional string email for which account you want to impersonate
    Returns:
        Credentials, the obtained credential.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        keyfile_dict=KEYFILE_DICT, scopes=SCOPES)
    if delegated_user:
        credentials = credentials.create_delegated(delegated_user)
    return credentials


class API:
    """
    Superclass that can be subclassed to interact with different google services
    """

    def __init__(self, credentials=None, delegated_user=None):
        self.credentials = credentials if credentials else get_credentials(
            delegated_user=delegated_user)

    def build(self):
        return discovery.build(self.service, self.version, credentials=self.credentials)


class Sheets(API):
    """
    Class to Interact with the Google Sheets API
    More info at: https://developers.google.com/sheets/api/reference/rest/
    """

    service = 'sheets'
    version = 'v4'

    def create(self, title):
        """
        Method to create a new google sheet
        Refer here to see what values are returned:
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#Spreadsheet

        :param title: Title of the spreadsheet
        :return: Information of the created sheet
        """
        sheets_api = self.build()
        body = {'properties': {'title': title}}
        sheet_info = sheets_api.spreadsheets().create(body=body).execute()
        return sheet_info

    def append(self, spreadsheet_id, values, cell_range='Sheet1', apply_formatting=True):
        """
        Appends data to a sheet
        :param spreadsheet_id:   ID of the sheet
        :param values:           A list of values that needs to be appended
        :param cell_range:       Cell range of the value to be inserted, Starts at A1:1 on sheet1 by default
        :param apply_formatting: Bool, if set to True will apply the default filtering as requested by Media Buyers
        """
        sheets_api = self.build()
        body = {'values': values}
        sheets_api.spreadsheets().values().append(spreadsheetId=spreadsheet_id, body=body, range=cell_range,
                                                  valueInputOption='RAW').execute()
        # Add formatting as we insert the data ( if apply_formatting is True )
        apply_formatting and self.batchUpdate(
            spreadsheet_id=spreadsheet_id) or None

    def get(self, spreadsheet_id, worksheet_name="Sheet1"):
        """
        Gets a full spreadsheet's data
        :param spreadsheet_id: ID of the sheet
        :param worksheet_name: the specific sheet (tabs at bottom of Google Sheet) whose cells we want to retrieve
        """
        sheets_api = self.build()

        request = sheets_api.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=worksheet_name)
        response = request.execute()

        return response

    def batchUpdate(self, spreadsheet_id, sheet_id=0):
        """
        NOTE: We are currently using this just for formatting of Cells
        To use it for data insertion as well, we'd need to pass more params and change the method.
        Currently it just auto resizes the cells and adds a basic filter as wanted by the Atlas team.
        This method should be changed to support passing of custom filters if needed in future

        For more info on how to add formatting and what are available, refer here:
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/request

        Updates data/formatting on a sheet
        :param spreadsheet_id: Id of the Spreadsheet
        :param sheet_id: Sheet id on the spreadsheet, if it's only one sheet it'll be at 0 which is the default
        """
        sheets_api = self.build()
        body = {
            "requests": [
                {
                    "setBasicFilter": {
                        "filter": {
                            "range": {
                                "sheetId": sheet_id
                            }
                        },
                    }
                },
                {
                    "updateSheetProperties": {
                        "properties": {
                            "sheetId": sheet_id,
                            "gridProperties": {
                                "frozenRowCount": 1,
                            }
                        },
                        "fields": 'gridProperties.frozenRowCount'
                    },
                }

            ],
        }
        sheets_api.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()

    def addSheet(self, spreadsheet_id, sheet_name):
        """
        Adds a new sheet {sheet_name} to given spreadsheet id.
        :param spreadsheet_id: Id of the Spreadsheet
        :param sheet_name:     Name of the new sheet
        """
        sheets_api = self.build()
        body = {
            "requests": [{
                "addSheet": {
                    "properties": {
                        "title": sheet_name,
                    },
                }
            }]
        }
        sheets_api.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()

    def copySheet(self, spreadsheet_id, sheet_id, destination_spreadsheet_id):
        """
        Copies given sheet_id from given spreadsheet_id to the given destination id
        :param spreadsheet_id:             ID of spreadsheet to copy from
        :param sheet_id:                   ID of sheet to copy
        :param destination_spreadsheet_id: ID of spreadsheet to copy sheet to
        """
        sheets_api = self.build()
        body = {
            "destinationSpreadsheetId": destination_spreadsheet_id
        }
        sheets_api.spreadsheets().sheets().copyTo(spreadsheetId=spreadsheet_id,
                                                  sheetId=sheet_id, body=body).execute()


class Drive(API):
    """
    Class to interact with the Google Drive API
    More info at: https://developers.google.com/drive/v3/web/about-sdk
    """

    service = 'drive'
    version = 'v3'

    def get_latest_google_sheet_id(self):
        drive_api = self.build()
        files = drive_api.files().list(orderBy="modifiedTime desc",
                                       q="mimeType='application/vnd.google-apps.spreadsheet'").execute()
        return files['files'][0]['id']

    def get_latest_atlas_google_sheet_id(self):
        drive_api = self.build()
        files = drive_api.files().list(orderBy="modifiedTime desc",
                                       q="mimeType='application/vnd.google-apps.spreadsheet'").execute()
        for drive_file in files['files']:
            if 'Atlas Offer Aggregator' in drive_file['name']:
                return drive_file['id']
        return None

    def get_latest_sheet_by_name(self, name):
        drive_api = self.build()
        files = drive_api.files().list(orderBy="modifiedTime desc",
                                       q="mimeType='application/vnd.google-apps.spreadsheet'").execute()
        for drive_file in files['files']:
            if name in drive_file['name']:
                return drive_file['id']
        return None

    def set_domain_permissions(self, role, file_id, domain):
        drive_api = self.build()
        body = {'role': role,
                'domain': domain,
                'type': 'domain'}

        drive_api.permissions().create(fileId=file_id, body=body).execute()

    def set_email_permissions(self, role, file_id, email_list):
        drive_api = self.build()
        body = {'role': role,
                'emailAddress': email_list,
                'type': 'user'}

        drive_api.permissions().create(fileId=file_id, body=body).execute()


class Analytics(API):
    """
    Class to interact with the Google Analytics API
    More info at: https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
    """

    service = 'analyticsreporting'
    version = 'v4'

    def getReport(self, start_date, end_date, view_id, metrics=None, dimensions=None):
        """
        getReport method to Analytics API.
        :param start_date: YYYY-MM-DD
        :param end_date:   YYYY-MM-DD
        :param view_id:    string, the view for the property to get reporting on

        :param metrics: see below
        :param dimensions: for a list of dimensions/metrics please see
        https://developers.google.com/analytics/devguides/reporting/core/dimsmets#mode=web&cats=session
        When adding metrics/dimensions you can either add just by name (without ga:) or with.
        """
        analytics_api = self.build()
        body = {
            "reportRequests": [
                {
                    "viewId": view_id,
                    "dateRanges": [
                        {"endDate": end_date, "startDate": start_date}
                    ],
                    "metrics": [],
                    "dimensions": [],
                    "pageSize": 100000
                }
            ]
        }
        if metrics:
            for m in metrics:
                body["reportRequests"][0]["metrics"].append(
                    {"expression": "ga:" in m and m or "ga:{}".format(m)})
        if dimensions:
            for d in dimensions:
                body["reportRequests"][0]["dimensions"].append(
                    {"name": "ga:" in d and d or "ga:{}".format(d)})
        return analytics_api.reports().batchGet(body=body).execute()


class Gmail(API):
    """
    Class to interact with the Google Gmail API. To access a specific user's email, initialize with
    gmail = Gmail(delegated_user="email@address")
    More info at https://developers.google.com/gmail/api/quickstart/python
    """
    service = 'gmail'
    version = 'v1'

    def list_emails(self, page_token=None):
        """
        List all emails for currently authenticated user. See
        https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#list
        """
        gmail_api = self.build()
        return gmail_api.users().messages().list(userId="me", pageToken=page_token).execute()

    def get_email(self, message_id):
        """
        Retrieves message data on given message_id. See
        https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#get
        """
        gmail_api = self.build()
        return gmail_api.users().messages().get(userId="me", id=message_id).execute()

    def get_attachment(self, message_id, attachment_id):
        """
        Returns the raw attachment data for given message/attachment id
        https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.attachments.html#get
        """
        gmail_api = self.build()
        attachment_response = gmail_api.users().messages().attachments().get(userId="me", messageId=message_id,
                                                                             id=attachment_id).execute()
        return base64.urlsafe_b64decode(attachment_response["data"].encode("UTF-8"))

    def get_csv_attachment(self, message_id, attachment_id):
        """
        Returns a dictified list of a csv attachment id/ message id given
        https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.attachments.html#get
        :return: [{col_header: 1st_row_value, col_header: 1st_row_value},
                  {col_header: 2nd_row_value, col_header: 2nd_row_value},
                  {etc}]
        """
        gmail_api = self.build()
        attachment_response = gmail_api.users().messages().attachments().get(userId="me", messageId=message_id,
                                                                             id=attachment_id).execute()
        file_data = base64.urlsafe_b64decode(
            attachment_response["data"].encode("UTF-8")).split("\n")
        headers = file_data[0].split(",")
        return [{headers[i].strip(): col_val.strip() for i, col_val in enumerate(row.split(","))} for row in
                file_data[1:]]

    def get_last_email_from_address(self, sender_address, page_token=None):
        """
        Retrieves the last received email from given sender_address
        :param sender_address: string | an email sender
        :return: email_id of last recieved, or NoneType
        """
        list_email_result = self.list_emails(page_token=page_token)
        for email in list_email_result["messages"]:
            current_email = self.get_email(email["id"])
            for header in current_email["payload"]["headers"]:
                if header["name"] == "From" and sender_address in header["value"]:
                    return email["id"]
        nextPageToken = list_email_result.get("nextPageToken", None)
        if nextPageToken:
            return self.get_last_email_from_address(sender_address=sender_address, page_token=nextPageToken)
        return None

    def send_email(self, to, subject, body, attachments=None):
        """
        Sends a new email from the currently authenticated user.
        :param to:          string | email address to send to "exampleemail@gmail.com"
        :param subject:     string | email subject
        :param body:        string | email body
        :param attachments: list   | an optional list of file paths to include as attachments
        :return:
        """
        gmail_api = self.build()
        sender = gmail_api.users().getProfile(
            userId="me").execute()['emailAddress']
        if not attachments:
            message = MIMEText(body)
            message['to'] = to
            message['from'] = sender
            message['subject'] = subject
            formatted_message = {
                'raw': base64.urlsafe_b64encode(message.as_string())}
        else:
            message = MIMEMultipart()
            message['to'] = to
            message['from'] = sender
            message['subject'] = subject

            msg = MIMEText(body)
            message.attach(msg)

            content_type, encoding = mimetypes.guess_type(file)

            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split('/', 1)
            if main_type == 'text':
                fp = open(file, 'rb')
                msg = MIMEText(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'image':
                fp = open(file, 'rb')
                msg = MIMEImage(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'audio':
                fp = open(file, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=sub_type)
                fp.close()
            else:
                fp = open(file, 'rb')
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(fp.read())
                fp.close()
            filename = os.path.basename(file)
            msg.add_header('Content-Disposition',
                           'attachment', filename=filename)
            message.attach(msg)

            formatted_message = {
                'raw': base64.urlsafe_b64encode(message.as_string())}
        try:
            sent_message = gmail_api.users().messages().send(
                userId='me', body=formatted_message).execute()
            return sent_message['id']
        except Exception as err:
            raise ("Err ({}){}".format(type(err), err))

# channel image
# video files for clips
# video files for promos
class GoogleStorage(object):
    """ Class for interactive with Google Cloud Storage """

    def __init__(self):
        self.client = storage.Client()
    
    def upload_channel_image(self, name, image_data):
        """ Takes image_data and a name and uploads the channel image """
        bucket = self.client.get_bucket("cdn.barscreen.tv")
        blob = bucket.blob("channel_images/{}".format(name))
        blob.upload_from_string(data=image_data)
        blob.make_public()
        return blob.public_url
    
    def upload_clip_video(self, name, file):
        bucket = self.client.get_bucket("cdn.barscreen.tv")
        if bucket.get_blob("clip_videos/{}".format(name)):
            raise ValueError("File already exists in cdn.")
        blob = bucket.blob("clip_videos/{}".format(name))
        blob.upload_from_file(file)
        blob.make_public()
        return blob.public_url
