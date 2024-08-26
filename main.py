from openai import OpenAI

# OpenAI API anahtarını ayarla
client = OpenAI(api_key="your-api-key")

def generate_recommendations(prompt, genre=None):
    """
    GPT-4 kullanarak film önerileri üretir. Kullanıcının belirttiği türü dikkate alır.
    """
    # Sistem mesajını tür filtreleme ile güncelle
    system_message = "You are a helpful assistant that suggests movies based on a given title or description."
    
    if genre:
        system_message += f" Only suggest movies that belong to the {genre} genre."
    
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )
    
    # Yanıtları toplamak için boş bir string
    response_text = ""
    
    # Her bir parça için döngü
    for chunk in stream:
        # Parçayı yanıt metnine ekle
        response_text += chunk.choices[0].delta.content or ""
    
    return response_text.strip()

# Sonsuz döngü ile kullanıcıdan girdi alma ve öneri sunma
while True:
    movie_input = input("Enter a movie title or description (or type 'exit' to quit): ")
    if movie_input.lower() == 'exit':
        break
    
    genre_input = input("Enter a genre to filter by (optional, press Enter to skip): ")
    genre_input = genre_input if genre_input else None
    
    # GPT-4 ile öneri üret
    recommendation = generate_recommendations(movie_input, genre=genre_input)
    
    # Sonucu kullanıcıya göster
    print("Recommendations:")
    print(recommendation)
