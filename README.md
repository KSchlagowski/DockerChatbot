# DockerChatbot

## Overview

DockerChatbot is a Python-based assistant designed to provide answers to Docker-related queries by scraping official Docker documentation. This tool can respond to common questions about Docker like installation, container management, cloud setup, and Docker Compose usage.

## Features
- **SpaCy**: Used for keyword extraction and natural language processing.
- **OpenAI API**: Facilitates response generation by leveraging the GPT-4o-mini model.
- **LangChain**: Enhances document search and contextual response generation, particularly in version 3 with FAISS integration.

## Purpose

The purpose of DockerChatbot is to streamline the process of accessing Docker documentation by providing instant, accurate responses to Docker-related queries. This chatbot uses web scraping, language processing, and OpenAI's API to generate relevant answers based on official Docker documentation.

## Requirements

The following dependencies are required to run DockerChatbot:

```
requests
beautifulsoup4
python-dotenv
spacy
langchain-openai
langchain-community
faiss-cpu
```

Install them by running:
```
pip install -r requirements.txt
```

## How it Works

1. **Web Scraping**: The chatbot uses BeautifulSoup to scrape content from Docker's official documentation.
2. **Keyword Extraction**: Spacy is used to extract key terms from user queries.
3. **Text Embedding and Search**: LangChain and FAISS are used in later versions to enhance document search and response relevance.
4. **API Interaction**: The bot queries OpenAI models (GPT-4o-mini) to process and format answers.

## Code Versions

Three versions of DockerChatbot have been implemented with incremental improvements in functionality and performance.

### Key Differences

| Feature                   | Version 1                             | Version 2                    | Version 3                         |
| ------------------------- | ------------------------------------- | ---------------------------- | --------------------------------- |
| **Web Scraping**          | Basic scraping of documentation pages | Same as Ver1                 | Same as Ver1                      |
| **Keyword Extraction**    | None                                  | Spacy for keyword extraction | Spacy for keyword extraction      |
| **Text Embedding/Search** | None                                  | None                         | FAISS for vector search           |
| **Response Generation**   | Direct from scraped content           | Direct from scraped content  | Embedding-based similarity search |
| **Query Execution Time**  | Moderate (7-17 sec)                   | Moderate (7-24 sec)          | Faster (7-11 sec)                 |
| **Accuracy of Responses** | High (relies on official docs)        | High                         | High (more contextual with FAISS) |

## Example Outputs and Comparison

The table below compares the chatbot's output across versions for common Docker-related queries.

| Query                                | Version 1 Response                          | Version 2 Response                 | Version 3 Response                          | Correctness |
| ------------------------------------ | ------------------------------------------- | ---------------------------------- | ------------------------------------------- | ----------- |
| How to install Docker on Mac?        | Detailed, correct (links to Docker docs)    | Similar to Ver1 but shorter        | Concise, accurate (matches Docker docs)     | ✅           |
| How to use docker-compose?           | Accurate, YAML example provided             | Adds watch mode, detailed commands | Similar to Ver2, focuses on yaml + CLI      | ✅           |
| What is a container? How to run one? | Accurate, step-by-step with examples        | Similar to Ver1                    | Concise but complete                        | ✅           |
| How to setup Docker for cloud?       | Comprehensive (Docker Build Cloud steps)    | Slightly shorter but accurate      | Cloud provider agnostic, mentions AWS/Azure | ✅           |
| Is Docker free?                      | Clear, differentiates free vs paid versions | Less detail on licensing specifics | Concise, emphasizes subscription tiers      | ✅           |

**Note**: All responses are based on official Docker documentation, ensuring high accuracy. The correctness of the responses aligns with Docker's website at the time of development.

## Running the Chatbot

Run the chatbot by executing any of the version scripts (`ver1.py`, `ver2.py`, `ver3.py`):

```
python ver1.py  # or ver2.py / ver3.py
```

The chatbot will process predefined prompts and return Docker-related information with processing times.

## Future Improvements

- **Real-time Web Crawling**: Dynamic scraping to capture the latest Docker documentation updates.
- **Enhanced Response Formatting**: More structured, markdown-formatted answers.
- **Error Handling**: Graceful handling of network errors or missing content.
- **Expanded Query Scope**: Support for broader Docker ecosystem queries beyond basic documentation.

Feel free to contribute by submitting pull requests or raising issues for feature requests!

