import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import os

def generate_word_cloud(df):
    if not os.path.exists('images'):
        os.makedirs('images')
    
    file_paths = []
    
    # Generate word cloud for overall content
    content_fig_path = wrod(df['Content'], "images/Content_fig_wc.png")
    file_paths.append(content_fig_path)
    
    # Get unique source values
    sources = df['Source'].unique()
    
    for source in sources:
        source_df = df[df['Source'] == source]
        content_series = source_df['Content'].astype(str)
        file_path = f"images/{source}_fig_wc.png"
        source_fig_path = wrod(content_series, file_path)
        file_paths.append(source_fig_path)
    
    return file_paths

def wrod(Content_series, file_path):
    Content_series = Content_series.astype(str)
    text = ' '.join(Content_series.tolist())
    
    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    # Plot the word cloud
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    # Save the word cloud as an image
    plt.savefig(file_path)
    plt.close()
    
    return file_path
