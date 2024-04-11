import pandas as pd
import numpy as np
import openai
import random

from config import organisation as organization_name
from config import apikey

# Set your OpenAI API key here
openai.api_key = apikey

def get_completion(prompt, model="text-davinci-003", temperature=0.5):
    """Generates a completion using OpenAI's GPT model."""
    response = openai.Completion.create(
        engine=model,  # Adjusted to use the `engine` parameter
        prompt=prompt,
        temperature=temperature,
        max_tokens=500,  # You might want to adjust this based on your needs
    )
    return response.choices[0].text

def labelling(data):
    """Labels data by sentiment."""
    sentiment_content_dict = {}
    for index, row in data.iterrows():
        sentiment = row['Sentiment']
        content = row['Content']
        sentiment_content_dict[sentiment] = sentiment_content_dict.get(sentiment, []) + [content]
    return sentiment_content_dict

def generate_suggestions(api_key, data):
    """Generates suggestions for each sentiment category."""
    random_number = random.randint(500, 1000)  # Sample size
    data = data.sample(n=min(random_number, len(data)), random_state=42)  # Ensure not to exceed dataset size
    dict_obt = labelling(data)

    suggestions = []
    for sentiment, comments in dict_obt.items():
        prompt = f"""
As a business insights expert at {organization_name}, analyze the {sentiment} feedback from various social media platforms. The dataset contains comments categorized as {sentiment}.

- Thoroughly analyze the feedback by reading, memorizing, and interpreting all comments.
- Present the top 5 **factual insights** derived from the sentiment, supported by evidence from the dataset.
- For each insight, provide a **percentage stat** indicating the proportion of comments expressing the same sentiment.
- Limit output to 5 bullet points with corresponding percentage stats.
        """
        response = get_completion(prompt, model="gpt-4.0-turbo")  # Update the model to the latest
        suggestions.append((sentiment, response))
    return suggestions
