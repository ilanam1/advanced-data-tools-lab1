from app.db.repositories.post_repository import PostRepository
from app.services.youtube_api_service import YouTubeAPIService
from app.services.reddit_service import RedditService


class AppController:
    def __init__(self):
        self.repo = PostRepository()

    def run_youtube_api_collection(self):
        youtube_service = YouTubeAPIService()

        posts = youtube_service.collect_posts_for_query(
            query="chatgpt",
            videos_limit=100,
            comments_per_video=100
        )

        inserted = self.repo.insert_many([post.to_dict() for post in posts])

        return {
            "source": "YouTube API",
            "collected": len(posts),
            "inserted": inserted
        }

    def run_reddit_selenium_collection(self):
        reddit_service = RedditService(headless=False)

        posts = reddit_service.scrape_subreddit("chatgpt", limit=100)

        inserted = self.repo.insert_many([post.to_dict() for post in posts])

        return {
            "source": "Reddit Selenium",
            "collected": len(posts),
            "inserted": inserted
        }

    def get_gpt_data_summary(self):
        return {
            "total_records": self.repo.count_all(),
            "youtube_count": self.repo.count_by_source("youtube"),
            "reddit_count": self.repo.count_by_source("reddit"),
            "api_count": self.repo.count_by_collection_method("api"),
            "scraping_count": self.repo.count_by_collection_method("scraping"),
            "avg_text_length": self.repo.get_average_text_length(),
            "top_topics": self.repo.get_top_topics(limit=5),
            "top_authors": self.repo.get_top_authors(limit=5),
            "source_breakdown": self.repo.get_source_breakdown(),
            "method_breakdown": self.repo.get_method_breakdown(),
            "posts_per_month": self.repo.get_posts_per_month(),
            "posts_per_month_by_source": self.repo.get_posts_per_month_by_source(),
        }