from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key='')

def translate_text(text, target_language):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that translates English to {target_language}."},
                {"role": "user", "content": f"Translate the following English text to {target_language}: '{text}'"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage
english_text = "Hello, how are you?"
target_language = "French"

result = translate_text(english_text, target_language)
print(f"English: {english_text}")
print(f"French: {result}")
