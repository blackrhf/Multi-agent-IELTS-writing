from metagpt.actions import Action, UserRequirement
from metagpt.roles import Role
from metagpt.schema import Message
from tavily import TavilyClient
from typing import ClassVar
import asyncio
import tenacity
import os
import logging

# 配置日志
logger = logging.getLogger(__name__)

# 设置模型配置
# os.environ["METAGPT_MODEL"] = "gpt-3.5-turbo"

# 初始化客户端
tavily_client = TavilyClient(api_key="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")
analysis_result = None

class EssayAnalyzer(Action):
    """作文分析智能体，识别主题和评估水平"""
    PROMPT_TEMPLATE: ClassVar[str] = """
    请分析以下英语作文并识别主要问题：
    作文内容：{essay}
    
    请按以下格式返回分析结果：
    作文主题：[一句话概括作文的内容]
    水平评估：[CEFR等级评估，如B1]
    重点改进领域：[3-5个最需要改进的领域]
    """
    
    async def run(self, topic: str, essay: str):
        analysis = await self._aask(self.PROMPT_TEMPLATE.format(topic=topic, essay=essay))
        return analysis

class EnglishTutor(Role):
    """英语作文辅导老师角色(仅分析功能)"""
    name: str = "Ms. Anderson"
    profile: str = "English Writing Tutor"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([EssayAnalyzer])
        self._watch([UserRequirement])
    
    async def _act(self) -> Message:
        last_msg = self.get_memories()[-1].content
        logger.info(f"收到的原始消息: {last_msg}")
        
        # 直接使用整个消息作为作文内容
        essay = last_msg.strip()
        logger.info(f"解析后的作文内容: {essay}")
        
        analysis = await self.rc.todo.run("", essay)  # 主题参数可以为空
        return Message(content=f"作文分析结果：\n{analysis}", role=self.profile)
    
    def _parse_input(self, input_str: str) -> tuple:
        """这个方法不再使用，保留是为了兼容性"""
        return ("", input_str.strip())

class LearningMaterialSearcher(Action):
    """学习素材检索智能体"""
    PROMPT_TEMPLATE: ClassVar[str] = """
   根据以下作文分析结果，请为学习者生成一篇阅读材料：
    学生水平：{level}
    重点改进领域：{weaknesses}
    作文主题：{topic}
    
    请生成一篇与作文主题相关的英文文章，文章难度略高于学生当前水平。
    返回格式：
    Title: [文章标题]
    Content: [文章正文]
    Learning Value: [学习价值]
    Difficulty: [阅读难度]
    """
    
    async def run(self, topic: str, level: str, weaknesses: str):
        try:
            # 检查API key
            if not tavily_client.api_key or tavily_client.api_key == "your-api-key-here":
                logger.warning("Tavily API key未设置或无效")
                # 返回模拟数据
                return {
                    "title": f"Improving Writing Skills for {level} Level Students",
                    "content": "This article focuses on common writing challenges faced by students and provides practical solutions. It covers topics such as grammar accuracy, vocabulary usage, and logical structure in academic writing.",
                    "learning_value": f"帮助学生理解并改进{weaknesses}",
                    "difficulty": level
                }

            # 如果有有效的API key，则使用Tavily搜索
            search_query = f"English learning material about {topic} for {level} level students focusing on {weaknesses}"
            
            materials = tavily_client.get_search_context(
                query=search_query,
                max_results=1,
                include_domains=[
                    "learnenglish.britishcouncil.org",
                    "newsinlevels.com",
                    "breakingnewsenglish.com"
                ],
                search_depth="advanced"
            )
            
            curated_materials = await self._aask(self.PROMPT_TEMPLATE.format(
                level=level,
                weaknesses=weaknesses,
                topic=topic
            ))
            
            # 解析返回的内容
            lines = curated_materials.split('\n')
            result = {}
            current_key = None
            current_value = []
            
            for line in lines:
                line = line.strip()
                if line.startswith('Title:'):
                    if current_key:
                        result[current_key] = '\n'.join(current_value).strip()
                    current_key = 'title'
                    current_value = [line[6:].strip()]
                elif line.startswith('Content:'):
                    if current_key:
                        result[current_key] = '\n'.join(current_value).strip()
                    current_key = 'content'
                    current_value = [line[8:].strip()]
                elif line.startswith('Learning Value:'):
                    if current_key:
                        result[current_key] = '\n'.join(current_value).strip()
                    current_key = 'learning_value'
                    current_value = [line[14:].strip()]
                elif line.startswith('Difficulty:'):
                    if current_key:
                        result[current_key] = '\n'.join(current_value).strip()
                    current_key = 'difficulty'
                    current_value = [line[10:].strip()]
                elif line and current_key:
                    current_value.append(line)
            
            if current_key:
                result[current_key] = '\n'.join(current_value).strip()
            
            return result
            
        except Exception as e:
            logger.error(f"搜索学习材料时发生错误: {str(e)}")
            # 返回模拟数据
            return {
                "title": f"Writing Improvement Guide for {level} Level",
                "content": f"A practical guide focusing on common writing challenges and solutions for {level} level students. Includes examples and exercises for improving {weaknesses}.",
                "learning_value": "针对性解决写作问题",
                "difficulty": level
            }

