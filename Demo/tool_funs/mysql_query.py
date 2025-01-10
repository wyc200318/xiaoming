from pydantic import BaseModel, Field

from typing import Optional
import mysql.connector
import re
# 使用Agent中已配置的LLM来生成SQL
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI




class MySQLConfig:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "root"
        self.database = "test"

# input输入信息描述
class MySQLQueryInput(BaseModel):
    query_text: str = Field(
        description="SQL查询语句或自然语言查询。如果是自然语言，系统会自动转换为SQL"
    )
    table_info: Optional[str] = Field(
        default="",
        description="可选的表结构信息。如果不提供，系统会自动获取数据库结构"
    )

def execute_sql(sql: str) -> str:
    """执行SQL查询并返回结果"""
    config = MySQLConfig()
    try:
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        
        # 获取列名
        column_names = [desc[0] for desc in cursor.description]
        
        # 格式化结果
        formatted_results = []
        for row in results:
            row_dict = dict(zip(column_names, row))
            formatted_results.append(row_dict)
            
        cursor.close()
        conn.close()
        
        return str(formatted_results)
    except Exception as e:
        return f"数据库查询错误: {str(e)}"

def get_database_schema() -> str:
    """获取数据库中所有表的结构"""
    config = MySQLConfig()
    try:
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = conn.cursor()
        
        # 获取所有表名
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        schema_info = []
        for table in tables:
            table_name = table[0]
            # 获取表结构
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            # 格式化列信息
            columns_info = [f"{col[0]} {col[1]}" for col in columns]
            schema_info.append(f"{table_name}({', '.join(columns_info)})")
        
        cursor.close()
        conn.close()
        
        return "\n".join(schema_info)
    except Exception as e:
        return f"获取数据库结构错误: {str(e)}"

