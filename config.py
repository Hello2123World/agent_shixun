# config.py
# -*- coding: utf-8 -*-

import streamlit as st

# ==========================================
# 1. 本地测试默认值（上传到 GitHub 前把 Key 改为 "sk-xxxx"）
# ==========================================
API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
BASE_URL = "https://api.siliconflow.cn/v1"
MODEL_NAME = "nex-agi/Nex-N2-Pro"
TEMPERATURE = 0.3

# ==========================================
# 2. 智能读取 Streamlit Secrets（云端部署或本地 streamlit 运行时自动覆盖）
# ==========================================
try:
    # 如果 Streamlit 环境中配置了 secrets，则自动用 secrets 覆盖本地变量
    if "API_KEY" in st.secrets:
        API_KEY = st.secrets["API_KEY"]
    if "BASE_URL" in st.secrets:
        BASE_URL = st.secrets["BASE_URL"]
    if "MODEL_NAME" in st.secrets:
        MODEL_NAME = st.secrets["MODEL_NAME"]
    if "TEMPERATURE" in st.secrets:
        TEMPERATURE = float(st.secrets["TEMPERATURE"])
except Exception:
    # 容错处理：如果你在终端单独运行 `python agent.py` 测试时，st.secrets 会报错。
    # 捕获异常后直接忽略，继续使用上面定义的本地默认值，保证程序绝不崩溃。
    pass