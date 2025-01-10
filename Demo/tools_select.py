from langchain.tools import Tool

from tool_funs import *

tools = [
    # Tool.from_function(
    #     func=weathercheck,
    #     name="weather_check",
    #     description="获取对应城市的天气",
    #     args_schema=WeatherInput,
    #     # args_schema=None
    # ),
    # Tool.from_function(
    #     func=product_order_number,
    #     name="product_order_number",
    #     description="获取对应商品的售出订单数目",
    #     args_schema=ProductOrderNumberInput,
    #     # args_schema=None
    # ),
    # Tool.from_function(
    #     func=product_price,
    #     name="product_price",
    #     description="查询商品对应的单价",
    #     args_schema=ProductPriceInput,
    #     # args_schema=None
    # ),
    Tool.from_function(
        func=mysql_query,
        name="mysql_query",
        description="""用于执行MySQL数据库查询的工具,
        只要使用MySQL数据库相关的内容，必须优先使用该方法。
        """,
        args_schema=MySQLQueryInput
    )
]

tool_names = [tool.name for tool in tools]

# 工具的描述信息特别重要，可以详细介绍每个表的列名，更容易正确检索
# 数据库包含以下表：
# 1.employ1 - 员工信息表
# 2.orders - 订单信息表

