import pandas as pd

from .post import Post

class PostAnalysisService:
  def __init__(self):
    pass

  def get_posts_by_dates(self, posts: list[Post]) -> pd.Series:
    df = pd.DataFrame([post.to_dict() for post in posts])
    print(posts)
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.date
    df["updated_at"] = pd.to_datetime(df["updated_at"]).dt.date

    return df.groupby("updated_at").size()

