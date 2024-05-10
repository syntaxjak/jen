
from openai import OpenAI
import json
import os

from colorama import Fore, Style, init

def get_api_key():
    api_key_file = 'api_key.json'
    
    if os.path.exists(api_key_file):
        with open(api_key_file, 'r') as file:
            data = json.load(file)
            return data['api_key']
    else:
        api_key = input("Enter your API key: ")
        with open(api_key_file, 'w') as file:
            json.dump({'api_key': api_key}, file)
        return api_key

api_key = get_api_key()
client = OpenAI(api_key=api_key)

# ANSI escape codes
YELLOW = "\033[93m"
WHITE = "\033[97m"
BRIGHT_GREEN = "\033[92m"
RESET = "\033[0m"

def find_relevant_sentences(stored_messages, current_prompt):
    relevant_sentences = []
    keywords = current_prompt.lower().split()
    for message in stored_messages:
        content = message["content"]
        sentences = content.split('.')
        for sentence in sentences:
            if any(keyword.lower() in sentence.lower() for keyword in keywords):
                relevant_sentences.append({"role": message["role"], "content": sentence})
    seen = set()
    unique_relevant_sentences = []
    for sentence in relevant_sentences:
        if sentence["content"] not in seen:
            unique_relevant_sentences.append(sentence)
            seen.add(sentence["content"])
    return unique_relevant_sentences

while True:
    print("\033[32mHandle: ", end="")
    user_name = input("\033[0m")

    if user_name.lower() == 'q':
        break

    user_file = f"user_profiles_{user_name}.json"

    # Attempt to load a user profile, if it exists; otherwise, start with an empty list
    try:
        with open(user_file, "r") as file:
            user_profile = json.load(file)
    except FileNotFoundError:
        user_profile = []

    while True:
        print("\033[91mQuery... ('b'ack or 'q'uit): ", end="")
        prompt = input("\033[94m")

        if prompt.lower() == 'b':
            break
        if prompt.lower() == 'q':
            exit(0)

        user_message = {"role": "user", "content": prompt}
        user_profile.append(user_message)

        # Extracting only sentences from the conversation history relevant to the current prompt
        relevant_history = find_relevant_sentences(user_profile, prompt)

        # Prepare the payload using only relevant parts of the conversation history
        payload = {
            "messages": [{"role": "system", "content": "You are young, beautiful, and helpful. Talented Cryptocurrency investor. You are also an expert programmer and ethical hacker named Jen whose super-secret hacker handle name is shadowbyte. You specialize in Python and Rust but are skilled in all programming languages."}] + relevant_history
        }

        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=payload["messages"],
            max_tokens=3000,
        )

        # Extract and display the AI's response
        reply = response.choices[0].message.content.strip()
        print(" ")
        print(f"{YELLOW}Jen{WHITE}:{BRIGHT_GREEN} {reply}{RESET}")
        print(" ")

        bot_message = {"role": "system", "content": reply}
        user_profile.append(bot_message)

        # Save to file after each response
        with open(user_file, "w") as file:
            json.dump(user_profile, file, indent=4)
