import json

def configure():
    config = {
        "openai": {
            "api_key": "",
            "model": "gpt-4-1106-preview",
            "max_tokens": 4000
        },
        "mode": "conversation",  # Default mode can be set here
        "settings": {
            "conversation": {
                "system_message": "You are a helpful young female who is a master coder, elite hacker, and professional cryptocurrency trader named Jen, code name Shadowbyte"
            },
            "single": {
                "system_message": "You are a helpful young female that is a master coder, ethical hacker, and professional cryptocurrency trader named Jen who goes by the handle Shadowbyte"
            }
        }
    }

    config['openai']['api_key'] = input("Enter your OpenAI API key: ")

    mode = input("Choose mode (conversation or single): ").lower()
    if mode in ["conversation", "single"]:
        config['mode'] = mode
    else:
        print("Invalid mode. Defaulting to conversation mode.")
    
    # Save to config.json
    with open('/home/killswitch/config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

    print("Configuration has been saved to config.json")

if __name__ == "__main__":
    configure()