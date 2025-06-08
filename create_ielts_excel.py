import pandas as pd

# 创建示例数据
data = {
    "版本": [f"剑雅{19-i if 19-i >= 10 else f'0{19-i}'}" for i in range(20)],
    "TEST1": [
        "Some people believe that universities should accept all students, while others think that admission should be based on merit. Discuss both views and give your own opinion.",
        "Many people believe that the government should spend more money on public transportation. Others think that money should be spent on roads and highways. Discuss both views and give your opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion."
    ],
    "TEST2": [
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion."
    ],
    "TEST3": [
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion."
    ],
    "TEST4": [
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion.",
        "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion.",
        "Some people believe that it is better to live in a big city, while others prefer to live in the countryside. Discuss both views and give your own opinion."
    ]
}

# 创建DataFrame
df = pd.DataFrame(data)

# 保存到Excel文件
df.to_excel("ielts.xlsx", index=False)

print("ielts.xlsx 文件已创建成功！") 