from flask import Flask, request, jsonify
from flask_cors import CORS
from essay_workflow import searcher_workflow, summarizer_workflow
from essay_polish import polish_essay
from ielts_question_finder import IELTSQuestionFinder
from ielts_sample_essay_finder import IELTSSampleEssayFinder
from ielts_evaluator import evaluate_essay
import asyncio
from functools import wraps
import logging
import pandas as pd
import nest_asyncio
from essay_analyzer import analyze_essay, recommend_materials

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 允许嵌套事件循环
nest_asyncio.apply()

app = Flask(__name__)
# 配置 CORS
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

def async_route(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(f(*args, **kwargs))
        finally:
            loop.close()
    return wrapped

# 初始化查询器
question_finder = IELTSQuestionFinder("ielts.xlsx")
sample_essay_finder = IELTSSampleEssayFinder()

@app.route('/api/ielts/questions/<version>', methods=['GET'])
def get_ielts_questions(version):
    try:
        logger.info(f"正在获取版本 {version} 的题目")
        # 获取所有题目
        questions = question_finder.get_questions(version)
        return jsonify({"success": True, "data": questions})
    except Exception as e:
        logger.error(f"获取题目失败: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/ielts/question/<version>/<test>', methods=['GET'])
def get_ielts_question(version, test):
    try:
        logger.info(f"正在获取版本 {version} 的 {test} 题目")
        # 获取指定测试的题目
        question = question_finder.get_question(version, test)
        return jsonify({"success": True, "data": question})
    except Exception as e:
        logger.error(f"获取题目失败: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/ielts/evaluate', methods=['POST'])
@async_route
async def evaluate_essay_endpoint():
    """评估作文并返回评分和润色结果"""
    try:
        data = request.get_json()
        essay = data.get('essay')
        task_type = data.get('task_type', 'Task 2')  # 默认为大作文
        topic = data.get('topic', '')
        
        if not essay:
            return jsonify({
                "success": False,
                "error": "No essay provided"
            }), 400

        # 获取评分
        evaluation_result = await evaluate_essay(essay, task_type, topic)
        
        # 获取润色结果
        polished_result = await polish_essay(essay)

        # 使用 print 直接输出到控制台
        print("="*50)
        print("DEBUG: evaluation_result =", evaluation_result)
        print("DEBUG: polished_result =", polished_result)
        print("="*50)

        logger.info(f"evaluation_result: {evaluation_result}")
        logger.info(f"polished_result: {polished_result}")
        
        return jsonify({
            "success": True,
            "evaluation": evaluation_result,
            "polishedEssay": polished_result
        })
    except Exception as e:
        logger.error(f"评估作文失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/ielts/sample/<version>/<test>', methods=['GET'])
def get_sample_essay(version, test):
    """获取指定版本的范文"""
    try:
        logger.info(f"正在获取版本 {version} 测试 {test} 的范文")
        result = sample_essay_finder.get_question_with_essay(version, test)
        logger.info(f"获取结果: {result}")
        return jsonify({
            "success": True,
            "data": result
        })
    except Exception as e:
        logger.error(f"获取范文失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/essay/question', methods=['GET'])
@async_route
async def get_essay_question():
    try:
        # 执行搜索工作流
        search_result = await searcher_workflow()
        if isinstance(search_result, str) and search_result.startswith("Error"):
            return jsonify({
                "success": False,
                "error": search_result
            }), 500

        # 执行总结工作流
        summarize_result = await summarizer_workflow(search_result)
        if isinstance(summarize_result, str) and summarize_result.startswith("Error"):
            return jsonify({
                "success": False,
                "error": summarize_result
            }), 500

        # 提取题目部分
        question_text = ""
        if "**题目**: " in summarize_result:
            start_idx = summarize_result.find("**题目**: ") + len("**题目**: ")
            end_idx = summarize_result.find("**参考年份**:")
            if end_idx == -1:
                end_idx = len(summarize_result)
            question_text = summarize_result[start_idx:end_idx].strip()
        
        if not question_text:
            return jsonify({
                "success": False,
                "error": "No question found in the result"
            }), 500

        return jsonify({
            "success": True,
            "question": question_text
        })
    except Exception as e:
        logger.error(f"获取作文题目失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/essay/polish', methods=['POST'])
@async_route
async def polish_essay_endpoint():
    try:
        data = request.get_json()
        essay = data.get('essay')
        
        if not essay:
            return jsonify({
                "success": False,
                "error": "No essay provided"
            }), 400

        # 直接执行作文润色，不重新生成题目
        polished_result = await polish_essay(essay)
        if isinstance(polished_result, str) and polished_result.startswith("Error"):
            return jsonify({
                "success": False,
                "error": polished_result
            }), 500
        
        return jsonify({
            "success": True,
            "polishedEssay": polished_result
        })
    except Exception as e:
        print(f"Error in polish_essay_endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/essay/analyze', methods=['POST'])
@async_route
async def analyze_essay_endpoint():
    """分析作文并返回推荐学习材料"""
    try:
        data = request.get_json()
        logger.info(f"接收到的请求数据: {data}")
        
        essay = data.get('essay')
        logger.info(f"提取的作文内容: {essay}")
        
        if not essay:
            return jsonify({
                "success": False,
                "error": "未提供作文内容"
            }), 400

        logger.info("开始分析作文...")
        # 分析作文
        analysis = await analyze_essay(essay)
        logger.info(f"作文分析结果: {analysis}")
        
        logger.info("开始推荐学习材料...")
        # 获取推荐材料
        materials = await recommend_materials(analysis)
        logger.info(f"推荐材料结果: {materials}")
        
        # 直接返回材料数据
        return jsonify({
            "success": True,
            "material": materials
        })
            
    except ValueError as ve:
        logger.error(f"输入验证错误: {str(ve)}")
        return jsonify({
            "success": False,
            "error": str(ve)
        }), 400
    except Exception as e:
        logger.error(f"分析作文失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": "分析作文失败"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
