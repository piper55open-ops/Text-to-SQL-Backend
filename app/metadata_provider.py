import psycopg2


def get_database_schema():
    """使用 admin 账号连接数据库，自动抓取表结构和字段信息"""
    try:
        # 这里用 admin 房东账号去查系统表
        conn = psycopg2.connect(
            host="localhost",
            database="enterprise_data",
            user="admin",
            password="secret123"  # 昨天咱们设的密码
        )
        cur = conn.cursor()
        # 查询 public 架构下所有的表和字段
        cur.execute("""
            SELECT table_name, column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'public';
        """)
        rows = cur.fetchall()

        schema_info = "数据库 enterprise_data 包含以下表和字段结构：\n"
        for row in rows:
            schema_info += f"- 表名: {row[0]}, 字段名: {row[1]} (类型: {row[2]})\n"

        cur.close()
        conn.close()
        return schema_info
    except Exception as e:
        print(f"⚠️ 抓取表结构失败: {e}")
        return "获取表结构失败，请检查数据库连接。"