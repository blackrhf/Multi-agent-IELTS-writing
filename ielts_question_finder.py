import pandas as pd
import logging

logger = logging.getLogger(__name__)

class IELTSQuestionFinder:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        logger.info(f"初始化 IELTSQuestionFinder，使用文件: {excel_file}")
        self.df = None
        self.load_excel()

    def load_excel(self):
        try:
            logger.info(f"正在读取Excel文件: {self.excel_file}")
            # 读取Excel文件，使用第一列作为索引
            self.df = pd.read_excel(self.excel_file, index_col=0)
            logger.info(f"Excel文件读取成功，列名: {self.df.columns.tolist()}")
        except Exception as e:
            logger.error(f"读取Excel文件失败: {str(e)}")
            raise

    def get_questions(self, version):
        """获取指定版本的所有题目"""
        try:
            # 直接使用版本作为索引查找
            if version not in self.df.index:
                logger.warning(f"未找到版本 {version} 的题目")
                return []

            # 获取所有测试的题目
            questions = []
            test_columns = ['TEST1', 'TEST2', 'TEST3', 'TEST4']
            for test_col in test_columns:
                question = self.df.loc[version, test_col]
                if pd.notna(question):  # 检查题目是否为空
                    questions.append(question)

            logger.info(f"找到 {len(questions)} 个题目")
            return questions
        except Exception as e:
            logger.error(f"获取题目失败: {str(e)}")
            raise

    def get_question(self, version, test):
        """获取指定版本和测试号的题目"""
        try:
            # 检查版本是否存在
            if version not in self.df.index:
                logger.warning(f"未找到版本 {version} 的题目")
                return None

            # 检查测试号是否有效
            if test not in ['TEST1', 'TEST2', 'TEST3', 'TEST4']:
                logger.warning(f"无效的测试号: {test}")
                return None

            # 获取题目
            question = self.df.loc[version, test]
            if pd.notna(question):  # 检查题目是否为空
                logger.info(f"找到题目: {question}")
                return question
            else:
                logger.warning(f"版本 {version} 的 {test} 题目为空")
                return None
        except Exception as e:
            logger.error(f"获取题目失败: {str(e)}")
            raise

def main():
    # 测试代码
    finder = IELTSQuestionFinder('ielts.xlsx')
    
    # 测试查找特定版本的所有题目
    version = "剑雅10"
    questions = finder.get_questions(version)
    print(f"\n=== {version}的所有题目 ===")
    for i, question in enumerate(questions, 1):
        print(f"\nTest {i}:")
        print(question)

    # 测试获取单个题目
    test = "TEST1"
    question = finder.get_question(version, test)
    if question:
        print(f"\n=== {version}的{test}题目 ===")
        print(question)
    else:
        print(f"\n=== {version}的{test}题目不存在 ===")

if __name__ == "__main__":
    main() 