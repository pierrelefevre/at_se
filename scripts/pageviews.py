import pymongo
import os
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv


load_dotenv()


def get_db():
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    return client["at"]


def get_pageviews():
    collection = get_db()["events"]
    return list(collection.find({"event": "pageview"}).sort("timestamp", 1))


def pageviews_linechart():
    pageviews = get_pageviews()

    df = pd.DataFrame(pageviews)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Set timestamp as the index (optional, but useful for time series)
    df.set_index("timestamp", inplace=True)

    # Count page views per time unit (e.g., per day)
    pageviews_per_day = df.resample("D").count()

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(pageviews_per_day["event"])
    plt.title("Page Views Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Page Views")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    pageviews_linechart()
