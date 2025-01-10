import mysql.connector
from mysql.connector import Error

def create_test_database():
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
    }
    
    try:
        # 连接MySQL
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # 创建测试数据库（如果不存在）
        cursor.execute("CREATE DATABASE IF NOT EXISTS test")
        cursor.execute("USE test")
        
        # 创建员工表
        create_employees_table = """
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            department VARCHAR(100),
            salary DECIMAL(10, 2),
            hire_date DATE
        )
        """
        cursor.execute(create_employees_table)
        
        # 插入测试数据
        insert_data = """
        INSERT INTO employees (name, department, salary, hire_date) 
        VALUES 
            ('张三', '技术部', 15000.00, '2022-01-15'),
            ('李四', '市场部', 12000.00, '2022-03-20'),
            ('王五', '技术部', 16000.00, '2021-11-05'),
            ('赵六', '人事部', 10000.00, '2023-01-10'),
            ('孙七', '市场部', 13000.00, '2022-07-01')
        """
        
        # 先检查是否已有数据
        cursor.execute("SELECT COUNT(*) FROM employees")
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute(insert_data)
            connection.commit()
            print("测试数据插入成功！")
        else:
            print("表中已有数据，跳过插入操作。")
        
        # 创建订单表
        create_orders_table = """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(100),
            product_name VARCHAR(100),
            amount DECIMAL(10, 2),
            order_date DATE
        )
        """
        cursor.execute(create_orders_table)
        
        # 插入订单测试数据
        insert_orders = """
        INSERT INTO orders (customer_name, product_name, amount, order_date) 
        VALUES 
            ('客户A', '笔记本电脑', 6999.00, '2024-01-15'),
            ('客户B', '手机', 3999.00, '2024-01-16'),
            ('客户C', '显示器', 1599.00, '2024-01-17'),
            ('客户A', '键盘', 299.00, '2024-01-18'),
            ('客户D', '鼠标', 199.00, '2024-01-19')
        """
        
        cursor.execute("SELECT COUNT(*) FROM orders")
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute(insert_orders)
            connection.commit()
            print("订单测试数据插入成功！")
        else:
            print("订单表中已有数据，跳过插入操作。")
            
        # 测试查询
        print("\n测试查询employees表：")
        cursor.execute("SELECT * FROM employees LIMIT 2")
        for row in cursor.fetchall():
            print(row)
            
        print("\n测试查询orders表：")
        cursor.execute("SELECT * FROM orders LIMIT 2")
        for row in cursor.fetchall():
            print(row)
            
    except Error as e:
        print(f"错误: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\n数据库连接已关闭")

if __name__ == "__main__":
    create_test_database() 