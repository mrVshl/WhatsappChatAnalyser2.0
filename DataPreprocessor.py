import pandas as pd
import streamlit as st
import helper
import re

#Creating a function that will return preprocessed data
def preprocess(data):
    pattern1 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    pattern2 = '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'
    pattern3 = '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'


    format_1 = '%d/%m/%y, %H:%M - '
    format_2 = '%m/%d/%y, %H:%M - '

    match1 = re.split(pattern1,data)[1:]
    match2 = re.split(pattern2,data)[1:] 
    match3 = re.split(pattern3,data)[1:]

    if match1:
        messages = re.split(pattern1,data)[1:]
        dates = re.findall(pattern1,data)  

    elif match2:
        messages = re.split(pattern2,data)[1:]
        date = re.findall(pattern2,data)
        dates = helper.convertDateTimeFormat(date)

    elif match3:
        messages = re.split(pattern3,data)[1:]
        date = re.findall(pattern3,data)
        dates = helper.convertDateTimeFormat(date)

    else:
        st.markdown("<span style='color: red;'>This File format is not Supported by WhatsApp chat Analyser!!!</span>", unsafe_allow_html=True)

    df = pd.DataFrame({'User_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format= format_1, errors='coerce')  # convert message_date format
    df['message_date'] = pd.to_datetime(df['message_date'], format= format_2, errors='coerce')  # convert message_date format
    df.rename(columns={'message_date': 'Date'}, inplace=True)

    # seprating users, messages and notifications

    users = []
    message = []

    for messages in df['User_message']:
        entry = re.split('([\w\W]+?):\s', messages)
        if entry[1:]:
            users.append(entry[1])
            message.append(entry[2])
        else:
            users.append('group_notifications')
            message.append(entry[0])

    df['User'] = users
    df['message'] = message
    df.drop(columns=['User_message'], inplace=True)

    df['Year'] = df['Date'].dt.year
    df['only_date'] = df['Date'].dt.date
    df['Month'] = df['Date'].dt.month_name()
    df['month_num'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['day_name'] = df['Date'].dt.day_name()
    df['Hour'] = df['Date'].dt.hour
    df['Minutes'] = df['Date'].dt.minute

    period = []
    for hour in df[['day_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

