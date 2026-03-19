from app.models.post import Post
from app.db.repositories.post_repository import PostRepository


def main():
    repo = PostRepository()

    sample_post = Post(
        source="test_source",
        collection_method="manual_test",
        topic="docker_mongo_check",
        title="First test post",
        text="This is a test record stored after Docker Mongo setup.",
        author="Ilan",
        created_at="2026-03-19",
        url="http://example.com/test-post-1",
        extra={"note": "initial repository test"}
    )

    result = repo.insert_post(sample_post.to_dict())

    if result is not None:
        print("Post inserted successfully.")
    else:
        print("Post already exists.")

    all_posts = repo.get_all()
    print("\nAll posts in DB:")
    for post in all_posts:
        print(post)


if __name__ == "__main__":
    main()