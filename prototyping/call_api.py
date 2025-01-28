import requests
import src.utils.connect_api as conn

print(f"Base URL: {conn.OPENAI_BASE_URL_CLARITY}")


def request_query(messages:dict, model:str="gpt-4o-mini"):
    # Define the request payload
    return {"model": model, "messages": messages}


def generate_query(role:str, message_content:str):
    return {"role": role, "content": message_content}


def api_request(messages:dict, model:str="gpt-4o-mini"):
    # Make the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {conn.OPENAI_API_KEY_CLARITY}"
    }
    request = request_query(messages, model)
    response = requests.post(
        f"{conn.OPENAI_BASE_URL_CLARITY}/chat/completions",
        json=request,
        headers=headers
    )    
    return response

def main():
    role1 = "system"
    content1 = "You are a helpful assistant."
    role2 = "user"
    content2 = "I need help creating a retrieve augmented generation with atomic_agents library. 2 lines"
    messages = [
        generate_query(role1, content1),
        generate_query(role2, content2)
        ]
    response = api_request(messages)

    response_1 = response.json()['choices'][0]['message']['content']

    # print(*lst, sep='\n')

    breakpoint()

main()