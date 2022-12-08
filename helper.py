import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

XLSFORM = os.getenv('XLSFORM')

survey_df = pd.read_excel(XLSFORM, sheet_name=0)
choice_df = pd.read_excel(XLSFORM, sheet_name=1)

style = """
    <style>
    td > div > table > tbody > tr > td {
        color: #264985;
        font-size: 0.9rem;

    }
    </style>
    """

def format_relevant(value):
    if str(value) == 'nan':
        return '-'
    return value

def format_question(value):
    if str(value) == 'nan':
        return 'Hidden from user'
    return value

def get_value(type, choice_name = ''):
    if type in ['select_one', 'select_multiple']:
        filtered_choice_df = choice_df[choice_df["list_name"]==choice_name]
        values = []
        for i, r in filtered_choice_df.iterrows():
            values.append([r["name"], '-', r["label::English (en)"]])
        return values
    if type in ['integer', 'decimal']:
        return 'User entered number'
    if type == 'text':
        return 'User entered text'
    if type == 'date':
        return 'User entered date'
    if type == 'time':
        return 'User entered time'
    if type == 'dateTime':
        return 'User entered date time'
    if type == 'image':
        return 'Captured image'
    if type == 'audio':
        return 'Recorded audio'
    if type == 'video':
        return 'Recorded video'
    if type == 'background-audio':
        return 'Background audio'
    if type == 'barcode':
        return 'User scanned barcode'
    if type == 'calculate':
        return 'Calculate field'
    if type in ['geopoint', 'geotrace', 'geoshape']:
        return 'Geographic coordinate'
    if type == 'file':
        return 'User upload file'
    if type == 'start':
        return 'Start date and time of the survey'
    if type == 'end':
        return 'End date and time of the survey'
    if type == 'today':
        return 'Day of the survey'
    if type == 'phonenumber':
        return 'Phone number (if available)'
    if type == 'username':
        return 'Username configured (if available)'
    if type == 'email':
        return 'Email address configured (if available)'
    if type == 'audit':
        return 'Log enumerator behavior during data entry'
    
    return "-"
