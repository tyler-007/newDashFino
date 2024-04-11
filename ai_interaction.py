import pandas as pd
import numpy as np
import openai
from config import organisation as organization_name
# Upgrade OpenAI library to the latest version

# Use the most powerful available model with optimized parameters
model_name = "gpt-3.5-turbo-instruct"  # Adjust if needed for fine-tuned models
temperature = 0.5  # Balance creativity and coherence
max_tokens = 150  # Adjusted for batch processing
stop = None  # Prevent premature truncation

def get_completion(prompt, data_batch=""):
    messages = [
        {"role": "system", "content": f"You are a kind business insights employee with speciality in online media sentiment analysis, you work in an organization - {organization_name} provided by the user."},
        {"role": "assistant", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=stop,
        input_text=data_batch  # Include data batch as input
    )

    return response.choices[0].message["content"]

def labelling(data):
    sentiment_content_dict = {}
    for index, row in data.iterrows():
        sentiment = row['Sentiment']
        content = row['Content']
        if sentiment in sentiment_content_dict:
            sentiment_content_dict[sentiment].append(content)
        else:
            sentiment_content_dict[sentiment] = [content]
    return sentiment_content_dict

def generate_suggestions(api_key, data):
    openai.api_key = api_key
    dict_obt = labelling(data)

    all_insights = []
    for sentiment in dict_obt.keys():
        data_batch = dict_obt[sentiment]  # Access content for sentiment

        # Split data into batches (adjust batch_size as needed)
        batch_size = 200
        data_batches = [data_batch[i:i + batch_size] for i in range(0, len(data_batch), batch_size)]

        insights = []
        for batch in data_batches:
            batch_text = " ".join(batch)  # Combine content into a single string
            prompt = f"""
As a business insights expert at {organization_name}, you have been tasked with analyzing the {sentiment} feedback received from various social media platforms. The dataset contains comments categorized as {sentiment}:

{batch_text}

Your objective is to thoroughly analyze the {sentiment} feedback by reading, memorizing, and interpreting all comments in this category. After analysis, you are required to present the top 5 insights derived from the sentiment. These insights should reflect the prevailing sentiment of the people and provide a deeper understanding of their feelings.

Furthermore, for each insight, you must provide a percentage stat indicating the proportion of comments expressing the same sentiment out of the total comments analyzed. For example, "35% of the total positive comments expressed satisfaction with the user interface (UI)."

The top 5 insights will be compiled as bullet points and presented to the Directors of the company for review and action.

Please ensure that your analysis is concise and focuses on the most significant findings. Limit your output to only 5 bullet points, each accompanied by its respective percentage stat.

"""
            response = get_completion(prompt)
            insights.append(response)

        all_insights.append(insights)

    return all_insights

