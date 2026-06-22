# agent.py
# -*- coding: utf-8 -*-

import sys
from config import API_KEY, BASE_URL, MODEL_NAME, TEMPERATURE
from prompts import DAILY_SYSTEM_PROMPT, STUDY_SYSTEM_PROMPT
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

class BilingualAgent:
    def __init__(self):
        """
        初始化 Agent，做好前置的输入容错检查 
        """
        if not API_KEY or API_KEY.startswith("sk-xxxxxxxx"):
            print("❌ 错误: 请先在 config.py 中配置您真实的 API_KEY！")
            sys.exit(1)
            
        # 初始化大模型基类组件 
        self.llm = ChatOpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
            model=MODEL_NAME,
            temperature=TEMPERATURE
        )

    def generate_response(self, scene: str, user_input: str, history_messages: list) -> str:
        """
        根据选定场景和历史上下文，生成大模型的回复 [cite: 3, 24, 25]
        :param scene: "日常场景" 或 "学习场景"
        :param user_input: 当前用户的输入文本
        :param history_messages: 历史对话消息列表 (包含由 HumanMessage 和 AIMessage 组成的 list)
        :return: 大模型的文本回复
        """
        # 1. 基础输入容错：过滤空内容或纯空格 
        if not user_input.strip():
            return "⚠️ 输入内容不能为空，请输入您需要处理的字句或段落。"

        # 2. 根据场景选择对应的系统提示词 
        system_content = STUDY_SYSTEM_PROMPT if scene == "学习场景" else DAILY_SYSTEM_PROMPT
        
        # 3. 核心技术：动态构建包含系统人设、历史记忆以及当前输入的消息队列 [cite: 3, 25]
        messages = [SystemMessage(content=system_content)]
        
        # 将传入的历史多轮记忆挂载到消息队列中 [cite: 3, 25]
        messages.extend(history_messages)
        
        # 挂载当前轮次用户的输入 [cite: 25]
        messages.append(HumanMessage(content=user_input))

        # 4. 异常容错处理：规避网络中断、限免流量超限等突发崩溃 
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"❌ 抱歉，大模型接口调用似乎遇到了一点问题。\n具体错误原因: {str(e)}\n提示：请检查网络连接或稍后再试。"