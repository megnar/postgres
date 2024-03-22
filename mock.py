from flask import Flask, request, jsonify
from fastapi import FastAPI
import uvicorn
import psycopg2

app = FastAPI()

mock_data = {
    "users": [
        {"id": 1, "name": "John"},
        {"id": 2, "name": "Alice"}
    ],
    "posts": [
        {"id": 1, "title": "Post 1"},
        {"id": 2, "title": "Post 2"}
    ]
}

response_set = {"select 1" : {"column": 1}}

@app.route('/query', methods=['POST'])
def handle_query():
    query = request.json.get('query')
    result = execute_query(query)
    return jsonify(result)

def execute_query(query):
    # chek if this query is in response_map
    if query == "SELECT * FROM users":
        return 1
    elif query == "SELECT * FROM posts":
        return mock_data['posts']
    else:
        return []

if __name__ == '__main__':

    conn = psycopg2.connect(
    dbname="your_database",
    user="your_username",
    password="your_password",
    host="localhost"
)



    uvicorn.run(app, host="127.0.0.1", port=5000)