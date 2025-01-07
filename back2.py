from flask import Flask, request, jsonify
from flask_cors import CORS

import llm
from llm import RAGEngine
import sqlite3
import json
import base64
import pandas as pd
import myollama

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 秘钥用于签名 JWT token
SECRET_KEY = 'your_secret_key'

# 全局变量用于存储 Excel 数据
file_path = "similarity.xlsx"
df = pd.read_excel(file_path, header=None)

num = 50


# 连接到 SQLite 数据库
def get_db_connection():
    conn = sqlite3.connect('database.db')  # 数据库文件路径，确保在正确的位置
    conn.row_factory = sqlite3.Row  # 允许以字典格式返回数据
    return conn


# 登录接口
@app.route('/api/login', methods=['POST'])
def login():
    # 从请求中获取 JSON 数据
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(username, password)

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "SELECT * FROM Users WHERE username = ? AND password = ?"
    cursor.execute(sql, (username, password))  # 使用参数化查询，防止SQL注入
    result = cursor.fetchone()  # 获取查询结果

    if result:
        print("用户名和密码匹配，用户信息：", dict(result))
        response = {
            "message": "Success",
            "data": {
                "user_id": result['id']
            }
        }
        conn.close()
        return jsonify(response), 200

    print("用户名或密码不正确，或网络错误")
    response = {
        "message": "failed",
        "data": {
            "user_id": 11111111
        }
    }
    conn.close()
    return jsonify(response), 400


# 注册接口
@app.route('/api/register', methods=['POST'])
def register():
    # 从请求中获取 JSON 数据
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(username, password)

    conn = get_db_connection()
    cursor = conn.cursor()

    # 检查用户名是否已存在
    sql = "SELECT * FROM Users WHERE username = ?"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    if result:
        print("用户名重复：", dict(result))
        response = {
            "message": "Repeat Username",
            "data": {
                "user_id": -1
            }
        }
        conn.close()
        return jsonify(response), 200

    initial_access = [0] * num  # 602个零，表示用户还未访问任何论文

    # 插入新用户，初始化 access 列为包含602个零的数组
    cursor.execute("INSERT INTO Users (username, password, access) VALUES (?, ?, ?)",
                   (username, password, json.dumps(initial_access)))

    # 插入新用户
    # sql = "INSERT INTO Users (username, password) VALUES (?, ?)"
    # cursor.execute(sql, (username, password))
    conn.commit()

    # 获取新插入的用户数据
    cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    print(result)

    if result:
        print("注册成功，用户信息：", dict(result))
        response = {
            "message": "Success",
            "data": {
                "user_id": result['id']
            }
        }
        conn.close()
        return jsonify(response), 200

    response = {
        "message": "failed",
        "data": {
            "user_id": 11111111
        }
    }
    conn.close()
    return jsonify(response), 200


# 获取所有论文接口
@app.route('/api/paper/getpapers', methods=['POST'])
def getpapers():
    # 从请求中获取 JSON 数据
    data = request.get_json()
    user_id = data.get('user_id')  # 获取 user_id
    print(user_id)
    response = {
        "message": "Success",
        "papers": []  # 这里将存放所有的论文数据
    }
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "SELECT access FROM Users WHERE id = ?"
    cursor.execute(sql, (user_id,))
    user = cursor.fetchone()
    access = json.loads(user['access'])

    score = {str(i): 0 for i in range(1, num + 1)}

    for i in range(1, num + 1):
        for j in range(1, num + 1):
            score[str(i)] += access[j - 1] * df.iloc[i, j]

    score = dict(sorted(score.items(), key=lambda item: item[1]))

    number = 0
    for key in score:
        number = number + 1
        paper_id = int(key)
        sql = "SELECT title, author, pub_date, summary, link FROM Papers WHERE paper_id = ?"
        cursor.execute(sql, (paper_id,))
        paper = cursor.fetchone()
        paper_authors = json.loads(paper['author'])  # 从 JSON 字符串转为列表

        # 构建单篇论文的 JSON 格式
        paper_info = {
            "paper_id": paper_id,
            "title": paper['title'],
            "author": paper_authors,
            "pub_date": paper['pub_date'],
            "summary": paper['summary'],
            "link": paper['link']
        }

        # 将每篇论文添加到响应的 papers 列表中
        response['papers'].append(paper_info)
        if number == 10:
            break

    conn.close()
    return jsonify(response), 200


