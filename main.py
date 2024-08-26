from openai import OpenAI
import tkinter as tk
from tkinter import simpledialog, scrolledtext

# OpenAI API anahtarını ayarla
client = OpenAI(api_key="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")

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

# Tkinter arayüzü
root = tk.Tk()
root.title("Chatbot")

# Konuşma geçmişini göstermek için kaydırılabilir bir metin kutusu
chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15)
chat_history.pack(padx=10, pady=10)

# Konuşma başlatma butonu
start_button = tk.Button(root, text="Start Conversation", command=start_conversation)
start_button.pack(pady=5)

# Film önerisi alma butonu
recommend_button = tk.Button(root, text="Get Movie Recommendation", command=get_movie_recommendation)
recommend_button.pack(pady=5)

root.mainloop()