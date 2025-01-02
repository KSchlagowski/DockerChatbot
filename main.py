import logging

from dotenv import load_dotenv
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import json

load_dotenv()
client = OpenAI()

tools = [
  {
      "type": "function",
      "function": {
          "name": "docker_installation",
          "description": "Call this function whenever user asks you about Docker installation. This tool will give you necessary information about this case.",
          "parameters": {
              "type": "object",
              "properties": {
                  "operation_system": {"type": "string"}
              },
              "required": ["operation_system"]
          },
      },
  }
]


def scrape_website(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('article', class_='prose min-w-0 flex-[2_2_0%] max-w-4xl dark:prose-invert')
    site_content = soup.find_all('p')
    return site_content


def get_website_content_based_on_tool_call(tool_call):
    content = "Error - the website wasn't found or the function wasn't properly called."
    if tool_call.function.name == "docker_installation":
        os = json.loads(tool_call.function.arguments)['operation_system']
        os = str(os).lower()
        if os == "mac":
            content = scrape_website('https://docs.docker.com/desktop/setup/install/mac-install/')
        elif os == "windows":
            content = scrape_website('https://docs.docker.com/desktop/setup/install/windows-install/')
        elif os == "linux":
            content = scrape_website('https://docs.docker.com/desktop/setup/install/linux/')
    return content


def process_query(message):
    completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {
              "role": "system",
              "content": "You are a helpful Docker customer support assistant. Use the supplied tools to assist the user on issues related to Docker application."
          },
          {
              "role": "system",
              "content": "Use the 'docker_installation' function when the user asks about installation of Docker."
          },
          {"role": "user", "content": f"{message}"}],
      tools=tools,
    )

    website_content = "Error - no website content"
    try:
        for tool_call in completion.choices[0].message.tool_calls:
            website_content = get_website_content_based_on_tool_call(tool_call)
    except Exception as e:
        logging.error(f"Error occurred while fetching function call: {str(e)}")

    return website_content

def print_model_response(message, response):
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"{message}"},
            {
                "role": "system",
                "content": f"You are a helpful Docker customer support assistant. Answer only to questions related to Docker. When the question is not about Docker kindly inform user that you can't answer it. Base your knowledge only on provided tools. Your tools gave you this docs website content to help you answer user's question: {response}. If previous response was an error, kindly inform user that he should try again later."
            }
            ],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")


if __name__ == "__main__":
    while True:
        message = input(">>> ")
        if message == "/exit":
            break
        response = process_query(message)
        print_model_response(message, response)
        print()
