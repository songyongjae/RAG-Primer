import openai

SYSTEM_MESSAGE = {"role": "system", "content": "You are an expert Financial assistant."}

def generate_response(prompt):
    """
    Uses OpenAI API to generate a response for the given prompt.

    :param prompt: Prompt string for the OpenAI API.
    :return: Generated response as a string.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[SYSTEM_MESSAGE, {"role": "user", "content": prompt}],
    )
    return response['choices'][0]['message']['content'].strip()
