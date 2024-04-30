import os
from dotenv import load_dotenv
import random
import re
from openai import OpenAI
from data_collator import collate_all_data

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY_XBERRY')
if not api_key:
    raise ValueError("No API key found. Please check your .env file.")

client = OpenAI(api_key=api_key)

SOURCE_FOLDER = 'news_summaries'
TARGET_FOLDER = 'news_best'
OUTPUT_FILE_BEST = os.path.join(TARGET_FOLDER, 'best_summaries.txt')
OUTPUT_FILE_BEST_OF_BEST = os.path.join(TARGET_FOLDER, 'best_of_best_summaries.txt')
OUTPUT_FILE_BEST_DEPTH_3 = os.path.join(TARGET_FOLDER, 'best_depth_3_summaries.txt')
MAX_RESPONSE_TOKENS = 300 # GPT needs some space in which to think, chain-of-thought like.
BEST_OF_BEST = True # Should we choose best of best?
BEST_DEPTH_3 = True # Should we choose best for the third time? (The absolute best)
N_FIRST_ROUND = 4 # Current implementation supports max 10
N_SECOND_ROUND = 4 # Current implementation supports max 10
N_THIRD_ROUND = 4 # Current implementation supports max 10
PROMPT = '''
IMPORTANT: Remember to end your response with: "So, the best article is <best_article_number>." (insert the number of the best article at the end)
You are a masterful content writer, specializing in selecting the most interesting stories.
You want to select stories that would be the most interesting & captivating for your readers. Their content should be concrete and important.
Below are three examples of what a good story has been in the past:

1. Spotify is rolling out a new AI-driven feature for personalized playlists. Instead of basing recommendations solely on previously listened-to tracks, users can now simply input prompts like 'relaxing music for allergy season' or 'a playlist that makes me feel like the main character'. Then, tailored music is delivered shortly after.
2. Neuralink reveals footage showcasing the chip's functionality. Utilizing the 'power of the mind,' a wheelchair user can now play online chess solely with their thoughts, highlighting the potential for those with physical disabilities. Elon Musk hints at future uses, suggesting the chips could control limb prosthetics.
3. A new startup named Cognition Labs has introduced Devin, an AI-based Software Engineer. Users provide instructions, and Devin formulates a plan and codes accordingly. Devin provides real-time updates, handles bugs and problems with Python packages, and deploys the application himself. Programmers, do you feel threatened?

And below are three examples of what a poor story has been in the past:

1. Another miniLLM for mobile apps, Danube from startup H2O, boasts 1.8B parameters and competitive results against major players. The startup plans to release additional tools for easier integration into mobile apps, including Danube Chat for conversational applications.
2. Groq acquires Definitive Intelligence to launch GroqCloud - a cloud-based IDE for programmers. The key aspect of this deal is that users will gain access to the Language Processing Unit Inference Engine, proprietary chips from Groq designed to accelerate LLMs.
3. Tencent presents BlockFusion, a diffusion-based model that creates 3D scenes using individual blocks. This enables seamless integration of new blocks to expand the scene.

Given the article summaries provided by the user, which is the single best story?
Let's think step by step. First write the short rationale for your decision.
Then, end your response with: "So, the best article is <best_article_number>."
IMPORTANT: Remember to end your response with: "So, the best article is <best_article_number>." (insert the number of the best article at the end)
'''

# Create the target directory if it does not exist
if not os.path.exists(TARGET_FOLDER):
    os.makedirs(TARGET_FOLDER)

# Create or clear the output file
with open(OUTPUT_FILE_BEST, 'w') as file:
    file.write("")  # Just to clear previous content if exists
with open(OUTPUT_FILE_BEST_OF_BEST, 'w') as file:
    file.write("")
with open(OUTPUT_FILE_BEST_DEPTH_3, 'w') as file:
    file.write("")

def choose_best(file_list, output_file, batch_size):
    # Process files in batches of N
    for i in range(0, len(file_list), batch_size):
        batch_files = file_list[i:i+batch_size]
        summaries = []
        
        # Read content of each file in the batch
        for idx, file_name in enumerate(batch_files):
            file_path = os.path.join(SOURCE_FOLDER, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                formatted_summary = f"<start article {idx}>\n{content}\n<end article {idx}>"
                summaries.append(formatted_summary)

        # Create prompt with formatted summaries
        user_prompt = "\n\n".join(summaries)
        
        # Send the prompt to the API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "system", "content": PROMPT},
                    {"role": "user", "content": user_prompt}],
            max_tokens=MAX_RESPONSE_TOKENS
        )

        # Get the most interesting summary index
        response_text = response.choices[0].message.content.strip()
        print('\n\n\nRESPONSE:')
        print(response_text)

        digits_mentioned = re.findall(r'\d', response_text)
        most_interesting_index = int(''.join(digits_mentioned[-1:]))
        
        # Write the file title of the most interesting summary to the output file
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write(batch_files[most_interesting_index] + "\n")

    print("Processing completed and results saved to", output_file)

# Get list of files and shuffle them
file_list = [f for f in os.listdir(SOURCE_FOLDER) if f.endswith('.txt')]
random.shuffle(file_list)
choose_best(file_list, OUTPUT_FILE_BEST, N_FIRST_ROUND)
if BEST_OF_BEST:
    with open(OUTPUT_FILE_BEST, 'r') as file:
        content = file.read()
        file_list = [f for f in os.listdir(SOURCE_FOLDER) if f in content]

    # Shuffle the list of filenames
    random.shuffle(file_list)
    choose_best(file_list, OUTPUT_FILE_BEST_OF_BEST, N_SECOND_ROUND)

if BEST_DEPTH_3:
    with open(OUTPUT_FILE_BEST_OF_BEST, 'r') as file:
        content = file.read()
        file_list = [f for f in os.listdir(SOURCE_FOLDER) if f in content]

    # Shuffle the list of filenames
    random.shuffle(file_list)
    choose_best(file_list, OUTPUT_FILE_BEST_DEPTH_3, N_THIRD_ROUND)

collate_all_data()