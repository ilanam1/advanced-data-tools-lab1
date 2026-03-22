from app.db.repositories.post_repository import PostRepository
from app.services.youtube_api_service import YouTubeAPIService
from app.services.reddit_service import RedditService


class AppController:
    def __init__(self):
        self.repo = PostRepository()

    def run_youtube_api_collection(self):
        """
        איסוף נתונים מיוטיוב דרך API ושמירה ל-MongoDB
        """
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
        """
        איסוף נתונים מ-Reddit דרך Selenium ושמירה ל-MongoDB
        """
        reddit_service = RedditService(headless=False)

        posts = reddit_service.scrape_subreddit("chatgpt", limit=100)

        inserted = self.repo.insert_many([post.to_dict() for post in posts])

        return {
            "source": "Reddit Selenium",
            "collected": len(posts),
            "inserted": inserted
        }