from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

def get_youtube_comments(video_url, max_comments=200, scroll_delay=2, num_scrolls=10):
    """
    Extracts YouTube comments up to a specified maximum using Selenium.

    Args:
        video_url (str): URL of the YouTube video.
        max_comments (int, optional): Maximum number of comments to extract. Defaults to 200.
        scroll_delay (int, optional): Delay (in seconds) between scroll actions. Defaults to 2.
        num_scrolls (int, optional): Number of times to scroll. Defaults to 10.
    """

    driver = webdriver.Chrome()  # Replace with your preferred webdriver
    driver.set_page_load_timeout(10)

    try:
        driver.get(video_url)
        driver.maximize_window()

        # Wait for comments section to load
        comments_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "placeholder-area"))
        )

        comments_list = []
        num_comments_fetched = 0
        last_height = driver.execute_script("return arguments[0].scrollHeight", comments_section)

        for _ in range(num_scrolls):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", comments_section)
            sleep(scroll_delay)

            # Check if new comments have been loaded
            new_height = driver.execute_script("return arguments[0].scrollHeight", comments_section)
            if new_height == last_height:
                break  # No new comments loaded, likely reached the end

            last_height = new_height

            # Extract comments using a reliable XPath
            comments = driver.find_elements(By.XPATH, """//ytd-comment-thread-renderer//yt-formatted-string[@class="style-scope ytd-comment-renderer"]""")
            comments_list.extend([comment.text.strip() for comment in comments])
            num_comments_fetched = len(comments_list)

        print(f"Fetched {num_comments_fetched} comments (limited to {max_comments} or reached end).")

    except TimeoutException:
        print("Error: Comments section not loaded within timeout.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        driver.quit()

# Example usage
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=nVTQMFY-w5c"  # Replace with your video URL
    get_youtube_comments(video_url, num_scrolls=20)  # Increase number of scrolls