# 获取单篇论文接口
@app.route('/api/paper/get/<int:paper_id>', methods=['GET'])
def get_paper(paper_id):
    # 获取从前端传递过来的 user_id
    user_id = request.args.get('user_id')  # 通过查询参数获取 user_id

    # 打印 user_id（用于调试）
    print(f"Received user_id: {user_id}")

    # 获取数据库连接
    conn = get_db_connection()
    cursor = conn.cursor()

    # 查询用户的 access 列
    cursor.execute("SELECT access FROM Users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    print(user['access'])
    if user:
        # 获取当前用户的 access 数组
        access = json.loads(user['access'])

        # 更新访问次数
        if paper_id <= len(access):
            access[paper_id - 1] += 1  # 将 paper_id 对应的访问次数加 1

            # 将更新后的 access 列写回数据库
            cursor.execute("UPDATE Users SET access = ? WHERE id = ?", (json.dumps(access), user_id))
            conn.commit()

            # 查询论文
            sql = "SELECT * FROM Papers WHERE paper_id = ?"
            cursor.execute(sql, (paper_id,))
            paper = cursor.fetchone()

            if paper:
                # 解析论文的作者信息（假设它是 JSON 格式的）
                paper_authors = json.loads(paper['author'])  # 从 JSON 字符串转为列表

                # 构建响应
                response = {
                    "message": "Success",
                    "paper": {
                        "paper_id": paper['paper_id'],
                        "data": base64.b64encode(paper['data']).decode('utf-8'),  # 论文的二进制字节流
                        "title": paper['title'],
                        "author": paper_authors,
                        "pub_date": paper['pub_date'],
                        "summary": paper['summary'],
                        "link": paper['link']
                    }
                }
                conn.close()
                myollama.qa_messages = []
                return jsonify(response), 200
            else:
                conn.close()
                return jsonify({"message": "未找到该论文"}), 404
        else:
            conn.close()
            return jsonify({"message": "Invalid paper_id"}), 400
    else:
        conn.close()
        return jsonify({"message": "未找到该用户"}), 404


@app.route('/api/paper/search', methods=['POST'])
def search_paper():
    data = request.get_json()
    query_text = data.get('query')

    # 初始化RAGEngine并进行查询
    try:
        idlist = []
        answer = llm.query_from_pdf(query_text, top_k=6)
        top_k_texts = [item['text'] for item in answer['top_k_list']]
        with open("papers_summary.txt", "r", encoding="utf-8") as file:
            papers_dict = json.load(file)
        for top_k_text in top_k_texts:
            print(top_k_text)
            # 遍历字典中的每个项
            for paper_id, summary in papers_dict.items():
                if top_k_text in summary:  # 如果摘要中包含 top_k_text
                    idlist.append(paper_id)
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT title, author, pub_date, summary, link FROM Papers WHERE paper_id = ?"
        response = {
            "message": "Success",
            "papers": []  # 这里将存放所有的论文数据
        }
        for id in idlist:
            cursor.execute(sql, (id,))
            paper = cursor.fetchone()
            paper_authors = json.loads(paper['author'])  # 从 JSON 字符串转为列表

            # 构建单篇论文的 JSON 格式
            paper_info = {
                "paper_id": id,
                "title": paper['title'],
                "author": paper_authors,
                "pub_date": paper['pub_date'],
                "summary": paper['summary'],
                "link": paper['link']
            }

            # 将每篇论文添加到响应的 papers 列表中
            response['papers'].append(paper_info)
        print(response)
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"message": f"查询过程中出错: {str(e)}"}), 500


@app.route('/api/paper/query', methods=['POST'])
def query_paper():
    # 从请求中获取数据
    data = request.get_json()
    paper_id = data.get('paper_id')
    query_text = data.get('query_text')

    print(f"Received query for paper ID {paper_id} with query text: {query_text}")

    # 从数据库中获取论文路径
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "SELECT title FROM Papers WHERE paper_id = ?"
    cursor.execute(sql, (paper_id,))
    paper = cursor.fetchone()
    title = paper['title']

    # 假设PDF文件保存在某个目录下
    file_path = f'output/{title}.pdf'

    # 调用 chat_qa 函数进行查询
    try:
        answer = myollama.chat_qa(file_path, query_text)
        # 获取类似于 top_k 的答案，假设你已经实现了这个逻辑
        # top_k_list = get_top_k_answers(query_text, file_path)

        return jsonify({
            "answer": answer
            # "top_k_list": top_k_list
        })
    except Exception as e:
        print(f"Error during QA processing: {e}")
        return jsonify({"error": "Failed to get answer"}), 500


@app.route('/api/paper/summarize', methods=['POST'])
def summarize_paper():
    data = request.get_json()
    paper_id = data.get('paper_id')

    print(paper_id)
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "SELECT title FROM Papers WHERE paper_id = ?"
    cursor.execute(sql, (paper_id,))
    paper = cursor.fetchone()
    title = paper['title']

    summary = myollama.summary('output\\' + title + '.pdf')
    return jsonify({"summary": summary})


@app.route('/api/paper/translate', methods=['POST'])
def translate_route():
    # 获取前端传递的待翻译文本
    data = request.get_json()
    trans_text = data.get('trans_text')

    print(trans_text)
    if not trans_text:
        return jsonify({'error': '没有提供翻译文本'}), 400

    # 调用翻译函数
    translated_text = myollama.translate(trans_text)

    if translated_text:
        return jsonify({'translated_text': translated_text}), 200
    else:
        return jsonify({'error': '翻译失败'}), 500


if __name__ == '__main__':
    app.run(debug=False)
