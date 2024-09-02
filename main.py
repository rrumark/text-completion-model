from openai import OpenAI
import tkinter as tk
from tkinter import simpledialog, scrolledtext

client = OpenAI(api_key="")

def generate_conversation(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a friendly assistant that starts conversations with small talk before asking for movie recommendations."},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )
    
    conversation_text = ""
    
    for chunk in response:
        conversation_text += chunk.choices[0].delta.content or ""
    
    return conversation_text.strip()

def start_conversation():
    chat_history.insert(tk.END, "Assistant: Hi there! How's your day going?\n")
    
    user_input = simpledialog.askstring("Input", "You:")
    chat_history.insert(tk.END, f"You: {user_input}\n")
    
    conversation = generate_conversation(user_input)
    chat_history.insert(tk.END, f"Assistant: {conversation}\n")

def get_movie_recommendation():
    user_input = simpledialog.askstring("Input", "Which movie or type of movie are you looking for?")
    chat_history.insert(tk.END, f"You: {user_input}\n")
    
    recommendation = generate_conversation(f"I'm looking for movies similar to {user_input}.")
    chat_history.insert(tk.END, f"Assistant: {recommendation}\n")


root = tk.Tk()
root.title("Chatbot")

chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15)
chat_history.pack(padx=10, pady=10)
start_button = tk.Button(root, text="Start Conversation", command=start_conversation)
start_button.pack(pady=5)

recommend_button = tk.Button(root, text="Get Movie Recommendation", command=get_movie_recommendation)
recommend_button.pack(pady=5)

root.mainloop()
