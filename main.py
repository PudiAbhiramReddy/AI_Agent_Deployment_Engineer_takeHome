import os
import openai
from dotenv import load_dotenv
load_dotenv()
"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

If I had two more hours, I would implement a user feedback loop. After a story is successfully generated, the system would ask the user "Did you like this story? (yes/no)" and "What would you like to change?". This feedback would then be used as a new input for the revision process, allowing the user to iteratively refine the story to their exact liking, making the experience more interactive and personalized. I would also add more robust error handling for API calls and edge cases in user input.

"""

# --- Prompt Templates ---

STORYTELLER_PROMPT_TEMPLATE = """
You are a world-famous author of bedtime stories for children aged 5 to 10.
Your task is to write a short, simple, and heartwarming story based on the user's request.
The story must have the following characteristics:
- It should be easy to understand for a 5-year-old.
- It must have a positive and happy tone, with no scary or sad elements.
- It should feature a clear, gentle moral or lesson at the end.
- The story should be approximately 200-300 words long.

User's story request: "{user_request}"
"""


JUDGE_PROMPT_TEMPLATE = """
You are a very picky children's book editor. Your job is to find stories that are not just safe, but also magical and engaging. A story that is boring or generic, even if it follows the rules, is an automatic failure.

Evaluate the story based on these criteria. You must respond with only "PASS" or "FAIL".
If you choose "FAIL", you must provide a single, short sentence explaining the reason.

1.  **Appropriateness:** Is the vocabulary, tone, and theme perfectly suitable for a 5-year-old? (No complex words, no scary themes).
2.  **Clarity:** Is there a clear beginning, middle, and end with a simple plot?
3.  **Engagement (The Strict Part):** Is the story creative and interesting? Does it have a unique element or a little spark of magic? A generic story about a friendly animal learning to share is not good enough. It must have a memorable detail to pass.
4.  **Moral:** Is there a positive moral shown through the story's events?

Here is the story you must evaluate:
--- STORY START ---
{story_draft}
--- STORY END ---

Provide your verdict and, if failing, the reason.
"""



REVISION_PROMPT_TEMPLATE = """
You are a children's story author. Your first draft was rejected by a picky editor for not being engaging enough. You must now rewrite it based on their feedback to make it more magical and creative.

The original request was: "{user_request}"

--- STORY DRAFT THAT FAILED ---
{story_draft}
--- END DRAFT ---

The editor's feedback was: "{feedback}"

Please write a new version of the story. Keep the core idea, but add a unique, memorable, or magical detail that directly addresses the editor's concern. For example, instead of a normal squirrel, maybe it's a squirrel whose tail sparkles. Instead of a normal forest, maybe the trees whisper secrets. Ensure the new story is still simple, positive, and appropriate for a 5-year-old.
"""


def call_model(prompt: str, max_tokens=500, temperature=0.7) -> str:
    """
    A wrapper for the OpenAI API call, updated for openai library v1.0.0+.
    """
    try:
        # The new syntax requires creating a client
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if client.api_key is None:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
            
        # The API call itself is also different
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content.strip() # The response object structure is also slightly different
    
    except Exception as e:
        # The error handling should be more specific to provide clearer feedback
        return f"An error occurred: {e}"


def main():
    """
    Main function to run the storyteller-judge system.
    """
    print("Welcome to the Bedtime Story Generator!")
    user_input = input("What kind of story do you want to hear? ")
    
    if not user_input:
        print("Please provide a story idea.")
        return

    print("\nWriting a draft for you... please wait.")

    max_attempts = 5
    current_story_draft = ""
    story_request = user_input
    
    for attempt in range(max_attempts):
        print(f"\n--- Attempt {attempt + 1} of {max_attempts} ---")
        
        # Step 1: Generate Story (or revise it)
        if attempt == 0:
            prompt = STORYTELLER_PROMPT_TEMPLATE.format(user_request=story_request)
        else:
            # On subsequent attempts, we use the revision prompt
            prompt = REVISION_PROMPT_TEMPLATE.format(
                user_request=story_request,
                story_draft=current_story_draft,
                feedback=feedback # from previous failed attempt
            )

        current_story_draft = call_model(prompt, max_tokens=500, temperature=0.7)
        print("Draft generated. Now sending to the editor for review...")
        
        # Step 2: Judge the Story
        judge_prompt = JUDGE_PROMPT_TEMPLATE.format(story_draft=current_story_draft)
        judge_response = call_model(judge_prompt, max_tokens=100, temperature=0.1)
        
        print(f"Editor's response: {judge_response}")

        # Step 3: Check the Verdict
        if judge_response.startswith("PASS"):
            print("\nStory approved! Here is your bedtime story:\n")
            print("-------------------------------------------")
            print(current_story_draft)
            print("-------------------------------------------")
            return # Success, end the program
        else:
            # Extract feedback for the revision loop
            feedback = judge_response.replace("FAIL:", "").strip()
            if attempt < max_attempts - 1:
                print(f"The story did not pass the quality check. Reason: '{feedback}'. Attempting to revise...")
            else:
                print("\nSorry, I couldn't create a story that met the quality standards after several attempts.")
                print("Here is the last draft I worked on, in case you are curious:")
                print("-------------------------------------------")
                print(current_story_draft)
                print("-------------------------------------------")

if __name__ == "__main__":
    main()