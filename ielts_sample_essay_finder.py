import pandas as pd
import logging
from sample_essays_data import SAMPLE_ESSAYS

logger = logging.getLogger(__name__)

class IELTSSampleEssayFinder:
    def __init__(self, excel_path='ielts.xlsx'):
        logger.info(f"初始化 IELTSSampleEssayFinder，使用文件: {excel_path}")
        # 读取Excel文件，跳过第一行
        self.df = pd.read_excel(excel_path, header=0)
        logger.info(f"Excel文件读取成功，列名: {self.df.columns.tolist()}")
        self.sample_essays = SAMPLE_ESSAYS
    
    def find_sample_essay(self, version: str, test: str) -> str:
        """
        查找特定版本的特定范文（测试用：始终返回剑雅10 TEST1的范文）
        
        Args:
            version: 剑雅版本，如 "剑雅16"
            test: 测试编号，如 "TEST1"
            
        Returns:
            str: 范文内容
        """
        # 测试用：始终返回剑雅10 TEST1的范文
        return self.sample_essays["剑雅10"]["TEST1"]
    
    def get_sample_essay(self, version, test):
        """获取指定版本和测试号的参考范文"""
        try:
            # 在A列中查找版本信息（2-11行）
            version_rows = self.df.iloc[1:11]  # 获取2-11行
            version_index = version_rows[version_rows.iloc[:, 0] == version].index
            if len(version_index) == 0:
                logger.warning(f"未找到版本 {version} 的参考范文")
                return None

            # 将TEST1-4映射到对应的列索引
            test_to_column = {
                'TEST1': 2,  # C列
                'TEST2': 4,  # E列
                'TEST3': 6,  # G列
                'TEST4': 8   # I列
            }

            if test in test_to_column:
                col_idx = test_to_column[test]
                essay = self.df.iloc[version_index[0], col_idx]
                if pd.notna(essay):  # 检查参考范文是否为空
                    logger.info(f"找到参考范文: {essay[:100]}...")  # 只显示前100个字符
                    return essay
                else:
                    logger.warning(f"版本 {version} 的 {test} 参考范文为空")
                    return None
            else:
                logger.warning(f"未找到测试 {test}")
                return None
        except Exception as e:
            logger.error(f"获取参考范文失败: {str(e)}")
            raise

    def get_question_with_essay(self, version: str, test: str) -> dict:
        """
        获取题目和对应的范文
        
        Args:
            version: 剑雅版本，如 "剑雅16"
            test: 测试编号，如 "TEST1"
            
        Returns:
            dict: 包含题目和范文的字典
        """
        try:
            # 在A列中查找版本信息（2-11行）
            version_rows = self.df.iloc[1:11]  # 获取2-11行
            version_index = version_rows[version_rows.iloc[:, 0] == version].index
            if len(version_index) == 0:
                logger.warning(f"未找到版本 {version} 的题目")
                return {
                    "version": version,
                    "test": test,
                    "question": None,
                    "sample_essay": None
                }

            # 将TEST1-4映射到对应的列索引
            test_to_column = {
                'TEST1': 2,  # C列
                'TEST2': 4,  # E列
                'TEST3': 6,  # G列
                'TEST4': 8   # I列
            }

            if test in test_to_column:
                col_idx = test_to_column[test]
                question = self.df.iloc[version_index[0], col_idx]
                essay = self.get_sample_essay(version, test)
                
                return {
                    "version": version,
                    "test": test,
                    "question": question if pd.notna(question) else None,
                    "sample_essay": essay
                }
            else:
                logger.warning(f"未找到测试 {test}")
                return {
                    "version": version,
                    "test": test,
                    "question": None,
                    "sample_essay": None
                }
        except Exception as e:
            logger.error(f"获取题目和范文失败: {str(e)}")
            raise

def main():
    # 测试代码
    finder = IELTSSampleEssayFinder()
    
    # 测试获取参考范文
    version = "剑雅18"
    test = "TEST1"
    essay = finder.get_sample_essay(version, test)
    if essay:
        print(f"\n=== {version}的{test}参考范文 ===")
        print(essay)
    else:
        print(f"\n=== {version}的{test}参考范文不存在 ===")

    # result1 = finder.get_question_with_essay("剑雅10", "TEST1")
    # result2 = finder.get_question_with_essay("剑雅11", "TEST2")
    # result3 = finder.get_question_with_essay("剑雅16", "TEST3")
    # print("result1-----------",result1)
    # print("result2------------",result2)
    # print("result3------------",result3)

if __name__ == "__main__":
    main() 