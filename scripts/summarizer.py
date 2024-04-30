import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY_XBERRY')
if not api_key:
    raise ValueError("No API key found. Please check your .env file.")

client = OpenAI(api_key=api_key)

# Path to the source directory and target directory
SOURCE_FOLDER = 'news_content'
TARGET_FOLDER = 'news_summaries'
PROMPT = '''
You are a master summarizer, specializing in writing short summaries for a business newsletter.
First you have to check: is the text provided by the user an article?
If yes, write a suitable title and a short, very concrete summary of the provided article.
If not, (it's something else, for example a list of articles or a broken page) respond instead with only the following tag: <no article />.
'''
NO_ARTICLE_TAG = '<no article />'
MAX_RESPONSE_TOKENS = 150

# Create the target directory if it does not exist
if not os.path.exists(TARGET_FOLDER):
    os.makedirs(TARGET_FOLDER)

# Iterate through all text files in the source directory
for filename in os.listdir(SOURCE_FOLDER):
    if filename.endswith('.txt'):
        file_path = os.path.join(SOURCE_FOLDER, filename)
        
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # Create the prompt for the GPT-3.5-turbo model
        #prompt = PROMPT + "\n" + file_content
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "system", "content": PROMPT},
                    {"role": "user", "content": file_content}],
            max_tokens=MAX_RESPONSE_TOKENS
        )

        # Get the summary from the response
        print('Summarizing ' + filename)
        summary_text = response.choices[0].message.content

        # Check if the summary contains "<no article />" and skip saving if it does
        if NO_ARTICLE_TAG not in summary_text:
            # Save the summary to a new file in the target directory
            summary_filename = os.path.splitext(filename)[0] + '.txt'
            summary_path = os.path.join(TARGET_FOLDER, summary_filename)
            with open(summary_path, 'w', encoding='utf-8') as summary_file:
                summary_file.write(summary_text)
        else:
            print(f"Skipping file '{filename}' as it contains {NO_ARTICLE_TAG} tag.")

print("Summaries have been processed.")
