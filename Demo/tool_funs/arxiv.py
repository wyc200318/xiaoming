# LangChain 的 ArxivQueryRun 工具
from pydantic import BaseModel, Field
from langchain.tools.arxiv.tool import ArxivQueryRun


def arxiv(query: str):
    print(f"执行论文查询逻辑..{query}")
    tool = ArxivQueryRun()
    return tool.run(tool_input=query)


class ArxivInput(BaseModel):
    query: str = Field(description="待搜索的论文名称")
