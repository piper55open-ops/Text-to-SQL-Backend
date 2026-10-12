from flask import Flask, request, jsonify
# 导入我们之前写好的 AI 核心
from app.agent_core import run_agent_for_web

# 初始化 Flask，并告诉它前端文件在 static 文件夹里
app = Flask(__name__, static_folder='static', static_url_path='/')


@app.route('/')
def home():
    """当用户访问首页时，把前端网页发给他"""
    return app.send_static_file('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():

    if not request.is_json:
        return jsonify({"error": "请求必须是JSON"}), 400

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "JSON必须是对象"}), 400

    user_question = data.get("question")

    if not isinstance(user_question, str):
        return jsonify({"error": "没收到问题呀"}), 400

    user_question = user_question.strip()

    if not user_question:
        return jsonify({"error": "没收到问题呀"}), 400

    print(f"收到前端提问: {user_question}")

    try:
        answer = run_agent_for_web(user_question)
    except Exception:
        return jsonify({"error": "服务器内部错误"}), 500

    return jsonify({"answer": answer})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    print("🚀 Flask 服务器启动！请在浏览器访问 http://127.0.0.1:5000")
    app.run(port=5000, debug=True)