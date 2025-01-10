# -*- coding: utf-8 -*-
"""
以下代码能够正常import的前提条件是 Langchain-Chatchat 这个文件夹添加到sys.path环境变量中了
"""
import os

import sys
sys.stdout.reconfigure(encoding='utf-8')

os.environ['XDG_CACHE_HOME'] = r"D:\huggingface"
os.environ['CACHE_HOME'] = r'D:\huggingface'
os.environ['MODELSCOPE_CACHE'] = r'D:\huggingface\modelscope\hub'

from langchain.chains import LLMChain
from langchain.agents import LLMSingleActionAgent, AgentExecutor
from langchain_community.chat_models import ChatOpenAI

from custom_template import CustomPromptTemplate, CustomOutputParser
from tools_select import tools, tool_names

# base_url = "http://127.0.0.1:20000"
base_url = "https://792508-proxy-20000.dsw-gateway-cn-hangzhou.data.aliyun.com"  # 去这个网站+/v1/models能访问，找network，model中找cokkies
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    # 'Cookie': 'cna=M7JVH61lrEICATtSPR8dHQCX; login_current_pk=1507531036788264; yunpk=1507531036788264; bs_n_lang=zh_CN; currentRegionId=cn-hangzhou; ajs_anonymous_id=9362fe51-c709-4b2f-9700-348baf32945f; cnaui=%2522aliyun710146****%2522; aui=%2522aliyun710146****%2522; LOGIN_ALIYUN_PK_FOR_TB=1507531036788264; TEAMBITION_SESSIONID=eyJ1aWQiOiI2NzM2YTVkYzk0OTAzODgxZjBiZDM1ODgiLCJhdXRoVXBkYXRlZCI6MTczMTYzNDY1Mjk4NywidXNlciI6eyJfaWQiOiI2NzM2YTVkYzk0OTAzODgxZjBiZDM1ODgiLCJuYW1lIjoiYWxpeXVuNzEwMTQ2NDk1OSIsImVtYWlsIjoiMjMzMjQ1NTg4NUBxcS5jb20iLCJhdmF0YXJVcmwiOiJodHRwczovL3Rjcy1kZXZvcHMuYWxpeXVuY3MuY29tL3RodW1ibmFpbC8xMTNjMDBhMGVjNzcyMGU5NmM0NGU1NzU2OWE2OTNjY2ExNWUvdy8xMDAvaC8xMDAiLCJyZWdpb24iOiIiLCJsYW5nIjoiemhfQ04iLCJsYW5ndWFnZSI6InpoX0NOIiwiaXNSb2JvdCI6ZmFsc2UsIm9wZW5JZCI6IiIsInBob25lRm9yTG9naW4iOiIiLCJjcmVhdGVkIjoiMjAyNC0xMS0xNVQwMTozNzozMi45ODdaIn0sImxvZ2luRnJvbSI6IiJ9; TEAMBITION_SESSIONID.sig=Wd34OAZ-Xr3vCRNt-uMB9tRLItA; _samesite_flag_=true; login_aliyunid_ticket=f_gNpoU_BOTwChTBoNM1ZJeedfK9zxYnbN5hossqIZCr6t7SGxRigm2Cb4fGaCdBZWIzmgdHq6sXXZQg4KFWufyvpeV*0*Cm58slMT1tJw3_9$$W0nTusEQ0dWGLx*81jUEBEA5FednzcKyOAI42LN0f0; login_aliyunid_pk=1507531036788264; hssid=CN-SPLIT-ARCEByIOc2Vzc2lvbl90aWNrZXQyAQE44ZWb_cEyQAFKELj5FoxC4dRQSSf2EiIWG7tFR1rW7NbBJTQf4bTPcXqdfZJN9g; hsite=6; aliyun_country=CN; partitioned_cookie_flag=doubleRemove; aliyun_site=CN; aliyun_lang=zh; login_aliyunid_csrf=_csrf_tk_1385135697812572; login_aliyunid=wyc200****; c_token=d1c10caaa930157e14e92f02431aeb76; ck2=5586696582c7680fbe5ead34d4b0924e; an=wyc2000423; lg=true; sg=314; bd=s0ouCmI%3D; tfstk=gczrxYqpxaQPso4PKj0e7Tk0RPuJr2yFCv4ItXVL9BDor9HHKxwKA04C2kJUa8DWVWXK8X2Ih_3QV3T3YxyKF0guOJl3CJMSF8NHTX2jrDESdYME8WeNGO_157F-J4X1CNZSxN5K53xoxpgDi2GFFWLBN7F-JIdXKGZ0wpPOtRFo-J0mmXGE-3xuKmYm9xYotUcHnslKn2YkrebmmfleZUxuKSfq9xDn-2c-WvD6ufoltRIfEVSW6RkgZx8H7Chrq6FyAeLLubozW7Dqsf4qa0kiDrj4hz2btza-DgKSJSZaLk2Gh3MubfyqfuWwzRy-t-c0F6tKgkP3W4nJ9eeZzJogrmRH750u2ql0S6tthrk7Kzoc1FoIoPiirosAFDgr_J48UB83ISN_ymUFQKDLVf3mTyCMYvoh4N9KihY8JuJHY0cxgA1VgBfXh-SxVlFkvHn8Djk1w_Kpv0cxgA1VgHKK2VhqC_CR.; isg=BM7OXgo6JU1kS5DT7LS89cfbH6SQT5JJu06wf_gXrVGMW221YN3KWWZXl4c3xIph; _streamlit_xsrf=2|fb4a870a|337338a0fb33bfe395ea94f810a30369|1735700692',
    'Cookie': 'cna=M7JVH61lrEICATtSPR8dHQCX; login_current_pk=1507531036788264; yunpk=1507531036788264; bs_n_lang=zh_CN; currentRegionId=cn-hangzhou; ajs_anonymous_id=9362fe51-c709-4b2f-9700-348baf32945f; cnaui=%2522aliyun710146****%2522; aui=%2522aliyun710146****%2522; LOGIN_ALIYUN_PK_FOR_TB=1507531036788264; TEAMBITION_SESSIONID=eyJ1aWQiOiI2NzM2YTVkYzk0OTAzODgxZjBiZDM1ODgiLCJhdXRoVXBkYXRlZCI6MTczMTYzNDY1Mjk4NywidXNlciI6eyJfaWQiOiI2NzM2YTVkYzk0OTAzODgxZjBiZDM1ODgiLCJuYW1lIjoiYWxpeXVuNzEwMTQ2NDk1OSIsImVtYWlsIjoiMjMzMjQ1NTg4NUBxcS5jb20iLCJhdmF0YXJVcmwiOiJodHRwczovL3Rjcy1kZXZvcHMuYWxpeXVuY3MuY29tL3RodW1ibmFpbC8xMTNjMDBhMGVjNzcyMGU5NmM0NGU1NzU2OWE2OTNjY2ExNWUvdy8xMDAvaC8xMDAiLCJyZWdpb24iOiIiLCJsYW5nIjoiemhfQ04iLCJsYW5ndWFnZSI6InpoX0NOIiwiaXNSb2JvdCI6ZmFsc2UsIm9wZW5JZCI6IiIsInBob25lRm9yTG9naW4iOiIiLCJjcmVhdGVkIjoiMjAyNC0xMS0xNVQwMTozNzozMi45ODdaIn0sImxvZ2luRnJvbSI6IiJ9; TEAMBITION_SESSIONID.sig=Wd34OAZ-Xr3vCRNt-uMB9tRLItA; _samesite_flag_=true; login_aliyunid_ticket=f_gNpoU_BOTwChTBoNM1ZJeedfK9zxYnbN5hossqIZCr6t7SGxRigm2Cb4fGaCdBZWIzmgdHq6sXXZQg4KFWufyvpeV*0*Cm58slMT1tJw3_9$$W0nTusEQ0dWGLx*81jUEBEA5FednzcKyOAI42LN0f0; login_aliyunid_pk=1507531036788264; hssid=CN-SPLIT-ARCEByIOc2Vzc2lvbl90aWNrZXQyAQE44ZWb_cEyQAFKELj5FoxC4dRQSSf2EiIWG7tFR1rW7NbBJTQf4bTPcXqdfZJN9g; hsite=6; aliyun_country=CN; partitioned_cookie_flag=doubleRemove; aliyun_site=CN; aliyun_lang=zh; login_aliyunid_csrf=_csrf_tk_1385135697812572; login_aliyunid=wyc200****; c_token=d1c10caaa930157e14e92f02431aeb76; ck2=5586696582c7680fbe5ead34d4b0924e; an=wyc2000423; lg=true; sg=314; bd=s0ouCmI%3D; tfstk=g6PExt2JE6CExwNFqVcygMogNSlpZbZPc0VSr448yUmntgnkqcZ-FvV5p8-z8kmBdzj-a4qSfwh7dpOuUcr-AvG3PuuucuiIAkakz4qstYeIVDirazEV5i1fGyUKwXjfcswIEs7-GHvkt3GGsbgPAzdWRyUKwFL6qtwgJ3zAuianZuciI4grZpv3qAAiycAnrB0kjNu-jbAHtQfiIquy-Bv3qPbZycmoZbcoF0mX_qkhroB1xjJW7in4-cRkZWf-LmSojV3L_2kEmvnwZqVZ8vo0-WsySNgg15kjCUsEsre_xVlVTn3UIrlnz7QDU0kz9fuuYsLqjWzz_ve6lIzZUDygtA8kZycoxowzYMJKxJZZHVDMzs3_cc4LtR7JjyqjYX0iCsb4SY2_9xFCjBl0HyGQEoj6dD2qrgS62VvD97eeqLknWVof7N8l5hZNBvwY-Lp-pR3ZcwQpeLHnWVof7NJJevhx7m_dJ; isg=BN7fJpqKNX3R02AjfOSspTcLL3Qgn6IZKz6gr4hnkiEcq3qF8C0NKRcHp7enlJox',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
}
PROMPT_TEMPLATES = {
    "agent_chat": {
        "default":
            'Answer the following questions as best you can. If it is in order, you can use some tools appropriately. '
            'You have access to the following tools:\n\n'
            '{tools}\n\n'
            'Use the following format:\n'
            'Question: the input question you must answer1\n'
            'Thought: you should always think about what to do and what tools to use.\n'
            'Action: the action to take, should be one of [{tool_names}]\n'
            'Action Input: the input to the action\n'
            'Observation: the result of the action\n'
            '... (this Thought/Action/Action Input/Observation can be repeated zero or more times)\n'
            'Thought: I now know the final answer\n'
            'Final Answer: the final answer to the original input question\n'
            'Begin!\n\n'
            'Question: {input}\n\n'
            'Thought: {agent_scratchpad}\n',

        "ChatGLM3":
            'You can answer using the tools, or answer directly using your knowledge without using the tools. '
            'Respond to the human as helpfully and accurately as possible.\n'
            'You have access to the following tools:\n'
            '{tools}\n'
            'Use a json blob to specify a tool by providing an action key (tool name) '
            'and an action_input key (tool input).\n'
            'Valid "action" values: "Final Answer" or  [{tool_names}]'
            'Provide only ONE action per $JSON_BLOB, as shown:\n\n'
            '```\n'
            '{{{{\n'
            '  "action": $TOOL_NAME,\n'
            '  "action_input": $INPUT\n'
            '}}}}\n'
            '```\n\n'
            'Follow this format:\n\n'
            'Question: input question to answer\n'
            'Thought: consider previous and subsequent steps\n'
            'Action:\n'
            '```\n'
            '$JSON_BLOB\n'
            '```\n'
            'Observation: action result\n'
            '... (repeat Thought/Action/Observation N times)\n'
            'Thought: I know what to respond\n'
            'Action:\n'
            '```\n'
            '{{{{\n'
            '  "action": "Final Answer",\n'
            '  "action_input": "Final response to human"\n'
            '}}}}\n'
            'Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. '
            'Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.\n'
            'Question: {input}\n\n'
            'Thought: {agent_scratchpad}',
    }
}


