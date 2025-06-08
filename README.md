# Multi-agent-IELTS-writing
基于于多智能体框架的雅思大作文学习系统

基本流程: 1训练题目生成-2（作文润色）能力提升-3真题模拟及评分-4学习素材推荐

后端代码在001jupyter文件上有完整展示

使用流程：

1.注册阿里云百炼大模型平台，https://www.aliyun.com/product/bailian/，确认自己已配置api-key

2.注册Tavily账号，https://tavily.com/，创建API-Key

3.安装第三方包：

conda create -n newsdrafting python==3.10 -y
conda activate newsdrafting
pip install ipykernel tavily-python metagpt==0.7.7 httpx==0.27.2
metagpt –-init-config

4.根据上一步步 返回的metagpt config文件地址找到相应yaml文件，将api_key替换为自己在阿里云百炼平台创建的API-KEY

  api_type: "openai"  #
  model: "qwen-max"  # 或其他模型名称
  base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  api_key: "YOUR_API_KEY" # 前往阿里云百炼平台获取免费API-KEY

---------------------------------------------------------------------
文件夹内是一个前端和后端进行交互的系统
