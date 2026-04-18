# 李本伟四六开
# 这是一场试炼
import psycopg2


def setup_readonly_user():
    # 依然先用 admin 账号登录来分配权限
    conn = psycopg2.connect(host="localhost", database="enterprise_data", user="admin", password="secret123")
    cur = conn.cursor()

    # 1. 创建新用户 (如果不存在)
    # 2. 授予连接权限
    # 3. 授予对 public 模式下所有表的查询权限 (SELECT)
    setup_sql = """
    DO $$ 
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = 'agent_runner') THEN
            CREATE ROLE agent_runner WITH LOGIN PASSWORD 'agent_pass_456';
        END IF;
    END $$;

    GRANT CONNECT ON DATABASE enterprise_data TO agent_runner;
    GRANT USAGE ON SCHEMA public TO agent_runner;
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO agent_runner;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO agent_runner;
    """

    cur.execute(setup_sql)
    conn.commit()
    print("✅ 物理防线已就绪：只读账号 agent_runner 创建成功。")
    cur.close()
    conn.close()


if __name__ == "__main__":
    setup_readonly_user()