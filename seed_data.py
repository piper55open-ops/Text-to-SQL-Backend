import psycopg2

def seed_database():
    print("🧹 正在清空旧数据并重置计数器...")
    try:
        conn = psycopg2.connect(
            host="localhost", database="enterprise_data",
            user="admin", password="secret123"
        )
        cur = conn.cursor()

        # 🚨 核心操作：清空表并重置 ID 计数器为 1 (CASCADE 会自动处理关联表)
        cur.execute("TRUNCATE users, orders RESTART IDENTITY CASCADE;")

        # 1. 注入用户 (这次百分之百确定 Piper 的 ID 是 1)
        print("👤 正在创建测试用户...")
        users_data = [('Piper',), ('Gemini',), ('Auckland_Shop',)]
        for user in users_data:
            cur.execute("INSERT INTO users (username) VALUES (%s);", user)

        # 2. 注入订单
        print("📦 正在创建测试订单...")
        orders_data = [
            (1,  '已完成'),  # 给 Piper
            (1,  '已退货'),   # 给 Piper
            (2,  '待出库'),  # 给 Gemini
            (3,  '已完成')    # 给 Auckland_Shop
        ]
        for order in orders_data:
            cur.execute("INSERT INTO orders (user_id, status) VALUES (%s, %s);", order)

        conn.commit()
        print("✅ 完美！数据已注入，且 ID 全部对齐。")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ 注入失败: {e}")

if __name__ == "__main__":
    seed_database()