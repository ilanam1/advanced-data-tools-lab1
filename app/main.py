from app.db.repositories.post_repository import PostRepository
from app.services.youtube_api_service import YouTubeAPIService


def main():
    repo = PostRepository()
    youtube_service = YouTubeAPIService()

    query = "chatgpt"
    posts = youtube_service.collect_posts_for_query(
        query=query,
        videos_limit=5,
        comments_per_video=5
    )

    inserted = repo.insert_many([post.to_dict() for post in posts])

    print(f"Collected {len(posts)} records from YouTube API")
    print(f"Inserted {inserted} new records into MongoDB")

    saved_posts = repo.find_by_source("youtube")
    print(f"Total YouTube records in DB: {len(saved_posts)}")

    for post in saved_posts[:3]:
        print(post)


if __name__ == "__main__":
    main()