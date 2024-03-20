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
        temperature=0.1,
        messages=msg_log)
    
    return response.choices[0].message.content

def main():
    def quit_gpt():
        output_box.insert(tk.END, "terminated\n")
        root.destroy()

    def on_send():
        user_input = input_box.get("1.0", tk.END).strip()
        input_box.delete("1.0", tk.END)

        if user_input.lower() == "quit":
            quit_gpt()
            return

        msg_log.append({"role": "user", "content": user_input})
        
        # Show popup message while waiting for response
        popup = tk.Toplevel(root)
        popup.title("Waiting for Response")
        popup.geometry("200x100")
        popup_label = tk.Label(popup, text="Waiting for response...", pady=20)
        popup_label.pack()

        popup.transient(root)
        popup.attributes('-topmost', True)
        popup.update()

        try:
            res = send_msg(msg_log=msg_log)
            msg_log.append({"role": "assistant", "content": res})

            output_box.configure(state='normal')
            output_box.insert(tk.END, f'Q: {user_input}\n', 'user_msg')
            output_box.insert(tk.END, f'A: {res}\n', 'assistant_msg')
            output_box.configure(state='disabled')
            output_box.see(tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            popup.destroy()

    # Main GUI setup
    root = tk.Tk()
    root.title("GPT DJ")
    root.geometry(f"+{10}+{10}")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Set font
    font_style = ("Helvetica", 12)

    output_box = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=font_style, spacing1=5, spacing2=2, spacing3=5)
    output_box.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
    output_box.tag_config('assistant_msg', background='lightblue')
    output_box.tag_config('user_msg', background='lightgreen')
    output_box.configure(state='disabled')

    input_box = tk.Text(frame, height=2, font=font_style)
    input_box.pack(padx=10, pady=10, fill=tk.X)
    input_box.configure(bg="lightyellow")

    quit_button = tk.Button(frame, text="Quit", command=quit_gpt, font=font_style)
    quit_button.pack(side=tk.RIGHT, padx=10, pady=10)

    send_button = tk.Button(frame, text="Send", command=on_send, font=font_style)
    send_button.pack(side=tk.RIGHT, padx=10, pady=10)

    root.bind('<Return>', lambda event: on_send())

    # prompt engineering
    msg_log = [{"role": "system", 
                "content": "You are a DJ assistant who creates playlists.\
                    Your user will be Korean, so communicate in Korean, but you must not translate artists' names and song titles into Korean.\
                    When you show a playlist, it must contains the title, artist, and release year of each song in a list format.\
                    You must show a playlist at least 10 songs.\
                    You must ask the user if they want to save the playlist after your answer.\
                    Your must write the message that they want to save like this: '(예/아니오)'.\
                    If they want to save the playlist into CSV, show the playlist with a header in CSV format, separated by ';' and the release year format should be 'YYYY'.\
                    The CSV format must start with a new line.\
                    The header of the CSV file must be in English and it should be formatted as follows: 'Title;Artist;Release'."}]

    root.mainloop()

if __name__ == "__main__":
    main()
