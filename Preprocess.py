import pandas as pd
import re

def preprocessing(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s'
    m = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({'User_Message': m, 'message_date': dates})

    # for extracting user name and their messages
    user_name = []
    messages = []
    for i in range(0, len(df['User_Message'])):
        entry = df['User_Message'].values[i].split(':')
        if (len(entry) <= 1):
            user_name.append("group_notification")
            messages.append(entry[0])
        else:
            user_name.append(entry[0])
            messages.append(entry[1])
    df['user'] = user_name
    df['message'] = messages



    dates = []
    for i in range(len(df['message_date'])):
        dates.append(df['message_date'].values[i].split(',')[0])
    df['date'] = pd.to_datetime(dates, infer_datetime_format=True)
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month_name()
    df['year'] = df['date'].dt.year
    df['day_name'] = df['date'].dt.day_name()


    # converting message date type to extract info
    time = []
    for i in range(len(df['message_date'])):
        time.append(df['message_date'].values[i].split(',')[1].split(' ')[1])
    df['time'] = pd.to_datetime(time, infer_datetime_format=True)
    df['hour'] = df['time'].dt.hour
    df['minute'] = df['time'].dt.minute

    # creating period column
    periods = []
    for i in range(len(df['message_date'])):
        periods.append(df['message_date'].values[0].split(',')[1].split('-')[0].split(' ')[2])
    df['period'] = periods



    df.drop(columns=['User_Message', 'message_date', 'time'], inplace=True)
    df.rename(
        columns={'year': 'Year', 'month': 'Month', 'day': 'Day', 'hour': 'Hour', 'minute': 'Minutes', 'user': 'User',
                 'message': 'Message'}, inplace=True)

    hour_min = []
    for hour in df[['day_name', 'Hour', 'period']]['Hour']:
        if hour == 12:
            hour_min.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            hour_min.append(str('12') + "-" + str(hour + 1))
        else:
            hour_min.append(str(hour) + "-" + str(hour + 1))

    df['hour_min'] = hour_min
    df['btw_time'] = df['hour_min'] + " " + df['period']
    return df


