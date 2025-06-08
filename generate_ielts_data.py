import pandas as pd
import numpy as np

# 创建示例数据
versions = [f"剑雅{i}" for i in range(10, 17)]  # 剑雅10-16
tests = [f"TEST{i}" for i in range(1, 5)]  # TEST1-4

# 创建示例范文数据
sample_essays = {
    "剑雅10": {
        "TEST1": "Some people believe that universities should accept all students, while others think that admission should be based on merit. Discuss both views and give your own opinion.",
        "TEST2": "Many people believe that the internet has made life easier and more convenient. To what extent do you agree or disagree?",
        "TEST3": "Some people think that the government should provide free housing for everyone. Others believe that it is not the government's responsibility. Discuss both views and give your opinion.",
        "TEST4": "In many countries, the number of people choosing to live alone is increasing. What are the reasons for this trend? Is it a positive or negative development?"
    },
    "剑雅11": {
        "TEST1": "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "TEST2": "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "TEST3": "Some people think that the government should invest more money in public transportation, while others believe that it is better to invest in roads and highways. Discuss both views and give your opinion.",
        "TEST4": "Many people believe that social networking sites have a negative impact on society. To what extent do you agree or disagree?"
    }
}

# 为其他版本生成类似的题目
for version in versions[2:]:
    sample_essays[version] = {
        "TEST1": f"Some people believe that {version} TEST1 topic about education and technology.",
        "TEST2": f"Many people think that {version} TEST2 topic about environment and society.",
        "TEST3": f"Some people argue that {version} TEST3 topic about health and lifestyle.",
        "TEST4": f"In recent years, {version} TEST4 topic about culture and globalization."
    }

# 创建DataFrame
df = pd.DataFrame(sample_essays).T

# 保存到Excel文件
df.to_excel("ielts.xlsx")

print("Excel文件已生成：ielts.xlsx")
print("\n数据预览：")
print(df.head()) 