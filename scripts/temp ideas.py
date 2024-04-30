page.goto(link, timeout=MAX_TIMEOUT)
# Zaakceptuj ciasteczka
# cookie_buttons = page.query_selector('button:has-text("Zgadzam się"), button:has-text("Consent"), button:has-text("Allow all"), button:has-text("Accept All Cookies"), button:has-text("Akceptuję"), button:has-text("Consent"), button:has-text("AGREE"), button:has-text("I Accept")')
# if cookie_buttons:
#     cookie_buttons.click()
#     print('Cookie button clicked!')
content_elements = page.query_selector_all('h1:visible, h2:visible, h3:visible, h4:visible, h5:visible, h6:visible, p:visible')
PROMPT = '''
You are a masterful content writer, specializing in selecting the most interesting stories for your company's LinkedIn posts.
You want to select stories that would be the most interesting/captivating for a businessperson, a hobbyist or a layman interested in Artificial Intelligence.
Below are three examples of what a good story has been in the past:

1. Spotify is rolling out a new AI-driven feature for personalized playlists. Instead of basing recommendations solely on previously listened-to tracks, users can now simply input prompts like 'relaxing music for allergy season' or 'a playlist that makes me feel like the main character'. Then, tailored music is delivered shortly after.
2. Neuralink reveals footage showcasing the chip's functionality. Utilizing the 'power of the mind,' a wheelchair user can now play online chess solely with their thoughts, highlighting the potential for those with physical disabilities. Elon Musk hints at future uses, suggesting the chips could control limb prosthetics.
3. A new startup named Cognition Labs has introduced Devin, an AI-based Software Engineer. Users provide instructions, and Devin formulates a plan and codes accordingly. Devin provides real-time updates, handles bugs and problems with Python packages, and deploys the application himself. Programmers, do you feel threatened?

And below are three examples of what a poor story has been in the past:

1. Another miniLLM for mobile apps, Danube from startup H2O, boasts 1.8B parameters and competitive results against major players. The startup plans to release additional tools for easier integration into mobile apps, including Danube Chat for conversational applications.
2. Groq acquires Definitive Intelligence to launch GroqCloud - a cloud-based IDE for programmers. The key aspect of this deal is that users will gain access to the Language Processing Unit Inference Engine, proprietary chips from Groq designed to accelerate LLMs.
3. Tencent presents BlockFusion, a diffusion-based model that creates 3D scenes using individual blocks. This enables seamless integration of new blocks to expand the scene.

Given the article summaries provided by the user, which is the single best story for your target audience? First write the short rationale for your decision and then the best article's number.
**IMPORTANT:**
DO NOT cite the whole story. Remember to end your response with the best article's number.
'''