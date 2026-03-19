import requests
from app.config.settings import YOUTUBE_API_KEY
from app.models.post import Post


class YouTubeAPIService:
    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self):
        if not YOUTUBE_API_KEY:
            raise ValueError("Missing YOUTUBE_API_KEY in .env file")
        self.api_key = YOUTUBE_API_KEY

    def search_videos(self, query: str, max_results: int = 10):
        url = f"{self.BASE_URL}/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "key": self.api_key,
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        videos = []
        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]

            videos.append({
                "video_id": video_id,
                "title": snippet.get("title", ""),
                "description": snippet.get("description", ""),
                "published_at": snippet.get("publishedAt"),
                "channel_title": snippet.get("channelTitle"),
                "url": f"https://www.youtube.com/watch?v={video_id}",
            })

        return videos

    def get_video_statistics(self, video_ids: list[str]):
        if not video_ids:
            return {}

        url = f"{self.BASE_URL}/videos"
        params = {
            "part": "snippet,statistics",
            "id": ",".join(video_ids),
            "key": self.api_key,
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        stats_map = {}
        for item in data.get("items", []):
            video_id = item["id"]
            snippet = item.get("snippet", {})
            statistics = item.get("statistics", {})

            stats_map[video_id] = {
                "title": snippet.get("title", ""),
                "description": snippet.get("description", ""),
                "published_at": snippet.get("publishedAt"),
                "channel_title": snippet.get("channelTitle"),
                "view_count": statistics.get("viewCount"),
                "like_count": statistics.get("likeCount"),
                "comment_count": statistics.get("commentCount"),
            }

        return stats_map

    def get_video_comments(self, video_id: str, max_results: int = 20):
        url = f"{self.BASE_URL}/commentThreads"
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": max_results,
            "textFormat": "plainText",
            "key": self.api_key,
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        comments = []
        for item in data.get("items", []):
            top_comment = item["snippet"]["topLevelComment"]["snippet"]

            comments.append({
                "author": top_comment.get("authorDisplayName"),
                "text": top_comment.get("textDisplay"),
                "published_at": top_comment.get("publishedAt"),
                "like_count": top_comment.get("likeCount"),
            })

        return comments

    def collect_posts_for_query(self, query: str, videos_limit: int = 10, comments_per_video: int = 10):
        videos = self.search_videos(query=query, max_results=videos_limit)
        video_ids = [video["video_id"] for video in videos]
        stats_map = self.get_video_statistics(video_ids)

        posts = []

        for video in videos:
            video_id = video["video_id"]
            video_stats = stats_map.get(video_id, {})

            try:
                comments = self.get_video_comments(video_id, max_results=comments_per_video)
            except requests.HTTPError:
                comments = []

            if not comments:
                post = Post(
                    source="youtube",
                    collection_method="api",
                    topic=query,
                    title=video_stats.get("title", video["title"]),
                    text=video_stats.get("description", video["description"]),
                    author=video_stats.get("channel_title", video["channel_title"]),
                    created_at=video_stats.get("published_at", video["published_at"]),
                    url=video["url"],
                    extra={
                        "video_id": video_id,
                        "view_count": video_stats.get("view_count"),
                        "like_count": video_stats.get("like_count"),
                        "comment_count": video_stats.get("comment_count"),
                        "comment_author": None,
                        "comment_text": None,
                        "comment_like_count": None,
                    },
                )
                posts.append(post)
            else:
                for comment in comments:
                    post = Post(
                        source="youtube",
                        collection_method="api",
                        topic=query,
                        title=video_stats.get("title", video["title"]),
                        text=comment["text"] or "",
                        author=comment["author"],
                        created_at=comment["published_at"],
                        url=f"{video['url']}#comment",
                        extra={
                            "video_id": video_id,
                            "video_url": video["url"],
                            "channel_title": video_stats.get("channel_title", video["channel_title"]),
                            "video_published_at": video_stats.get("published_at", video["published_at"]),
                            "view_count": video_stats.get("view_count"),
                            "video_like_count": video_stats.get("like_count"),
                            "video_comment_count": video_stats.get("comment_count"),
                            "comment_like_count": comment["like_count"],
                        },
                    )
                    posts.append(post)

        return posts