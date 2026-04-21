import os
import re
import psycopg2
from dotenv import load_dotenv
from google import genai

# 导入安全和元数据模块
from app.security import is_sql_safe
from app.metadata_provider import get_database_schema

# 加载配置
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def clean_sql(raw_text: str) -> str:
    cleaned = re.sub(r"```sql", "", raw_text, flags=re.IGNORECASE)
    cleaned = re.sub(r"```", "", cleaned)
    return cleaned.strip()


def run_agent_for_web(user_question: str) -> str:
    """专为 Streamlit 网页端设计的函数，返回 Markdown 格式的字符串"""

    # 1. 获取数据库结构
    schema_info = get_database_schema()

    # 2. 构建 Prompt
    prompt = f"""
    你是一个 PostgreSQL 专家。请根据以下结构生成 SQL：
    {schema_info}
    规则：只输出 SQL，不输出解释，只能 SELECT。
    提问：{user_question}
    """

    try:
        # 3. 召唤 AI
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=prompt
        )
        generated_sql = clean_sql(response.text)

        # 4. 安全检测
        if not is_sql_safe(generated_sql):
            return f"🚨 **安全拦截**：生成的 SQL 包含非法操作！\n\n`{generated_sql}`"

        # 5. 执行查询
        conn = psycopg2.connect(
            host="localhost", database="enterprise_data",
            user="agent_runner", password="agent_pass_456"
        )
        cur = conn.cursor()
        cur.execute(generated_sql)
        results = cur.fetchall()
        cur.close()
        conn.close()

        # 6. 拼装返回给网页的 Markdown 文本
        output = f"### 📝 生成的 SQL\n```sql\n{generated_sql}\n```\n\n"
        output += "### ✅ 查询结果\n"
        if not results:
            output += "查无数据。"
        else:
            for row in results:
                output += f"- {row}\n"
        return output

    except Exception as e:
        return f"❌ **系统错误**: {str(e)}"


# 保留原来的终端测试功能
if __name__ == "__main__":
    print(run_agent_for_web("查一下 Piper 的订单"))