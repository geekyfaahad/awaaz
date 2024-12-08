import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create a structured dataset
data = [
    {
        "timestamp": "2024-12-06 10:51:13",
        "HTTPX_uvloop_avg_time": 683.159065246582,
        "HTTPX_uvloop_std_dev": 140.15181547585402,
        "AIOHTTP_uvloop_avg_time": 339.404296875,
        "AIOHTTP_uvloop_std_dev": 6.25442377915556,
        "Trio_asks_avg_time": 751.331615447998,
        "Trio_asks_std_dev": 292.00339180766395,
        "Httptools_response": "Request sent using httptools",
        "Httptools_time_taken": 0
    },
    {
        "timestamp": "2024-12-06 10:51:23",
        "HTTPX_uvloop_avg_time": 702.9914379119873,
        "HTTPX_uvloop_std_dev": 224.09313732964944,
        "AIOHTTP_uvloop_avg_time": 467.0353889465332,
        "AIOHTTP_uvloop_std_dev": 212.33085381856176,
        "Trio_asks_avg_time": 593.2182312011719,
        "Trio_asks_std_dev": 28.342757268337305,
        "Httptools_response": "Request sent using httptools",
        "Httptools_time_taken": 0
    },
    {
        "timestamp": "2024-12-06 10:51:32",
        "HTTPX_uvloop_avg_time": 714.2147541046143,
        "HTTPX_uvloop_std_dev": 207.94777068858127,
        "AIOHTTP_uvloop_avg_time": 343.27502250671387,
        "AIOHTTP_uvloop_std_dev": 18.048864836224524,
        "Trio_asks_avg_time": 630.359697341919,
        "Trio_asks_std_dev": 36.31435002733324,
        "Httptools_response": "Request sent using httptools",
        "Httptools_time_taken": 0
    },
    {
        "timestamp": "2024-12-06 10:51:41",
        "HTTPX_uvloop_avg_time": 605.8053016662598,
        "HTTPX_uvloop_std_dev": 17.055871296762007,
        "AIOHTTP_uvloop_avg_time": 363.3927822113037,
        "AIOHTTP_uvloop_std_dev": 37.455989747266344,
        "Trio_asks_avg_time": 582.7519416809082,
        "Trio_asks_std_dev": 40.18189519554695,
        "Httptools_response": "Request sent using httptools",
        "Httptools_time_taken": 0
    },
    # Add more data points if necessary...
]

# Convert data into a DataFrame
df = pd.DataFrame(data)

# Convert timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Generate summary statistics
summary_stats = df.describe()

# Correlation matrix for avg_time columns
correlation_matrix = df[['HTTPX_uvloop_avg_time', 'AIOHTTP_uvloop_avg_time', 'Trio_asks_avg_time']].corr()

# Create plots
plt.figure(figsize=(12, 8))

# Line plot of average response times
plt.subplot(2, 2, 1)
plt.plot(df['timestamp'], df['HTTPX_uvloop_avg_time'], label='HTTPX (uvloop)', marker='o')
plt.plot(df['timestamp'], df['AIOHTTP_uvloop_avg_time'], label='AIOHTTP (uvloop)', marker='o')
plt.plot(df['timestamp'], df['Trio_asks_avg_time'], label='Trio (asks)', marker='o')
plt.title('Average Response Times Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Average Response Time (ms)')
plt.xticks(rotation=45, fontsize=8)
plt.legend()
plt.tight_layout()

# Bar plot of standard deviations
plt.subplot(2, 2, 2)
plt.bar(df['timestamp'], df['HTTPX_uvloop_std_dev'], label='HTTPX (uvloop)', alpha=0.6)
plt.bar(df['timestamp'], df['AIOHTTP_uvloop_std_dev'], label='AIOHTTP (uvloop)', alpha=0.6)
plt.bar(df['timestamp'], df['Trio_asks_std_dev'], label='Trio (asks)', alpha=0.6)
plt.title('Standard Deviations Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Standard Deviation (ms)')
plt.xticks(rotation=45, fontsize=8)
plt.legend()
plt.tight_layout()

# Heatmap of correlation matrix
plt.subplot(2, 2, 3)
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", cbar=True)
plt.title('Correlation Matrix')
plt.tight_layout()

# Summary statistics text visualization
plt.subplot(2, 2, 4)
plt.axis('off')
stats_text = summary_stats[['HTTPX_uvloop_avg_time', 'AIOHTTP_uvloop_avg_time', 'Trio_asks_avg_time']].to_string()
plt.text(0.5, 0.5, stats_text, fontsize=10, ha='center', va='center', family='monospace')
plt.title('Summary Statistics')

# Show the plot
plt.tight_layout()
plt.show()
