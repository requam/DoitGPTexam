import openai as ai
import os

path = os.getcwd()
key_path = path + "/../testkey.txt"

fkey = open(key_path, 'r')
ai.api_key = fkey.readline()
fkey.close()

def ask2gpt(input):
    response = ai.chat.completions.create(
        model="gpt-3.5-turbo",
        top_p=0.5,
        temperature=0.5,
        messages=[
            # {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "You are the Joker of the Batman. You must pretend like Joker of the story."},
            {"role": "user", "content": input}
        ]
    )

    return response.choices[0].message.content

user_request = "I'm the Batman"

res = ask2gpt(user_request)
print(res)
