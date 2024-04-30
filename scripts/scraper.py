from playwright.sync_api import sync_playwright
import os

NUM_GOOGLE_PAGES = 30
MAX_TIMEOUT = 20000
ARTICLE_MIN_CHARS = 1024
ARTICLE_MAX_CHARS = 1024 * 52 # Longest true article found in testing was 51 kB
MAX_LINK_CHARS_IN_FILENAME = 72
OUTPUT_DIRECTORY_NAME = 'news_content'
SAVE_SCREENSHOTS = False
BLACKLISTED_WEBSITES = ['elblog.pl']

def save_content_to_file(content, index, link):
    os.makedirs(OUTPUT_DIRECTORY_NAME, exist_ok=True)
    truncated_link = link.replace("https://", "").replace("www.", "").replace("/", "")[:MAX_LINK_CHARS_IN_FILENAME]
    file_path = os.path.join(OUTPUT_DIRECTORY_NAME, truncated_link + '.txt')
    file_exists = os.path.exists(file_path)
    if not file_exists:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content if content else "Content was not found.")
        print(f'Content saved for article {index}')
    else:
        print(f'File already exists: {file_path}')

def run(playwright):
    browser = playwright.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
    page = browser.new_page()

    try:
        print('Opening Google...')
        page.goto('https://www.google.com/search?q=artificial+intelligence+news&tbm=nws&tbs=qdr:w', timeout=MAX_TIMEOUT)
        # Accept cookies
        page.get_by_role("button", name="Zaakceptuj wszystko").click()

        valid_links = []
        for i in range(NUM_GOOGLE_PAGES):
            print('Collecting article links... page ' + str(i+1))
            page.wait_for_selector('#search', timeout=MAX_TIMEOUT)
            links = page.query_selector_all('#search a:visible')
            
            for link in links:
                href = link.get_attribute('href')
                if href and 'https://' in href:
                    is_blacklisted = False
                    for blacklisted_website in BLACKLISTED_WEBSITES:
                        if blacklisted_website in href:
                            is_blacklisted = True
                            break
                    if not is_blacklisted:
                        valid_links.append(href)

            next_page_button = page.query_selector("#pnnext")
            if next_page_button:
                next_page_button.click()
            else:
                print("No more pages or next page button not found.")
                break

        print(f'Found {len(valid_links)} valid links. Processing content...')
        for index, link in enumerate(valid_links, start=1):
            print(f'Processing link {index}: {link}')
            try:
                page.goto(link, timeout=MAX_TIMEOUT)
                content_elements = page.query_selector_all('h1:visible, h2:visible, h3:visible, h4:visible, h5:visible, h6:visible, p:visible')
                content = "\n".join([element.text_content() or '' for element in content_elements])
                content = link + "\n" + content
                if len(content) >= ARTICLE_MIN_CHARS:
                    content = content[:ARTICLE_MAX_CHARS]
                    save_content_to_file(content, index, link)
                    if SAVE_SCREENSHOTS:
                        page.screenshot(path=f"{OUTPUT_DIRECTORY_NAME}/screenshot_{index}.png")
                else:
                    print('Content too short to save.')
            except Exception as e:
                print(f'Failed to process link {index}: {e}')

    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
