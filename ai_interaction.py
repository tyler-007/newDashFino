import pandas as pd
import numpy as np
import openai
import random


from config import organisation as organization_name
from config import apikey
openai.api_key = apikey  # Replace with your actual API key

def get_completion(prompt, model="gpt-4.0-turbo", temperature=0.5):
    """Generates a completion using OpenAI's GPT model."""
    response = openai.Completion.create(  # Use correct method for OpenAI 1.4.1
        model=model,
        prompt=prompt,
        instructions=[
            "Use evidence from the provided dataset to support your claims.",
            "Avoid making claims that are not supported by the data.",
            "Be factual and objective in your analysis.",
            "Focus on the most significant findings from each sentiment category.",
            "Present insights as concise bullet points with corresponding percentage stats."
        ],
        temperature=temperature,
    )
    return response.choices[0].text.content 

def labelling(data):
    """Labels data by sentiment."""
    sentiment_content_dict = {}
    for index, row in data.iterrows():
        sentiment = row['Sentiment']
        content = row['Content']
        sentiment_content_dict[sentiment] = sentiment_content_dict.get(sentiment, []) + [content]
    return sentiment_content_dict

def generate_suggestions(api_key,data):
    """Generates suggestions for each sentiment category."""
    openai.api_key = api_key
    random_number = random.randint(500, 1000)
    data = data.sample(n=random_number, random_state=42)
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
        response = get_completion(prompt)
        suggestions.append((sentiment, response))
    return suggestions


