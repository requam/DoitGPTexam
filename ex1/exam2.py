import openai as ai
import os

path = os.getcwd()
key_path = path + "/../testkey.txt"

fkey = open(key_path, 'r')
ai.api_key = fkey.readline()
fkey.close()

def send_msg(msg_log):
    response = ai.chat.completions.create(
        model="gpt-3.5-turbo",
        top_p=0.5,
        temperature=0.5,
        messages=msg_log)
    
    return response.choices[0].message.content

def main():
    msg_log = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    log = msg_log.copy()

    while True:
        user_input = input("Q: ")

        if user_input.lower() == "quit":
            print("terminated")
            break

        # msg_log.append({"role": "user", "content": user_input})
        log.append({"role": "user", "content": user_input})
        # res = send_msg(msg_log=msg_log)
        msg = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
        res = send_msg(msg_log=msg)

        # msg_log.append({"role": "assistant", "content": res})
        log.append({"role": "assistant", "content": res})

        print(f'A: {res}')

    print(log)

if __name__ == "__main__":
    main()

'''
    memoriless system...
    should be send all of the messages including api's response
    because it doen't remember that already answered the previous questions
    OMG... taking ma money
'''
