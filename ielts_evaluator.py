import json
import sys
import asyncio
from typing import ClassVar
from metagpt.actions import Action, UserRequirement
from metagpt.roles import Role
from metagpt.environment import Environment
from metagpt.schema import Message


class IELTSWritingEvaluation(Action):
    """雅思作文评分动作"""
    PROMPT_TEMPLATE: ClassVar[str] = """
    [雅思评分指令]
    作为专业雅思考官，请严格按以下标准评分：
    
    题目: {task}
    类型: {task_type} 
    字数: {word_count}词
    {word_penalty}
    
    评分维度：
    1. 任务完成(Task Achievement):
       - 完全回应题目要求
       - 观点清晰度
       - 论证充分性
    
    2. 连贯衔接(Coherence and Cohesion):
       - 结构合理性
       - 段落连贯性
    
    3. 词汇资源(Lexical Resource):
       - 词汇多样性
       - 用词准确性
    
    4. 语法范围(Grammatical Range):
       - 结构多样性
       - 语法准确性
    
    评分规则：
    - 所有分数必须是0.5的整数倍(如5.0, 6.5)
    - 字数不足必须扣分
    
    请返回严格JSON格式：
    {{
        "scores": {{
            "task_achievement": 分数,
            "coherence_cohesion": 分数,
            "lexical_resource": 分数,
            "grammatical_range": 分数,
            "overall": 总分
        }},
        "feedback": {{
            "task": "反馈内容",
            "coherence": "反馈内容",
            "vocabulary": "反馈内容",
            "grammar": "反馈内容",
            "general": "总体建议"
        }},
        "word_penalty": "字数说明"
    }}
    """
    
    name: str = "IELTS_Evaluator"
    
    def round_score(self, score: float) -> float:
        """确保分数为0.5的倍数"""
        return round(score * 2) / 2

    async def run(self, task: str, task_type: str, essay: str, word_count: int):
        # 字数检查
        penalty = ""
        min_words = 150 if task_type == "Task 1" else 250
        if word_count < min_words:
            penalty = f"⚠️ 字数不足: 仅{word_count}词(要求{min_words}词)，将扣分"
        
        # 构建提示词
        prompt = self.PROMPT_TEMPLATE.format(
            task=task,
            task_type=task_type,
            essay=essay,
            word_count=word_count,
            word_penalty=penalty
        )
        
        # 获取评分
        response = await self._aask(prompt)
        
        # 结果处理
        try:
            result = json.loads(response)
            # 分数标准化
            for key in result["scores"]:
                result["scores"][key] = self.round_score(float(result["scores"][key]))
            return json.dumps(result, ensure_ascii=False)
        except:
            return response

class IELTSEvaluator(Role):
    """雅思评分专家"""
    name: str = "IELTS_Examiner"
    profile: str = "Professional IELTS Writing Evaluator"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([IELTSWritingEvaluation])
        self._watch([UserRequirement])
    
    async def _act(self) -> Message:
        # 获取输入
        last_msg = [m for m in self.get_memories() if isinstance(m, Message)][-1]
        content = last_msg.content
        
        # 解析输入
        try:
            task, task_type, essay = content.split("|", 2)
            word_count = len(essay.split())
            
            # 执行评分
            evaluation = await self.rc.todo.run(
                task.strip(),
                task_type.strip(),
                essay.strip(),
                word_count
            )
            
            return Message(
                content=evaluation,
                role=self.profile,
                cause_by=type(self.rc.todo)
            )
            
        except Exception as e:
            error_msg = f"输入格式错误: {str(e)}"
            return Message(
                content=error_msg,
                role=self.profile,
                cause_by=type(self.rc.todo)
            )

async def evaluate_essay(essay: str, task_type: str = "Task 2", topic: str = "Education Access"):
    """执行评分工作流"""
    # 初始化
    env = Environment()
    examiner = IELTSEvaluator()
    env.add_roles([examiner])
    
    # 构建输入
    input_msg = Message(
        content=f"{topic}|{task_type}|{essay}",
        role="Human",
        cause_by=UserRequirement,
        send_to=examiner.name
    )
    
    # 运行
    env.publish_message(input_msg)
    await env.run()
    
    # 获取结果
    result_content = None
    print("环境历史消息数量:", len(env.history))
    
    # 将所有字符组合成完整消息
    full_message = ""
    for msg in env.history:
        if isinstance(msg, str):
            full_message += msg
    
    print("\n完整消息:", full_message)
    
    # 尝试从完整消息中提取JSON
    try:
        # 查找JSON开始和结束的位置
        start = full_message.find('{')
        end = full_message.rfind('}') + 1
        if start != -1 and end != 0:
            json_str = full_message[start:end]
            result = json.loads(json_str)
            if isinstance(result, dict) and "scores" in result:
                result_content = json_str
                print("找到评分结果:", result_content)
    except json.JSONDecodeError:
        print("JSON解析失败")
    except Exception as e:
        print(f"处理消息时出错: {str(e)}")
    
    print("\n最终result_content:", result_content)
    
    # 处理结果
    if result_content:
        try:
            result = json.loads(result_content)
            print("=== IELTS 评分结果 ===")
            print(f"总分: {result['scores']['overall']}")
            print(f"\n任务完成: {result['scores']['task_achievement']}")
            print(f"反馈: {result['feedback']['task']}")
            print(f"\n连贯衔接: {result['scores']['coherence_cohesion']}")
            print(f"反馈: {result['feedback']['coherence']}")
            print(f"\n词汇: {result['scores']['lexical_resource']}")
            print(f"反馈: {result['feedback']['vocabulary']}")
            print(f"\n语法: {result['scores']['grammatical_range']}")
            print(f"反馈: {result['feedback']['grammar']}")
            print(f"\n字数评估: {result.get('word_penalty', '符合要求')}")
            print(f"\n总体建议: {result['feedback']['general']}")
            return result
        except json.JSONDecodeError:
            print("原始评分结果:", result_content)
            return result_content
        except Exception as e:
            print(f"结果解析错误: {str(e)}")
            return None
    
    return None

def main():
    # 测试用例
    test_essay = """Many argue that universities should accept all students, while others believe admission should be merit-based. This essay discusses both views before presenting my opinion.

    Supporters of open access argue education is a fundamental right. They contend that restricting access creates inequality. Additionally, some students develop academic abilities later in life.

    Opponents argue limited resources necessitate selective admissions. They maintain high standards would decline if universities accepted weaker students. Furthermore, they believe meritocracy ensures the most capable students receive education.

    In my view, while academic merit is important, universities should also consider potential. A balanced approach considering both achievement and aptitude would benefit society most."""

    # 修改异步处理方式
    async def run_evaluation():
        return await evaluate_essay(
            essay=test_essay,
            task_type="Task 2",
            topic="University Access"
        )
    
    # 使用新的事件循环策略
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    result = asyncio.run(run_evaluation())
    print("【main函数打印返回值】", result)

if __name__ == "__main__":
    main() 