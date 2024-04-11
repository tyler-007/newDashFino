import pandas as pd
import io

def process_csv_file(uploaded_file):
    df = pd.read_csv(io.BytesIO(uploaded_file.read()))
    filtered_data = df[['Source', 'Screenname', 'Sentiment', 'Content']]
    removed = ['Fino Payments Bank', 'finopaymentsbank', 'Fino Payments Bank Ltd', 'FinoPaymntsBank']
    filtered_data = filtered_data[~filtered_data['Screenname'].isin(removed)]
    sources_req = ['Twitter.com', 'youtube.com', 'linkedin', 'Facebook.com', 'Instagram']
    filtered_data = filtered_data[filtered_data['Source'].isin(sources_req)]
    return filtered_data
