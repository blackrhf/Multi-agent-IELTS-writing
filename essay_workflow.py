from metagpt.actions import Action, UserRequirement
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.environment import Environment
from metagpt.const import MESSAGE_ROUTE_TO_ALL
from tavily import TavilyClient
from typing import ClassVar
import os
from dotenv import load_dotenv
import time
from tenacity import retry, stop_after_attempt, wait_exponential

# 加载环境变量
load_dotenv()

# 初始化Tavily客户端
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', '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')
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# 设置 OpenAI API 密钥
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
else:
    print("Warning: OPENAI_API_KEY not found in environment variables")

# 网络语料检索
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def rag_internet(question, max_results=5, max_tokens=4000):
    try:
        return tavily_client.get_search_context(
            query=question, 
            max_results=max_results,
            include_domains=["bbc.com", "technologyreview.com", "sciencedaily.com"],
            search_depth="advanced",
            max_tokens=max_tokens
        )
    except Exception as e:
        print(f"Error in rag_internet: {str(e)}")
        raise  # 让重试装饰器处理异常

# 搜索相关类
class Search(Action):
    PROMPT_TEMPLATE: ClassVar[str] = """事件主题：{topic}\n相关新闻：{news}\n请对相关新闻进行整理，按照新闻类型大致分类并输出概要。返回的内容里不应有URL。"""
    name: str = "Search"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def run(self, topic: str):
        if not self.PROMPT_TEMPLATE:
            raise NotImplementedError("资料收集智能体的 PROMPT_TEMPLATE 未实现!")

        print("\n=== 语料检索 ===")
        news = rag_internet(topic)
        print(news)
        print("\n=== 整理语料 ===")
        try:
            corpus = await self._aask(self.PROMPT_TEMPLATE.format(topic=topic, news=news))
            return corpus
        except Exception as e:
            print(f"Error in Search.run: {str(e)}")
            raise  # 让重试装饰器处理异常

class Searcher(Role):
    name: str = "Dan"
    profile: str = "Searcher"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        watch_list = [UserRequirement]
        action_list = [Search]

        if not watch_list:
            raise NotImplementedError("资料收集智能体的监听对象未定义!")
        if not action_list:
            raise NotImplementedError("资料收集智能体的动作空间未定义!")

        self._watch(watch_list)
        self.set_actions(action_list)

    async def _act(self) -> Message:
        topic_input = self.get_memories()[-1].content.strip()
        news_content = await self.rc.todo.run(topic_input)
        return Message(content=news_content, role=self.profile, cause_by=type(self.rc.todo))

# 总结相关类
class Summarize1(Action):
    PROMPT_TEMPLATE: ClassVar[str] = """{corpus}\n请根据新闻素材，筛选和雅思作文主题相关的新闻，并对相关新闻事件做一个简要的总结（1-2句话）"""
    name: str = "Summarize1"

    async def run(self, corpus: str):
        if not self.PROMPT_TEMPLATE:
            raise NotImplementedError("资料整理智能体第一步的 PROMPT_TEMPLATE 未实现!")
        print("\n=== 执行Summarize1 ===")
        rsp = await self._aask(self.PROMPT_TEMPLATE.format(corpus=corpus))
        return rsp

class Summarize2(Action):
    PROMPT_TEMPLATE: ClassVar[str] = """{corpus}\n请基于上述语料，根据新闻的主题不同权重不同，"环境": 0.3, "科技": 0.25, "教育": 0.2, "社会": 0.15, "文化": 0.1。按照权重随机的选择一条新闻。"""
    name: str = "Summarize2"

    async def run(self, corpus: str):
        if not self.PROMPT_TEMPLATE:
            raise NotImplementedError("资料整理智能体第二步的 PROMPT_TEMPLATE 未实现!")
        print("\n=== 执行Summarize2 ===")
        rsp = await self._aask(self.PROMPT_TEMPLATE.format(corpus=corpus))
        return rsp

class Summarize3(Action):
    PROMPT_TEMPLATE: ClassVar[str] = """{corpus}\n请基于上述语料，生成一道与雅思学术类写作Task 2真题高度相似的题目，要求：  
1. **年份限定**：模仿2020-2023年雅思写作题型和话题趋势；  
2. **题型选择**：从以下任选一种：  
   - Opinion (Agree/Disagree)  
   - Discussion (Discuss Both Views)  
   - Advantages/Disadvantages  
   - Problem/Solution  
   - Two-part Question  
3. **话题范围**：教育、科技、环境、社会、文化；  
4. **语言风格**：使用官方真题的句式（如'Some people believe...while others...'）；  
5. **输出格式**：  
   - 题型: [类型]  
   - 题目: [完整题目]  
   - 参考年份: [仿真的年份，如'2022年风格']"""
    name: str = "Summarize3"

    async def run(self, corpus: str):
        if not self.PROMPT_TEMPLATE:
            raise NotImplementedError("资料整理智能体第三步的 PROMPT_TEMPLATE 未实现!")
        print("\n=== 执行Summarize3 ===")
        rsp = await self._aask(self.PROMPT_TEMPLATE.format(corpus=corpus))
        return rsp

class Summarizer(Role):
    name: str = "Dan"
    profile: str = "Summarizer"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        watch_list = [Search]
        if not watch_list:
            raise NotImplementedError("资料整理智能体的监听对象未定义!")
        self._watch(watch_list)
        self.set_actions([Summarize1(), Summarize2(), Summarize3()])
        self._set_react_mode(react_mode="by_order")

# 工作流函数
async def searcher_workflow():
    try:
        news_company = Environment()
        news_company.add_roles([Searcher()])
        
        news_company.publish_message(
            Message(role="Human", 
                    content="2025年上半年新闻",
                    cause_by=UserRequirement,
                    send_to=MESSAGE_ROUTE_TO_ALL)
        )
        
        await news_company.run()
        if not news_company.history:
            return "Error: No search results found"
            
        # 合并所有消息内容
        result = ""
        for msg in news_company.history:
            if isinstance(msg, str):
                result += msg
            elif hasattr(msg, 'content'):
                result += msg.content
            else:
                result += str(msg)
        return result
    except Exception as e:
        error_msg = f"Error in search workflow: {str(e)}"
        print(error_msg)
        return error_msg

async def summarizer_workflow(search_output):
    try:
        if isinstance(search_output, str):
            search_output = Message(content=search_output, role="System")
            
        news_company = Environment()
        news_company.add_roles([Summarizer()])
        
        news_company.publish_message(
            Message(role="Searcher", 
                    content=search_output.content if hasattr(search_output, 'content') else str(search_output),
                    cause_by=Search,
                    send_to=MESSAGE_ROUTE_TO_ALL)
        )
        
        await news_company.run()
        if not news_company.history:
            return "Error: No summary results found"
            
        # 合并所有消息内容
        result = ""
        for msg in news_company.history:
            if isinstance(msg, str):
                result += msg
            elif hasattr(msg, 'content'):
                result += msg.content
            else:
                result += str(msg)
        return result
    except Exception as e:
        error_msg = f"Error in summarizer workflow: {str(e)}"
        print(error_msg)
        return error_msg 