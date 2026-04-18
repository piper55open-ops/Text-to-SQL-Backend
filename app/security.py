# 李本伟四六开
# 这是一场试炼
import re


def is_sql_safe(sql_query: str) -> bool:
    """
    静态扫描 SQL，拦截 DDL/DML 操作
    """
    # 定义黑名单：禁止删除、修改、截断、插入
    forbidden_words = [
        r"\bDROP\b", r"\bDELETE\b", r"\bUPDATE\b",
        r"\bTRUNCATE\b", r"\bALTER\b", r"\bINSERT\b"
    ]

    query_upper = sql_query.upper()

    for word in forbidden_words:
        if re.search(word, query_upper):
            return False  # 发现危险信号

    return True  # 安全


# 测试一下安检员灵不灵
if __name__ == "__main__":
    test_query = "SELECT * FROM users; DROP TABLE products;"
    if not is_sql_safe(test_query):
        print("🚨 警告：检测到非法操作，已成功拦截！")