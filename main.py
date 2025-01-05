from dotenv import load_dotenv
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import time

load_dotenv()
client = OpenAI()


def scrape_website(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('article', class_='prose min-w-0 flex-[2_2_0%] max-w-4xl dark:prose-invert')
    site_content = s.find_all('p')
    return site_content


def print_model_response(message, response):
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"{message}"},
            {
                "role": "system",
                "content": f"You are a helpful Docker customer support assistant. Answer only to questions related to "
                           f"Docker. When the question is not about Docker kindly inform user that you can't answer "
                           f"it. Base your knowledge only on provided tools. Your tools gave you this docs website "
                           f"content to help you answer user's question: {response}. If previous response was an "
                           f"error, kindly inform user that he should try again later. "
                           f"Focus on giving the user information from the documentation (your tools rely on it). "
                           f"If information from the documentation requires additional explanation, make it clear to "
                           f"the user that this is your opinion and not a description of the documentation."
            }
        ],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")


def look_for_proper_doc_article(user_prompt):
    r = requests.get('https://docs.docker.com/desktop/setup/install/linux/')
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('nav', class_='md:text-sm flex flex-col')
    site_content = s.find_all('a')

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user",
             "content": f"What is the link for an article that can help user in his Docker problem? "
                        f"User's problem: {user_prompt}. Nav content: {site_content}. "
                        f"Give me only the URL link, no other information. "
                        f"Don't hallucinate, give me exact link that is provided in nav content. "},
        ]
    )
    doc_article_url = completion.choices[0].message.content
    print("Found url: ", doc_article_url)
    return doc_article_url


def process_query(message):
    start = time.time()

    doc_url = look_for_proper_doc_article(message)
    article = scrape_website(doc_url)
    print_model_response(message, article)

    end = time.time()
    exec_time = end - start
    return exec_time


# test
sample_prompts = ["How to install Docker on Mac?", "How to use docker-compose?",
                  "What is a container? How to run one?",
                  "How to setup Docker for cloud?", "Is Docker free?"
]

for prompt in sample_prompts:
    print()
    print("Prompt = ", prompt)
    print()
    process_time = process_query(prompt)
    print()
    print("Time needed to process this query is ", process_time, " seconds.")
    print("---------------------------------")

if __name__ == "__main__":
    while True:
        query = input(">>> ")
        if query == "/exit":
            break
        process_query(query)
        print()
