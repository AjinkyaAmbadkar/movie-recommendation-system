def get_ollama_explanation(prompt, model="llama3.2:3b"):
    import requests
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    if response.status_code == 200:
        return response.json()["response"].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"
    
def generate_prompt(user_top_movie, user_top_genres, rec_title, rec_genres):
    return f"""
You are a movie assistant. The user loved "{user_top_movie}" (Genres: {', '.join(user_top_genres)}).
Now you want to recommend "{rec_title}" (Genres: {', '.join(rec_genres)}).
Explain in 1-2 lines why the user might enjoy this new movie.
"""

