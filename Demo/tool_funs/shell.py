# LangChain 的 Shell 工具
from pydantic import BaseModel, Field
from langchain.tools import ShellTool


def shell(query: str):
    print(f"当前运行shell命令:{query}")
    tool = ShellTool()
    return tool.run(tool_input=query)


class ShellInput(BaseModel):
    query: str = Field(description="一个能在Linux命令行运行的Shell命令")