def extract_info(text: str, key: str) -> str:
    """从文本中提取特定信息"""
    try:
        start = text.find(key)
        if start == -1:
            logger.warning(f"未找到关键字: {key}")
            return ""
            
        # 查找冒号（支持中英文冒号）
        colon_pos = text.find("：", start)
        if colon_pos == -1:
            colon_pos = text.find(":", start)
        if colon_pos == -1:
            logger.warning(f"未找到冒号分隔符: {key}")
            return ""
            
        # 对于重点改进领域，需要特殊处理
        if key == "重点改进领域":
            # 找到下一个主要标题的开始位置
            next_section = text.find("\n\n", colon_pos)
            if next_section == -1:
                next_section = len(text)
            result = text[colon_pos + 1:next_section].strip()
        else:
            # 对于其他字段，只取到下一个换行符
            end = text.find("\n", colon_pos)
            if end == -1:
                end = len(text)
            result = text[colon_pos + 1:end].strip()
            
        logger.debug(f"从文本中提取 {key}: {result}")
        return result
    except Exception as e:
        logger.error(f"提取信息时发生错误: {str(e)}")
        return ""

async def analyze_essay(essay_submission: str):
    """分析作文"""
    global analysis_result
    try:
        if not essay_submission or len(essay_submission.strip()) == 0:
            raise ValueError("作文内容不能为空")
            
        logger.info("开始分析作文...")
        tutor = EnglishTutor()
        msg = Message(content=essay_submission, role="Student", cause_by=UserRequirement)
        result = await tutor.run(msg)
        
        if not result or not result.content:
            raise ValueError("分析结果为空")
            
        analysis_result = result.content
        logger.info("作文分析完成")
        return analysis_result
    except Exception as e:
        logger.error(f"分析作文时发生错误: {str(e)}")
        raise

async def recommend_materials(analysis_result: str):
    """推荐学习材料"""
    try:
        if not analysis_result:
            raise ValueError("分析结果不能为空")
            
        logger.info("开始推荐学习材料...")
        topic = extract_info(analysis_result, "作文主题")
        level = extract_info(analysis_result, "水平评估")
        weaknesses = extract_info(analysis_result, "重点改进领域")
        
        if not all([topic, level, weaknesses]):
            raise ValueError("无法从分析结果中提取必要信息")
        
        searcher = LearningMaterialSearcher()
        materials = await searcher.run(topic, level, weaknesses)
        logger.info("学习材料推荐完成")
        return materials
    except Exception as e:
        logger.error(f"推荐学习材料时发生错误: {str(e)}")
        raise

# 测试代码
if __name__ == "__main__":
    # 测试用例
    test_text = """作文主题：Comparison between urban and rural living with personal preference based on lifestyle priorities
水平评估：B1
重点改进领域：
1. 逻辑衔接强化 - 段落间过渡较机械
2. 词汇多样性提升 - "advantages and disadvantages"重复出现
3. 论证深度扩展 - 缺乏具体事例支撑
4. 结尾段深化 - 结论停留在个人选择层面
5. 句法复杂度 - 简单句占比过高"""

    print("=== 测试信息提取 ===")
    print("1. 测试作文主题提取:")
    topic = extract_info(test_text, "作文主题")
    print(f"提取结果: {topic}")
    
    print("\n2. 测试水平评估提取:")
    level = extract_info(test_text, "水平评估")
    print(f"提取结果: {level}")
    
    print("\n3. 测试重点改进领域提取:")
    weaknesses = extract_info(test_text, "重点改进领域")
    print(f"提取结果: {weaknesses}")
    
    print("\n4. 测试不存在的字段:")
    not_exist = extract_info(test_text, "不存在的字段")
    print(f"提取结果: {not_exist}")

    # 示例作文
    essay_submission = """
I personally disagree with the issue whether the working days should be one day less. By no means should we make the weekend three days long. There are two aspects that support my point of view.

First of all, now all over the world are facing an unprecedented economic recession caused by COVID-19. Many factories are forced to close and the shops shut down. The economic loss is substantial. Nevertheless, with the advent of vaccine, I perceive that now people can go back to their work. This would certainly be conducive to our economy. If we reduce one day from work, even just from a week, it would cause repercussions on our society in terms of the development of economy.

Secondly, I am used to do my leisure activities in Saturday and Sunday. If there is one day more, I would wonder what to do on that day, and that means I have to rearrange my weekend plans. I think it would be tiring. Most importantly, I come to admit that, too some degree, I am a workaholic. I cannot even image if I am separated from my favourite place – my office. It is the place where I retreat to when I feel anxious and want to get rid of everything. Working, indeed, gives me a sense of achievement and contentment. I, therefore, would oppose to the idea of cutting one working day.

Though some people may argue that they need one day more in the week to reduce their stress from work, it could be harmful to our economic growth in this harsh time. Also, I believe that many people are used to the current working system, which provides two days for break. The sudden change will make people confused. Unless the government enacts a comprehensive policy for this new system, I think the idea does not work, and it would surely brings chaos in our society.
    """
    
    async def main():
        try:
            # 分析作文
            analysis = await analyze_essay(essay_submission)
            print("\n=== 作文分析测试 ===")
            print("分析结果：")
            print(analysis)
            
            # 推荐学习材料
            materials = await recommend_materials(analysis)
            print("\n推荐材料：")
            print(materials)
        except Exception as e:
            print(f"执行过程中发生错误: {str(e)}")
    
    # 获取事件循环并运行主程序
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close() 