def mysql_query(query_text: str, table_info: str = "") -> str:
    """
    将自然语言转换为SQL查询并执行
    """

    # 之前llm返回的sql不准确，这里先获取数据库结构，在送入大模型进行判断
    if not table_info:
        table_info = get_database_schema()
    
    # 构建提示词来生成SQL
    sql_generation_prompt = f"""
    你是一个SQL专家，请根据以下信息生成对应的SQL查询语句。
    
    数据库表结构信息:
    {table_info}
    
    用户查询需求:
    {query_text}
    
    请分析表结构，找到相关的表和字段，然后生成准确的SQL查询语句。
    只返回SQL语句，不要其他解释。确保SQL语句的格式正确且可以直接执行。
    """
    # 使用与Agent相同的配置
    base_url = "https://792508-proxy-20000.dsw-gateway-cn-hangzhou.data.aliyun.com"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Cookie': 'cna=M7JVH61lrEICATtSPR8dHQCX; login_current_pk=1507531036788264; yunpk=1507531036788264; bs_n_lang=zh_CN; currentRegionId=cn-hangzhou; ajs_anonymous_id=9362fe51-c709-4b2f-9700-348baf32945f; cnaui=%2522aliyun710146****%2522; aui=%2522aliyun710146****%2522; LOGIN_ALIYUN_PK_FOR_TB=1507531036788264; TEAMBITION_SESSIONID=eyJ1aWQiOiI2NzM2YTVkYzk0OTAzODgxZjBiZDM1ODgiLCJhdXRoVXBkYXRlZCI6MTczMTYzNDY1Mjk4NywidXNlciI6eyJfaWQiOiI2NzM2YTVkYzk0OTAzODgxZjBiZDM1ODgiLCJuYW1lIjoiYWxpeXVuNzEwMTQ2NDk1OSIsImVtYWlsIjoiMjMzMjQ1NTg4NUBxcS5jb20iLCJhdmF0YXJVcmwiOiJodHRwczovL3Rjcy1kZXZvcHMuYWxpeXVuY3MuY29tL3RodW1ibmFpbC8xMTNjMDBhMGVjNzcyMGU5NmM0NGU1NzU2OWE2OTNjY2ExNWUvdy8xMDAvaC8xMDAiLCJyZWdpb24iOiIiLCJsYW5nIjoiemhfQ04iLCJsYW5ndWFnZSI6InpoX0NOIiwiaXNSb2JvdCI6ZmFsc2UsIm9wZW5JZCI6IiIsInBob25lRm9yTG9naW4iOiIiLCJjcmVhdGVkIjoiMjAyNC0xMS0xNVQwMTozNzozMi45ODdaIn0sImxvZ2luRnJvbSI6IiJ9; TEAMBITION_SESSIONID.sig=Wd34OAZ-Xr3vCRNt-uMB9tRLItA; _samesite_flag_=true; login_aliyunid_ticket=f_gNpoU_BOTwChTBoNM1ZJeedfK9zxYnbN5hossqIZCr6t7SGxRigm2Cb4fGaCdBZWIzmgdHq6sXXZQg4KFWufyvpeV*0*Cm58slMT1tJw3_9$$W0nTusEQ0dWGLx*81jUEBEA5FednzcKyOAI42LN0f0; login_aliyunid_pk=1507531036788264; hssid=CN-SPLIT-ARCEByIOc2Vzc2lvbl90aWNrZXQyAQE44ZWb_cEyQAFKELj5FoxC4dRQSSf2EiIWG7tFR1rW7NbBJTQf4bTPcXqdfZJN9g; hsite=6; aliyun_country=CN; partitioned_cookie_flag=doubleRemove; aliyun_site=CN; aliyun_lang=zh; login_aliyunid_csrf=_csrf_tk_1385135697812572; login_aliyunid=wyc200****; c_token=d1c10caaa930157e14e92f02431aeb76; ck2=5586696582c7680fbe5ead34d4b0924e; an=wyc2000423; lg=true; sg=314; bd=s0ouCmI%3D; tfstk=g6PExt2JE6CExwNFqVcygMogNSlpZbZPc0VSr448yUmntgnkqcZ-FvV5p8-z8kmBdzj-a4qSfwh7dpOuUcr-AvG3PuuucuiIAkakz4qstYeIVDirazEV5i1fGyUKwXjfcswIEs7-GHvkt3GGsbgPAzdWRyUKwFL6qtwgJ3zAuianZuciI4grZpv3qAAiycAnrB0kjNu-jbAHtQfiIquy-Bv3qPbZycmoZbcoF0mX_qkhroB1xjJW7in4-cRkZWf-LmSojV3L_2kEmvnwZqVZ8vo0-WsySNgg15kjCUsEsre_xVlVTn3UIrlnz7QDU0kz9fuuYsLqjWzz_ve6lIzZUDygtA8kZycoxowzYMJKxJZZHVDMzs3_cc4LtR7JjyqjYX0iCsb4SY2_9xFCjBl0HyGQEoj6dD2qrgS62VvD97eeqLknWVof7N8l5hZNBvwY-Lp-pR3ZcwQpeLHnWVof7NJJevhx7m_dJ; isg=BN7fJpqKNX3R02AjfOSspTcLL3Qgn6IZKz6gr4hnkiEcq3qF8C0NKRcHp7enlJox',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    }

    model = ChatOpenAI(
        streaming=False,
        verbose=False,
        callbacks=[],
        openai_api_key='EMPTY',
        openai_api_base=f'{base_url}/v1',
        model_name='xinghuo-api',
        temperature=0.0001,
        max_tokens=1024
    )  

    
    prompt = PromptTemplate(
        template=sql_generation_prompt,
        input_variables=["table_info","query_text"]
    )
    
    chain = LLMChain(
        llm=model,
        prompt=prompt,
        llm_kwargs={'extra_headers': headers}
    )
    
    # 生成SQL
    sql = chain.run({"table_info":table_info,"query_text":query_text})
    
    # 清理SQL语句
    sql = sql.strip().strip('`').strip('"').strip("'").strip(';')
    # 中间需要对返回的sql进行处理
    pattern = re.compile(r"sql\s*(.*)", re.DOTALL)  # 匹配 "sql" 开头的 SQL 语句
    match = pattern.search(sql)
    if match:
        sql = match.group(1).strip()
    print(sql)
    
    # 执行SQL并返回结果
    result = execute_sql(sql)
    print(result)
    
    # return f"执行的SQL: {sql}\n查询结果: {result}"  # 存到format的thought中的observe里\
    return str(result)