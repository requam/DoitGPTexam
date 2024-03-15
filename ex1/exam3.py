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

def main():
    def on_send():
        user_input = input_box.get("1.0", tk.END).strip()
        input_box.delete("1.0", tk.END)

        if user_input.lower() == "quit":
            output_box.insert(tk.END, "terminated\n")
            root.destroy()
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

        # res = send_msg(msg_log=msg_log)
        
        # msg_log.append({"role": "assistant", "content": res})
        
        # output_box.configure(state='normal')
        # output_box.insert(tk.END, f'Q: {user_input}\n', 'user_msg')
        # output_box.insert(tk.END, f'A: {res}\n', 'assistant_msg')
        # output_box.configure(state='disabled')
        # output_box.see(tk.END)

    # Main GUI setup
    root = tk.Tk()
    root.title("ChatBot")

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

    send_button = tk.Button(frame, text="Send", command=on_send, font=font_style)
    send_button.pack(padx=10, pady=10)

    root.bind('<Return>', lambda event: on_send())

    msg_log = [{"role": "system", "content": "You are a helpful assistant."}]

    root.mainloop()

if __name__ == "__main__":
    main()
