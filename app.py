import datetime
import random
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import numpy as np


def convert_df_csv(df):
    return df.to_csv(index=False).encode('utf-8')


def random_timestamp_from_range(date_range) -> str:
    """Generates a random timestamp between a start and end date.

    :param date_range: tuple of start and end date
    :return: str timestamp between date range
    """
    datetime_range = [datetime.combine(d, datetime.min.time()) for d in date_range]  # Convert date to datetime
    start, end = datetime_range  # Split tuple
    random_timestamp = start + (
            (end + timedelta(days=1)) - start) * random.random()  # Get random date between start and end

    return datetime.strftime(random_timestamp, '%Y-%m-%d %T')  # Return as string


def generate_logs_df(usernames, date_range, quantity, bias) -> pd.DataFrame:
    """Creates a DataFrame of dummy login attempts within provided parameters.

    :param bias: bias towards successful logins
    :param usernames: List of usernames
    :param date_range: Start and end date of logs
    :param quantity: Number of rows to generate
    :return: DataFrame of generated dummy logs
    """
    df = pd.DataFrame(columns=['log_id', 'username', 'timestamp', 'successful'])  # Create empty DataFrame

    for row in range(quantity):  # Generate each log row
        username = random.choice(usernames)  # Pick random username from list
        timestamp = random_timestamp_from_range(date_range)  # Fetch timestamp
        successful = np.random.choice(['Y', 'N'], p=[bias, 1 - bias])  # Pick success or failure with probability

        insert_row = {
            'log_id': row + 1,
            'username': username,
            'timestamp': timestamp,
            'successful': successful,
        }
        df = pd.concat([df, pd.DataFrame([insert_row])])  # Concat each new row to DataFrame

    return df.set_index(df.log_id)


def main():
    st.set_page_config('Log Generator', '📋')
    st.title("Login Record Generator")

    st.header('Input')
    with st.form('params'):
        usernames = st.text_area('Usernames', help="Seperated by comma or newline").strip()
        usernames = [u.strip().lower() for u in usernames.replace('\n', ',').split(',')]
        date_range = st.date_input('Date range', [])
        quantity = st.number_input('Records', min_value=1, value=50)
        bias = st.slider('Success probability', min_value=0.00, max_value=1.00, value=0.75,
                         help='Chance that each login attempt will be successful')
        output_type = st.selectbox('Output as', ['CSV', 'DataFrame'])

        submit = st.form_submit_button('Generate')

    if submit:
        df_logs = generate_logs_df(usernames, date_range, quantity, bias)

        st.header('Output')

        if output_type == 'CSV':
            csv = convert_df_csv(df_logs)  # Convert to file
            st.download_button(  # Allow user to download
                "Download CSV",
                csv,
                'output.csv',
                'text/csv',
            )

        st.dataframe(df_logs)  # Show results


if __name__ == '__main__':
    main()
