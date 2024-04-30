import os
import shutil
from datetime import datetime

NEWS_FOLDER = 'news_content'
SUMMARIES_FOLDER = 'news_summaries'
BEST_FOLDER = 'news_best'
OUTPUT_FOLDER = 'news_result_docs'
OUTPUT_FOLDER_PREVIOUS = os.path.join(OUTPUT_FOLDER, "previous_results")
INPUT_FILE_BEST = os.path.join(BEST_FOLDER, 'best_summaries.txt')
INPUT_FILE_BEST_OF_BEST = os.path.join(BEST_FOLDER, 'best_of_best_summaries.txt')
INPUT_FILE_BEST_DEPTH_3 = os.path.join(BEST_FOLDER, 'best_depth_3_summaries.txt')
OUTPUT_FILE_BEST = os.path.join(OUTPUT_FOLDER, "list_best.txt")
OUTPUT_FILE_BEST_OF_BEST = os.path.join(OUTPUT_FOLDER, "list_best_of_best.txt")
OUTPUT_FILE_BEST_DEPTH_3 = os.path.join(OUTPUT_FOLDER, "list_best_depth_3.txt")

def preserve_previous_results(previous_results_folder, current_folder):
    # Ensure the target directory exists
    if not os.path.exists(previous_results_folder):
        os.makedirs(previous_results_folder)

    # Get the current timestamp
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    # List all files in the source directory
    for filename in os.listdir(current_folder):
        if filename.endswith('.txt'):
            # Generate the new filename with timestamp
            new_filename = f"{filename.split('.txt')[0]}_{current_time}.txt"
            
            # Full path for source and destination
            src_path = os.path.join(current_folder, filename)
            dest_path = os.path.join(previous_results_folder, new_filename)
            
            # Move the file from source to destination
            shutil.move(src_path, dest_path)
            print(f"Moved {filename} to {new_filename}")

def collate_data(input_file, output_file):
    if os.path.exists(input_file):
        with open(input_file, 'r') as file:
            file_list = [line.strip() for line in file]

        # Create or clear the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("")  # Just to clear previous content if exists

        for filename in file_list:
            filename_news = os.path.join(NEWS_FOLDER, filename)
            filename_summary = os.path.join(SUMMARIES_FOLDER, filename)

            with open(filename_news, 'r', encoding='utf-8') as file:
                article_link = file.readline().strip()
            with open(filename_summary, 'r', encoding='utf-8') as file:
                summary_contents = file.read()

            with open(output_file, 'a', encoding='utf-8') as file:
                file.write(article_link + "\n" + summary_contents + "\n\n\n") 

def collate_all_data():
    preserve_previous_results(OUTPUT_FOLDER_PREVIOUS, OUTPUT_FOLDER)
    collate_data(INPUT_FILE_BEST, OUTPUT_FILE_BEST)
    collate_data(INPUT_FILE_BEST_OF_BEST, OUTPUT_FILE_BEST_OF_BEST)
    collate_data(INPUT_FILE_BEST_DEPTH_3, OUTPUT_FILE_BEST_DEPTH_3)