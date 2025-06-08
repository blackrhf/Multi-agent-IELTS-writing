from typing import ClassVar
from metagpt.actions import Action
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
from metagpt.actions import UserRequirement
from tavily import TavilyClient

class EssayPolisher(Action):
    """雅思作文润色智能体"""
    PROMPT_TEMPLATE: ClassVar[str] = """
    请根据雅思写作评分标准对以下英语作文进行润色：
    
    原始作文：
    {essay}
    
    请按以下格式返回修改建议：
    
    评分分析
    1. 任务完成度：[分数] 评价和建议
    2. 连贯与衔接：[分数] 评价和建议
    3. 词汇丰富度：[分数] 评价和建议
    4. 语法多样性及准确性：[分数] 评价和建议
    
    优化范文
    [优化后的完整作文]
    
    修改要点
    1. [具体修改点] - [提升效果]
    2. [具体修改点] - [提升效果]
    3. [具体修改点] - [提升效果]
    
    建议论证方向
    - [论证角度1]
    - [论证角度2]
    - [论证角度3]
    """
    
    async def run(self, essay: str):
        polished = await self._aask(self.PROMPT_TEMPLATE.format(essay=essay))
        return polished

class IELTSWritingCoach(Role):
    """雅思写作辅导老师"""
    name: str = "Ms. Anderson"
    profile: str = "English Writing Tutor"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([EssayPolisher])
        self._watch([UserRequirement])
    
    async def _act(self) -> Message:
        last_msg = self.get_memories()[-1].content
        polished = await self.rc.todo.run(last_msg)
        return Message(content=polished, role=self.profile)

async def polish_essay(essay: str) -> str:
    """
    润色作文的主函数
    
    Args:
        essay (str): 需要润色的作文内容
        
    Returns:
        str: 润色后的作文内容
    """
    try:
        coach = IELTSWritingCoach()
        msg = Message(content=essay, role="Student", cause_by=UserRequirement)
        result = await coach.run(msg)
        return result.content
    except Exception as e:
        logger.error(f"Error in polish_essay: {str(e)}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # 测试代码
    test_essay = """
    I personally disagree with the issue whether the working days should be one day less. By no means should we make the weekend three days long. There are two aspects that support my point of view.

    First of all, now all over the world are facing an unprecedented economic recession caused by COVID-19. Many factories are forced to close and the shops shut down. The economic loss is substantial. Nevertheless, with the advent of vaccine, I perceive that now people can go back to their work. This would certainly be conducive to our economy. If we reduce one day from work, even just from a week, it would cause repercussions on our society in terms of the development of economy.

    Secondly, I am used to do my leisure activities in Saturday and Sunday. If there is one day more, I would wonder what to do on that day, and that means I have to rearrange my weekend plans. I think it would be tiring. Most importantly, I come to admit that, too some degree, I am a workaholic. I cannot even image if I am separated from my favourite place – my office. It is the place where I retreat to when I feel anxious and want to get rid of everything. Working, indeed, gives me a sense of achievement and contentment. I, therefore, would oppose to the idea of cutting one working day.

    Though some people may argue that they need one day more in the week to reduce their stress from work, it could be harmful to our economic growth in this harsh time. Also, I believe that many people are used to the current working system, which provides two days for break. The sudden change will make people confused. Unless the government enacts a comprehensive policy for this new system, I think the idea does not work, and it would surely brings chaos in our society.
    """
    
    import asyncio
    result = asyncio.run(polish_essay(test_essay))
    print(result) 