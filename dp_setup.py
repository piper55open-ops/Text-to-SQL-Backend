import psycopg2


def create_tables():
    # 这里的参数要和你 Docker 启动时设定的完全一致
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="enterprise_data",
        user="admin",
        password="secret123"
    )
    cur = conn.cursor()

    # 一次性创建四张核心表
    sql = """
    -- 1. 用户表
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        join_date DATE DEFAULT CURRENT_DATE
    );
    COMMENT ON TABLE users IS '存储客户基本信息';

    -- 2. 产品表
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        product_name VARCHAR(100) NOT NULL,
        price DECIMAL(10, 2) NOT NULL
    );
    COMMENT ON TABLE products IS '存储商品清单及单价';

    -- 3. 订单主表
    CREATE TABLE IF NOT EXISTS orders (
        order_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id),
        status VARCHAR(20) -- 'completed', 'returned'
    );
    COMMENT ON TABLE orders IS '记录订单状态，用于统计退货率';

    -- 4. 订单详情表
    CREATE TABLE IF NOT EXISTS order_items (
        item_id SERIAL PRIMARY KEY,
        order_id INTEGER REFERENCES orders(order_id),
        product_id INTEGER REFERENCES products(product_id),
        quantity INTEGER DEFAULT 1
    );
    """

    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ 业务表结构已强制注入数据库！")


if __name__ == "__main__":
    create_tables()