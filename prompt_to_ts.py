from openai import AzureOpenAI
import json


def prompt_to_ts(text: str, schema: str):
    """
    Params:
    text: string, user's document
    schema: string, but of typescript type — type Result = {...}

    Returns:
    schema instance filled with values, in JSON format
    """
    AZURE_OPENAI_API_KEY = "replace it here"
    AZURE_OPENAI_ENDPOINT = "replace it here"
    DEPLOYMENT_NAME = "gpt-4o-mini"
    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version="2024-02-01",
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
    )

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {
                "role": "user",
                "content": f"Based on this text: {text}, return a JSON that describes this text in this TypeScript schema: {schema}. If it cannot arrive at the answer directly, say 'cannot answer'. Just return the JSON, do not include ```json.",
            },
        ],
    )
    answer = response.choices[0].message.content
    try:
        data = json.loads(answer)
        return data
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {answer}"


if __name__ == "__main__":
    global_text = "Bananas are my favorite food."
    global_schema = """type Result = {
    "Does this text mention bananas?": boolean;
    "Sentiment about bananas.": string;
    "Pairs of words": Array<[string, string]>;
    "Number of words": number;
    "Contrapositive": string;
    }"""
    prompt_to_ts(text=global_text, schema=global_schema)
