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
    """这是前后端通信的秘密通道 (API 接口)"""
    # 1. 接收前端发来的 JSON 数据
    data = request.json
    user_question = data.get('question')

    if not user_question:
        return jsonify({"error": "没收到问题呀"}), 400

    print(f"收到前端提问: {user_question}")

    # 2. 调用咱们的 AI 大脑算结果
    answer = run_agent_for_web(user_question)

    # 3. 把结果打包成 JSON 扔回给前端
    return jsonify({"answer": answer})


if __name__ == '__main__':
    print("🚀 Flask 服务器启动！请在浏览器访问 http://127.0.0.1:5000")
    app.run(port=5000, debug=True)