def invoke_agent_llm():

    model_name = 'xinghuo-api'  # 星火api能很好的调用工具

    model = ChatOpenAI(  # 都是调用v1/chat/completion
        streaming=False,
        verbose=False,
        callbacks=[],
        openai_api_key='EMPTY',
        openai_api_base=f'{base_url}/v1',
        model_name=model_name,
        temperature=0.0001,
        max_tokens=1024
    )
    # NOTE:是按需要改动，有三处地方
    # NOTE: 定义一个适合的思考过程的模板
    prompt_template = PROMPT_TEMPLATES['agent_chat']['default']
    # prompt_template = PROMPT_TEMPLATES['agent_chat']['ChatGLM3']
    # NOTE: 需要定义一个模块，将思考过程(包含LLM输出、Agent Function的输出)合并到调用LLM的文本中
    prompt_template_agent = CustomPromptTemplate(  # 本质是里面format方法
        template=prompt_template,
        tools=tools,
        input_variables=["input", "intermediate_steps"]  # intermediate_steps给了模板里面的agent_scratchpad，模板里面history删除了。所以这里没有
    )
    # NOTE: 需要定义一个LLM返回结果的解析器，解析器需要基于提示词、LLM返回等信息解析出是否需要调用额外的工具，以及最终结果方法
    output_parser = CustomOutputParser()  # 从当前文件夹下的custom_template文件加载解析器
    llm_chain = LLMChain(
        llm=model,
        prompt=prompt_template_agent,
        llm_kwargs={
            'extra_headers': headers
        }
    )

    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nObservation:", "Observation"],
        allowed_tools=tool_names,
    )
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        memory=None,
    )

    # result = agent_executor("上海天气怎么样")  # 执行触发format方法
    # print(result)

    # result = agent_executor("id为2535的商品总共售出了多少钱")
    # print(result)

    # result = agent_executor("客户A的笔记本电脑的价格是多少")
    # print(result)

    result = agent_executor("客户C的显示器的价格是多少")
    print(result)

    # result = agent_executor("所有人中工资最高的是谁")
    # print(result)

    # result = agent_executor("王五的工资是多少")
    # print(result)



if __name__ == '__main__':
    invoke_agent_llm()
