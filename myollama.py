import requests
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    api_key="sk-QyPN3iYhwmgRAGbi4zH8L4A7nf8h3ehVyYbFhOu2eVgg2CxG",
    base_url="https://api.moonshot.cn/v1",
)

url = f"http://localhost:11434/api/chat"
model = "llama3.2:1b"
headers = {"Content-Type": "application/json"}


def summary(file_path):
    file_object = client.files.create(file=Path(file_path), purpose="file-extract")
    file_content = client.files.content(file_id=file_object.id).text
    print(file_content)
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant and you are better at English conversations. All your responses must be in English.",
        },
        {
            "role": "user",
            "content": file_content + "\n" + "Please summarize the main content of this paper in points",
        },
    ]
    data = {
        "model": model,
        "options": {
            "temperature": 0.2
        },
        "stream": False,
        "messages": messages

    }
    response = requests.post(url, json=data, headers=headers, timeout=60)
    res = response.json()
    return res["message"]["content"]


def translate(str):
    messages = [
        {"role": "system",
         "content": "你是一个人工智能助手，你更擅长中文和英文的对话。现在我会给你一些英文句子或词语，请将其翻译为中文"},
        {"role": "user", "content": str}
    ]

    data = {
        "model": model,
        "options": {
            "temperature": 0.2
        },
        "stream": False,
        "messages": messages

    }
    response = requests.post(url, json=data, headers=headers, timeout=60)
    res = response.json()
    return res["message"]["content"]


def qa_make_system_messages(file_path):
    file_object = client.files.create(file=Path(file_path), purpose="file-extract")
    file_content = client.files.content(file_id=file_object.id).text

    system_messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that is good at question-answering and English conversation.Please answer the corresponding questions based on the following documents, and all answers must be in English"
        },
        {
            "role": "system",
            "content": "The content of the paper is as follows" + "\n" + file_content
        },
        {
            "role": "user",
            "content": "I will ask some questions"
        },
    ]
    return system_messages


qa_messages = []


def make_qa_messages(input, n, file_path):
    global qa_messages
    qa_messages.append({
        "role": "user",
        "content": input,
    })

    new_messages = []
    new_messages.extend(qa_make_system_messages(file_path))

    if len(qa_messages) > n:
        qa_messages = qa_messages[-n:]

    new_messages.extend(qa_messages)
    return new_messages


def chat_qa(file_path, input):
    data = {
        "model": model,
        "options": {
            "temperature": 0.2
        },
        "stream": False,
        "messages": make_qa_messages(input, 20, file_path)
    }
    response = requests.post(url, json=data, headers=headers, timeout=60)
    res = response.json()
    assistant_message = res["message"]

    qa_messages.append(assistant_message)
    return assistant_message["content"]

# if __name__ == "__main__":
#     # test_file = "output\\A new Capacity-Achieving Private Information Retrieval Scheme with  (Almost) Optimal File Length for Coded Servers.pdf"
#     inn = """
#         The tool can process and understand texts in multiple languages, collect and analyze information from multiple language resources around the world,
#         improve the breadth and depth of information collection, and accurately capture the nuances of different languages.
#     """

# print(summary(test_file))
# print(translate(inn))
# print(chat_qa(test_file, "这篇论文讲了什么"))
# print(chat_qa(test_file, input()))

# chat_qa(test_file, "这篇论文有几个主要部分")
# chat_qa(test_file, "详细讲解一下第二部分")

# print(chat_qa(test_file, "你好，我今年 27 岁。"))
# print(chat_qa(test_file, "你知道我今年几岁吗？"))
