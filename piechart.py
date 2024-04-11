import matplotlib.pyplot as plt
import pandas as pd
import os

def generate_dashboard(df):
    if not os.path.exists('images'):
        os.makedirs('images')
    
    file_paths = []
    
    # Generate pie chart for overall sentiment
    sentiment_fig_path = plot_piechart(df, 'Sentiment', "images/sentiment_fig.png")
    file_paths.append(sentiment_fig_path)
    
    # Get unique source values
    sources = df['Source'].unique()
    
    for source in sources:
        source_df = df[df['Source'] == source]
        file_path = f"images/{source}_fig.png"
        source_fig_path = plot_piechart(source_df, 'Sentiment', file_path)
        file_paths.append(source_fig_path)
    
    return file_paths

def plot_piechart(data, column, file_path, background_color=None):
    sentiment_counts = data[column].value_counts()
    if background_color is None:
        background_color = '#ffffff' # White
    colors = {'Positive': 'purple', 'Negative': 'red', 'Neutral': 'white'}
    labels = sentiment_counts.index.tolist()
    counts = sentiment_counts.values.tolist()
    explode = [0.1] * len(counts) # Dynamically calculate explode based on the number of categories
    
    fig, ax = plt.subplots(figsize=(8, 6))
    patches, texts, autotexts = ax.pie(counts, labels=None, autopct='%1.1f%%', startangle=140,
                                       colors=[colors[label] for label in labels], explode=explode,
                                       textprops=dict(color="#4169E1"))
    ax.axis('equal')
    ax.set_facecolor(background_color)
    fig.patch.set_facecolor('black')
    
    for text, label in zip(autotexts, labels):
        text.set_text(f'{text.get_text()} - {label}')
    
    plt.legend(patches, labels, loc="best")
    
    # Save the figure as an image
    plt.savefig(file_path)
    plt.close(fig) # Close the figure to release memory
    
    return file_path
'''import matplotlib.pyplot as plt
import pandas as pd
import os

def generate_dashboard(df):
    if not os.path.exists('images'):
        os.makedirs('images')
    
    file_paths = []
    
    sentiment_fig_path = plot_piechart(df, 'Sentiment', "images/sentiment_fig.png")
    file_paths.append(sentiment_fig_path)
    
    sources = df['Source'].unique()
    
    for source in sources:
        source_df = df[df['Source'] == source]
        file_path = f"images/{source}_fig.png"
        source_fig_path = plot_piechart(source_df, 'Sentiment', file_path)
        file_paths.append(source_fig_path)
    
    return file_paths

def plot_piechart(data, column, file_path, background_color=None):
    sentiment_counts = data[column].value_counts()
    if background_color is None:
        background_color = '#ffffff' 
    colors = {'Positive': 'purple', 'Negative': 'red', 'Neutral': 'white'}
    labels = sentiment_counts.index.tolist()
    counts = sentiment_counts.values.tolist()
    explode = [0.1] * len(counts) 
    
    fig, ax = plt.subplots(figsize=(8, 6))
    patches, texts, autotexts = ax.pie(counts, labels=None, autopct='%1.1f%%', startangle=140,
                                       colors=[colors[label] for label in labels], explode=explode,
                                       textprops=dict(color="#4169E1"))
    ax.axis('equal')
    ax.set_facecolor(background_color)
    fig.patch.set_facecolor('black')
    
    for text, label in zip(autotexts, labels):
        text.set_text(f'{text.get_text()} - {label}')
    
    plt.legend(patches, labels, loc="best")
      
    plt.savefig(file_path)
    plt.close(fig) 
    
    return file_path
    '''