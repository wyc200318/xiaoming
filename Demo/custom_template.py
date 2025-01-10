# -*- coding: utf-8 -*-
from __future__ import annotations
from langchain.agents import Tool, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from typing import List
from langchain.schema import AgentAction, AgentFinish


class CustomPromptTemplate(StringPromptTemplate):
    template: str
    tools: List[Tool]
    # {agent_scratchpad}通常在代理的“Thought”阶段被填充，使用的intermediate_steps里面东西，用于记录代理在解决问题过程中的思考和决策。
    def format(self, **kwargs) -> str:  # 包含input，tool和其描述信息，将模板补全送入大语言模型
        intermediate_steps = kwargs.pop("intermediate_steps")  # 调用tool和返回的结果是什么
        thoughts = ""
        for action, observation in intermediate_steps:  # 第一次结果得到intermediate_steps，第二次里面才有内容
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        kwargs["agent_scratchpad"] = thoughts
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])  # 获取工具
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)  # 将之前过程信息拼接到一起，准备调用大模型


class CustomOutputParser(AgentOutputParser):
    begin: bool = False

    def __init__(self):
        super().__init__()
        self.begin = True
    # 大语言模型结果的解析
    def parse(self, llm_output: str) -> AgentFinish | tuple[dict[str, str], str] | AgentAction:
        # LLM一般会输出比较多的信息，将无效的信息截断丢弃
        if self.begin:
            # self.begin = False
            stop_words = ["Observation:"]  # 截取Observation之前的文本，后面都是假设的东西
            min_index = len(llm_output)
            for stop_word in stop_words:
                index = llm_output.find(stop_word)  # 停止字符
                if index != -1 and index < min_index:
                    min_index = index
                llm_output = llm_output[:min_index]  # 截取下一步应该做的东西，截至长的假设输出

        # 当发现有最终结果的特殊字符的时候，直接结束 -- 返回最终结果
        if "Final Answer:" in llm_output:
            self.begin = True
            return AgentFinish(
                return_values={"output": llm_output.split("Final Answer:", 1)[-1].strip()},
                log=llm_output,
            )

        # 获取LLM返回需要出发的agent function name和入参
        parts = llm_output.split("Action:")
        if len(parts) < 2:
            return AgentFinish(
                return_values={"output": f"调用agent工具失败，该回答为大模型自身能力的回答:\n\n `{llm_output}`"},
                log=llm_output,
            )

        # 直接llm返回中的action input后的内容
        action = parts[1].split("Action Input:")[0].strip()
        action_input = parts[1].split("Action Input:")[1].strip()
        try:
            ans = AgentAction(  # 调用相应tool的方法
                tool=action,
                tool_input=action_input.strip(" ").strip('"'),
                log=llm_output
            )
            return ans
        except:
            return AgentFinish(
                return_values={"output": f"调用agent失败: `{llm_output}`"},
                log=llm_output,
            )
