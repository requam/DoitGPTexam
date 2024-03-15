import openai as ai
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox

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
