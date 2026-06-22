# app.py
# -*- coding: utf-8 -*-

import streamlit as st
from agent import BilingualAgent
from langchain_core.messages import HumanMessage, AIMessage

# 1. 初始化页面配置
st.set_page_config(
    page_title="中英文双语助手 Agent",
    page_icon="🤖",
    layout="wide"
)

# 2. 在 Session 状态中持久化初始化 Agent 实例和历史记忆 
if "agent" not in st.session_state:
    st.session_state.agent = BilingualAgent()

if "history" not in st.session_state:
    st.session_state.history = []  # 用于给大模型传递的 LangChain 消息列表 [cite: 25]

if "display_history" not in st.session_state:
    st.session_state.display_history = []  # 用于在前端界面渲染的对话记录

# 3. 侧边栏设计：实现场景切换与记忆重置 [cite: 24, 51]
st.sidebar.title("⚙️ 控制面板")
scene_mode = st.sidebar.selectbox(
    "请选择使用场景：",
    ["日常场景", "学习场景"],
    help="不同场景下，助手的语气、翻译风格和纠错侧重点会完全不同 [cite: 24]。"
)

st.sidebar.markdown("---")
# 支持重置对话重新开始 [cite: 51]
if st.sidebar.button("🧹 清空当前对话历史"):
    st.session_state.history = []
    st.session_state.display_history = []
    st.success("对话历史已清空！")
    st.rerun()

st.sidebar.info(
    "💡 功能提示：\n"
    "- 输入中文：自动帮您翻译为英文 [cite: 24]。\n"
    "- 输入英文：自动进行语法纠错与语句润色 [cite: 24]。\n"
    "- 支持多轮连续对话探讨细节 [cite: 24]！"
)

# 4. 主界面渲染
st.title("🤖 中英文双语助手 Agent")
st.caption(f"当前技术栈：Python + LangChain + Streamlit | 驱动模型：{scene_mode} ({st.session_state.agent.llm.model_name})")

# 展示历史对话流
for message in st.session_state.display_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 核心聊天交互逻辑
if user_prompt := st.chat_input("请输入您想要翻译、润色或纠错的文本..."):
    
    # 在前端即时渲染用户输入
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.display_history.append({"role": "user", "content": user_prompt})

    # 调用 Agent 获取包含容错机制的回复 
    with st.chat_message("assistant"):
        with st.spinner("思考与组织语言中..."):
            assistant_reply = st.session_state.agent.generate_response(
                scene=scene_mode,
                user_input=user_prompt,
                history_messages=st.session_state.history
            )
            st.markdown(assistant_reply)
            
    # 如果回复没有报错，则将这一轮对话加入多轮记忆上下文 [cite: 3, 24]
    if not assistant_reply.startswith("❌") and not assistant_reply.startswith("⚠️"):
        st.session_state.history.append(HumanMessage(content=user_prompt))
        st.session_state.history.append(AIMessage(content=assistant_reply))
        st.session_state.display_history.append({"role": "assistant", "content": assistant_reply})