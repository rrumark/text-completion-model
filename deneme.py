from openai import OpenAI
import tkinter as tk
from tkinter import simpledialog, scrolledtext

# OpenAI API anahtarını ayarla
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

def start_conversation(event=None):
    user_input = entry.get()
    chat_history.insert(tk.END, f"You: {user_input}\n")
    
    conversation = generate_conversation(user_input)
    chat_history.insert(tk.END, f"Assistant: {conversation}\n")
    
    # Girdiyi temizle
    entry.delete(0, tk.END)

def get_movie_recommendation(event=None):
    user_input = entry.get()
    chat_history.insert(tk.END, f"You: {user_input}\n")
    
    recommendation = generate_conversation(f"I'm looking for movies similar to {user_input}.")
    chat_history.insert(tk.END, f"Assistant: {recommendation}\n")
    
    # Girdiyi temizle
    entry.delete(0, tk.END)

# Tkinter arayüzü
root = tk.Tk()
root.title("Chatbot")

# Konuşma geçmişini göstermek için kaydırılabilir bir metin kutusu
chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15)
chat_history.pack(padx=10, pady=10)

# Giriş alanı (Entry widget)
entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=10)
entry.bind("<Return>", start_conversation)  # Enter tuşuna basıldığında start_conversation fonksiyonunu çağırır

# Konuşma başlatma butonu
start_button = tk.Button(root, text="Start Conversation", command=start_conversation)
start_button.pack(pady=5)

# Film önerisi alma butonu
recommend_button = tk.Button(root, text="Get Movie Recommendation", command=get_movie_recommendation)
recommend_button.pack(pady=5)

root.mainloop()
