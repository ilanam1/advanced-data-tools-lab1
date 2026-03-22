import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.models.post import Post


class RedditService:
    def __init__(self, headless: bool = False):
        self.headless = headless

    def _create_driver(self):
        # הגדרות לדפדפן כרום
        options = webdriver.ChromeOptions()

        # אם רוצים ריצה ללא פתיחת חלון
        if self.headless:
            options.add_argument("--headless=new")

        # הגדרות מומלצות ליציבות
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        return driver

    def scrape_subreddit(self, subreddit: str, limit: int = 10):
        """
        סקרייפינג של פוסטים ציבוריים מ-Reddit לפי subreddit.
        מחזיר רשימת אובייקטים מסוג Post כדי להשתלב עם המבנה הקיים בפרויקט.
        """
        driver = self._create_driver()
        posts_data = []

        try:
            url = f"https://www.reddit.com/r/{subreddit}/"
            driver.get(url)

            # המתנה לטעינת הפוסטים
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "shreddit-post"))
            )

            # המתנה קטנה נוספת ליציבות
            time.sleep(3)

            # ננסה למשוך יותר פוסטים ע"י גלילה
            last_count = 0
            scroll_attempts = 0
            max_scroll_attempts = 5

            while scroll_attempts < max_scroll_attempts:
                posts = driver.find_elements(By.TAG_NAME, "shreddit-post")

                if len(posts) >= limit:
                    break

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                if len(posts) == last_count:
                    scroll_attempts += 1
                else:
                    scroll_attempts = 0

                last_count = len(posts)

            posts = driver.find_elements(By.TAG_NAME, "shreddit-post")

            for post in posts[:limit]:
                try:
                    title = post.get_attribute("post-title") or ""
                    author = post.get_attribute("author") or ""
                    post_url = post.get_attribute("permalink") or ""
                    subreddit_name = post.get_attribute("subreddit-prefixed-name") or f"r/{subreddit}"
                    created_at = post.get_attribute("created-timestamp") or ""
                    comments_count = post.get_attribute("comment-count") or ""
                    score = post.get_attribute("score") or ""

                    # אם הקישור יחסי - נהפוך אותו למלא
                    if post_url and post_url.startswith("/"):
                        post_url = f"https://www.reddit.com{post_url}"

                    reddit_post = Post(
                        source="reddit",
                        collection_method="scraping",
                        topic=subreddit.lower(),
                        title=title,
                        text="",
                        author=author,
                        created_at=created_at,
                        url=post_url,
                        extra={
                            "subreddit": subreddit_name,
                            "score": score,
                            "comment_count": comments_count,
                        }
                    )

                    posts_data.append(reddit_post)

                except Exception as e:
                    print(f"Error while parsing single Reddit post: {e}")

        except Exception as e:
            print(f"Error while scraping Reddit subreddit '{subreddit}': {e}")

        finally:
            driver.quit()

        return posts_data