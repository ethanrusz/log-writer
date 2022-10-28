import datetime
import random
from datetime import datetime

import streamlit as st
import pandas as pd


def random_timestamp_from_range(date_range) -> str:
    """Generates a random timestamp between a start and end date.

    :param date_range: tuple of start and end date
    :return: str timestamp between date range
    """
    datetime_range = [datetime.combine(d, datetime.min.time()) for d in date_range]  # Convert date to datetime
    start, end = datetime_range  # Split tuple
    random_timestamp = start + (end - start) * random.random()  # Get random date between start and end

    return datetime.strftime(random_timestamp, '%Y-%m-%d %T')  # Return as string


def generate_logs_df(usernames, date_range, quantity) -> pd.DataFrame:
    """Creates a DataFrame of dummy login attempts within provided parameters.

    :param usernames: List of usernames
    :param date_range: Start and end date of logs
    :param quantity: Number of rows to generate
    :return: DataFrame of generated dummy logs
    """
    df = pd.DataFrame(columns=['log_id', 'username', 'timestamp', 'successful'])  # Create empty DataFrame

    for row in range(quantity):  # Generate each log row
        username = random.choice(usernames)  # Pick random username from list
        timestamp = random_timestamp_from_range(date_range)  # Fetch timestamp
        successful = random.choice(['Y', 'N'])  # Randomly pick success

        df = df.append({  # Add to DataFrame
            'log_id': row + 1,
            'username': username,
            'timestamp': timestamp,
            'successful': successful
        }, ignore_index=True)

    return df


def main():
    st.set_page_config('TMC Log Generator', '📋')
    st.title("Log Generator")

    st.header('Input')
    with st.form('params'):
        usernames = st.text_area('Usernames', help="Seperated by comma or newline").strip()
        usernames = [u.strip().lower() for u in usernames.replace('\n', ',').split(',')]
        date_range = st.date_input('Date Range', [])
        quantity = st.slider('Records', min_value=1, max_value=500, value=50)
        st.selectbox('Output as', ['DataFrame', 'CSV'], disabled=True)

        submit = st.form_submit_button('Generate')

    if submit:
        df_logs = generate_logs_df(usernames, date_range, quantity)
        st.header('Output')
        st.info('Only DataFrame output is available for now.')
        st.dataframe(df_logs)


if __name__ == '__main__':
    main()
