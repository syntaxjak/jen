import json
import sys
from openai import OpenAI

def single_question_mode(client, config, question):
    system_message = config['settings']['single']['system_message']
    payload = {
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ]
    }
    response = client.chat.completions.create(
        model=config['openai']['model'],
        messages=payload["messages"],
        max_tokens=config['openai']['max_tokens']
    )
    return response.choices[0].message.content.strip()

def conversation_mode(client, config):
    system_message = config['settings']['conversation']['system_message']
    chat_history = []

    while True:
        print("\n")
        prompt = input("Enter your prompt (or 'quit' to exit): ")
        if prompt.lower() == 'quit':
            break

        user_message = {"role": "user", "content": prompt}
        chat_history.append(user_message)

        payload = {
            "messages": [{"role": "system", "content": system_message}] + chat_history
        }

        response = client.chat.completions.create(
            model=config['openai']['model'],
            messages=payload["messages"],
            max_tokens=config['openai']['max_tokens']
        )

        reply = response.choices[0].message.content.strip()
        print(f"Jen: {reply}")

        bot_message = {"role": "system", "content": reply}
        chat_history.append(bot_message)

        # Optionally, limit the chat history if needed.
        # For example: chat_history = chat_history[-6:]

def main(question, config):
    api_key = config['openai']['api_key']
    client = OpenAI(api_key=api_key)

    mode = config['mode']
    if mode == "conversation":
        conversation_mode(client, config)
    else:
        reply = single_question_mode(client, config, question)
        print(f"Jen: {reply}")

if __name__ == "__main__":
    with open('/home/killswitch/config.json') as config_file:
        config = json.load(config_file)

    if config['mode'] == "single" and len(sys.argv) < 2:
        print("Usage: python script.py \"Your question here\"")
        sys.exit(1)

    question = ' '.join(sys.argv[1:])
    main(question, config)