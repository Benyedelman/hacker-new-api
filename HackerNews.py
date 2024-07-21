


from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt

colors = [ 'gold', 'lightcoral', 'lightskyblue', 'lightgreen', 'orange','lightpink', 'lightsalmon', 'lightseagreen', 'lightslategray', 'lightsteelblue',
    'lime', 'limegreen', 'mediumaquamarine', 'mediumblue', 'mediumorchid','mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise',
    'mediumvioletred', 'midnightblue', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orchid',
    'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip','peachpuff', 'peru', 'pink', 'plum', 'powderblue',
    'purple', 'rebeccapurple', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna']


# Function to fetch top stories
def fetch_top_stories_ids():
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    response = requests.get(url)
    return response.json()

# Function to fetch story details
def fetch_story_details(story):
    url = f'https://hacker-news.firebaseio.com/v0/item/{story}.json'
    response = requests.get(url)
    return response.json()

# Function to fetch comment details
def fetch_comment_details(comment):
    url = f'https://hacker-news.firebaseio.com/v0/item/{comment}.json'
    response = requests.get(url)
    return response.json()

def calculate_time_passed(timestamp):
    current_time = datetime.now().timestamp()
    time_passed = current_time - timestamp
    days_passed = time_passed // (24 * 3600)
    time_passed = time_passed % (24 * 3600)
    hours_passed = time_passed // 3600
    time_passed %= 3600
    minutes_passed = time_passed // 60
    time_passed %= 60
    seconds_passed = time_passed
    return (f"{int(days_passed)} days, {int(hours_passed)} hours, {int(minutes_passed)} minutes, {int(seconds_passed)} seconds")


# Fetch and save top stories and comments details to CSV
def fetch_and_save_data(num_stories):
    top_stories_ids = fetch_top_stories_ids()[:num_stories]
    stories_data = []
    comments_data = []
    for story in top_stories_ids:
        story_details = fetch_story_details(story)
        story_details['time'] = calculate_time_passed(story_details['time'])
        stories_data.append({'author': story_details.get('by'),
            'title': story_details.get('title'),
            'url': story_details.get('url'),
            'score': story_details.get('score'),
            'time': story_details.get('time'),
            'num_comments': story_details.get('descendants')})
        
        for comment in story_details['kids']:
            comment_details = fetch_comment_details(comment)
            comments_data.append({
            'story_title': story_details.get('title', ''),
            'text': comment_details.get('text', ''),})

    stories_df = pd.DataFrame(stories_data)                          # Convert lists to DataFrames
    comments_df = pd.DataFrame(comments_data)
    stories_df.to_csv('stories.csv', index=False)                    # Save to CSV files
    comments_df.to_csv('comments.csv', index=False)

# Analyze and plot data with top num_stories 
def analyze_and_plot(num_stories, colors):
    stories_df = pd.read_csv('stories.csv')                          # Read the data from CSV
    df_sorted = stories_df.sort_values('score', ascending=False)     # Sort by score in descending order to get top stories by score
    sizes = df_sorted['score'].tolist()                              # Prepare data for plotting
    title = df_sorted['title'].tolist()
    # presentation
    plt.figure(figsize = (15, 8))                                      # screen size
    patches, texts = plt.pie(sizes, colors = colors, startangle = 90)  # Circle calculation
    plt.legend(patches, title, loc = 'best', fontsize = 'medium')      # Text settings
    plt.title(f'Top {num_stories} Hacker News Stories by Score')       # Title definitions
    plt.savefig('top_stories_pie_chart.png')                           # file name
    plt.show()

# Main function
if __name__ == '__main__':
    num_stories = 4
    fetch_and_save_data(num_stories)
    analyze_and_plot(num_stories, colors)



