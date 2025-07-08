from langchain_community.llms import Ollama
from django.core.cache import cache

def generate_email_response_function(prompt, regenerate=False):
    # Use llama3.2 model as the default
    llm = Ollama(model="llama3.2")

    # Check if the response is already cached and regenerate is False
    cache_key = 'email_response_' + prompt
    if not regenerate:
        cached_response = cache.get(cache_key)
        if cached_response:
            return cached_response
        
    # Instructions for the AI model to generate a professional email
    system_instructions = """
        You are an intelligent assistant that helps users generate professional emails.
        When a user provides basic information, you will craft a well-structured and properly formatted email based on the given context.
        Ensure that the email follows standard business communication practices, including a formal or semi-formal greeting depending on the recipient's relationship with the user.
        Briefly state the purpose or context in the introduction, then address the main points clearly and concisely in the body of the email.
        Conclude the email politely, offering next steps or expressing gratitude as needed.
        Use an appropriate sign-off such as "Best regards" or "Sincerely" and, if requested, include the user's name, title, and contact information.
        The overall tone should match the user's preference (formal, neutral, or casual), and the email should be clear, polite, and free of errors.
        Do not include sample subject lines unless specifically requested.
    """

    # Generate text based on the input prompt
    try:
        response = llm(prompt + system_instructions)
        
        # Clean up the response if needed
        generated_text = response.strip()
        
        # Cache the response for a certain amount of time (e.g., 1 hour)
        cache.set(cache_key, generated_text, 3600)
        
        return generated_text
    except Exception as e:
        # Return a fallback message if there's an error
        return "Sorry, I couldn't generate an email response at this time. Please try again later."
    print(generated_text)
    return generated_text
