# 100个优质开源Agent项目汇总

> 更新时间：2025年3月  
> 数据来源：GitHub、开源中国、技术社区等

---

## 📑 目录

1. [通用Agent框架](#一通用agent框架)
2. [编程Agent](#二编程agent)
3. [RAG与知识库Agent](#三rag与知识库agent)
4. [多Agent协作框架](#四多agent协作框架)
5. [自动化与工作流Agent](#五自动化与工作流agent)
6. [数据分析Agent](#六数据分析agent)
7. [垂直领域Agent](#七垂直领域agent)
8. [Agent开发工具与平台](#八agent开发工具与平台)

---

## 一、通用Agent框架

### 1. AutoGPT
- **GitHub链接**: https://github.com/Significant-Gravitas/AutoGPT
- **简介**: 最早的自主AI Agent项目之一，能够自动执行分解任务并调用工具
- **Star数**: 179k+
- **主要功能**: 自主任务分解、网络搜索、文件操作、代码执行、长期记忆
- **适用场景**: 通用自动化任务、研究分析、内容生成
- **技术栈**: Python, OpenAI API
- **活跃度评估**: ⭐⭐⭐⭐⭐ 极高，社区活跃，持续更新

### 2. LangChain
- **GitHub链接**: https://github.com/langchain-ai/langchain
- **简介**: 最流行的LLM应用开发框架，提供完整的Agent构建工具链
- **Star数**: 117k+
- **主要功能**: 链式调用、工具集成、记忆管理、Agent编排
- **适用场景**: 企业级LLM应用、复杂Agent系统
- **技术栈**: Python/JS/TS, 多模型支持
- **活跃度评估**: ⭐⭐⭐⭐⭐ 极高，生态完善

### 3. LangGraph
- **GitHub链接**: https://github.com/langchain-ai/langgraph
- **简介**: LangChain团队推出的状态机Agent框架，支持复杂工作流
- **Star数**: 25k+
- **主要功能**: 状态管理、循环工作流、多Agent协调
- **适用场景**: 复杂多步骤任务、对话系统
- **技术栈**: Python, LangChain
- **活跃度评估**: ⭐⭐⭐⭐⭐ 快速增长中

### 4. LlamaIndex
- **GitHub链接**: https://github.com/run-llama/llama_index
- **简介**: 专注于数据索引和检索的LLM框架
- **Star数**: 38k+
- **主要功能**: 数据索引、RAG、查询引擎、Agent工具
- **适用场景**: 知识库问答、文档分析
- **技术栈**: Python, 多种向量数据库
- **活跃度评估**: ⭐⭐⭐⭐⭐ 非常活跃

### 5. CrewAI
- **GitHub链接**: https://github.com/joaomdmoura/crewAI
- **简介**: 专注于多Agent团队协作的框架
- **Star数**: 28k+
- **主要功能**: 角色定义、任务分配、团队协作、流程编排
- **适用场景**: 复杂任务分解、团队模拟
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 热度持续上升

### 6. Semantic Kernel
- **GitHub链接**: https://github.com/microsoft/semantic-kernel
- **简介**: 微软开源的LLM应用开发SDK
- **Star数**: 24k+
- **主要功能**: 插件系统、规划器、记忆管理、多语言支持
- **适用场景**: 企业级AI应用、微软生态集成
- **技术栈**: C#, Python, Java
- **活跃度评估**: ⭐⭐⭐⭐⭐ 微软官方维护

### 7. SuperAGI
- **GitHub链接**: https://github.com/TransformerOptimus/SuperAGI
- **简介**: 开发者友好的开源AI Agent平台
- **Star数**: 15k+
- **主要功能**: Agent构建、工具集成、并发执行、GUI界面
- **适用场景**: Agent快速开发、原型验证
- **技术栈**: Python, React
- **活跃度评估**: ⭐⭐⭐⭐ 活跃

### 8. BabyAGI
- **GitHub链接**: https://github.com/yoheinakajima/babyagi
- **简介**: 极简的任务驱动自主Agent
- **Star数**: 20k+
- **主要功能**: 任务生成、优先级排序、自主执行
- **适用场景**: 任务管理、自动化流程
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐ 概念验证项目

### 9. AgentGPT
- **GitHub链接**: https://github.com/reworkd/AgentGPT
- **简介**: 浏览器中运行的自主AI Agent
- **Star数**: 32k+
- **主要功能**: 网页界面、任务规划、自动执行
- **适用场景**: 快速原型、教育演示
- **技术栈**: TypeScript, Next.js
- **活跃度评估**: ⭐⭐⭐⭐ 活跃

### 10. Haystack
- **GitHub链接**: https://github.com/deepset-ai/haystack
- **简介**: 模块化NLP框架，支持RAG和Agent
- **Star数**: 20k+
- **主要功能**: 文档检索、问答系统、Agent管道
- **适用场景**: 企业搜索、知识库
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 企业级框架

### 11. LiteLLM
- **GitHub链接**: https://github.com/BerriAI/litellm
- **简介**: 统一多LLM API调用的代理层
- **Star数**: 16k+
- **主要功能**: 多模型统一接口、负载均衡、成本跟踪
- **适用场景**: 多模型管理、API代理
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 快速增长

### 12. PydanticAI
- **GitHub链接**: https://github.com/pydantic/pydantic-ai
- **简介**: Pydantic团队推出的类型安全Agent框架
- **Star数**: 8k+
- **主要功能**: 类型安全、结构化输出、依赖注入
- **适用场景**: 类型严格的Agent应用
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 新兴热门

### 13. AG2 (原AutoGen)
- **GitHub链接**: https://github.com/ag2ai/ag2
- **简介**: 微软研究院开发的多Agent对话框架
- **Star数**: 40k+
- **主要功能**: 多Agent对话、代码生成、工具使用
- **适用场景**: 代码生成、多角色协作
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 非常活跃，已独立运营

### 14. smolagents
- **GitHub链接**: https://github.com/huggingface/smolagents
- **简介**: HuggingFace推出的极简Agent框架
- **Star数**: 10k+
- **主要功能**: 代码Agent、工具调用、沙箱执行
- **适用场景**: 代码任务、安全执行
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ HF官方支持

### 15. Phidata
- **GitHub链接**: https://github.com/phidatahq/phidata
- **简介**: 构建具备记忆、知识和工具的AI助手
- **Star数**: 18k+
- **主要功能**: 知识库、记忆管理、多Agent
- **适用场景**: AI助手、客服系统
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 快速增长

---

## 二、编程Agent

### 16. OpenCode
- **GitHub链接**: https://github.com/opencode-ai/opencode
- **简介**: 开源终端AI编程助手，支持75+ LLM提供商
- **Star数**: 103k+
- **主要功能**: 代码生成、重构、调试、上下文感知
- **适用场景**: 终端编程、代码理解
- **技术栈**: TypeScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 极热门

### 17. Claude Code
- **GitHub链接**: https://github.com/anthropics/claude-code
- **简介**: Anthropic官方CLI编程助手
- **Star数**: 25k+
- **主要功能**: 命令行编程、代码编辑、项目理解
- **适用场景**: 终端开发、代码重构
- **技术栈**: TypeScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 官方维护

### 18. Devika
- **GitHub链接**: https://github.com/stitionai/devika
- **简介**: 开源AI软件工程师，模拟人类开发流程
- **Star数**: 19k+
- **主要功能**: 代码规划、实现、调试、文档
- **适用场景**: 端到端软件开发
- **技术栈**: Python, JavaScript
- **活跃度评估**: ⭐⭐⭐⭐ 较活跃

### 19. MetaGPT
- **GitHub链接**: https://github.com/geekan/MetaGPT
- **简介**: 多Agent协作编程框架，模拟软件公司
- **Star数**: 53k+
- **主要功能**: 角色分配、SOP流程、代码生成
- **适用场景**: 复杂软件开发、团队协作模拟
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 非常热门

### 20. ChatDev
- **GitHub链接**: https://github.com/OpenBMB/ChatDev
- **简介**: 虚拟软件公司的多Agent协作平台
- **Star数**: 26k+
- **主要功能**: 多角色对话、代码开发、评审优化
- **适用场景**: 教育、原型开发
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 学术背景

### 21. Aider
- **GitHub链接**: https://github.com/paul-gauthier/aider
- **简介**: 终端AI结对编程助手
- **Star数**: 35k+
- **主要功能**: 代码编辑、Git集成、多文件修改
- **适用场景**: 日常编程、代码审查
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 持续增长

### 22. Continue
- **GitHub链接**: https://github.com/continuedev/continue
- **简介**: IDE插件形式的AI编程助手
- **Star数**: 22k+
- **主要功能**: 代码补全、重构、解释、自动生成
- **适用场景**: IDE增强、日常开发
- **技术栈**: TypeScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 活跃

### 23. Tabby
- **GitHub链接**: https://github.com/TabbyML/tabby
- **简介**: 自托管AI代码助手
- **Star数**: 33k+
- **主要功能**: 代码补全、聊天、本地部署
- **适用场景**: 隐私优先的编程环境
- **技术栈**: Rust, Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 快速增长

### 24. Cody
- **GitHub链接**: https://github.com/sourcegraph/cody
- **简介**: Sourcegraph推出的AI编程助手
- **Star数**: 15k+
- **主要功能**: 代码搜索、补全、解释、重构
- **适用场景**: 大型代码库、企业开发
- **技术栈**: TypeScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 企业级

### 25. PearAI
- **GitHub链接**: https://github.com/trypear/pearai-app
- **简介**: 开源AI代码编辑器
- **Star数**: 8k+
- **主要功能**: AI辅助编程、代码生成、多模型支持
- **适用场景**: 开发者生产力提升
- **技术栈**: TypeScript
- **活跃度评估**: ⭐⭐⭐⭐ 新兴项目

### 26. Refact.ai
- **GitHub链接**: https://github.com/smallcloudai/refact
- **简介**: 自托管AI编码助手
- **Star数**: 4k+
- **主要功能**: 代码补全、聊天、模型微调
- **适用场景**: 私有化部署、数据安全
- **技术栈**: Python, Rust
- **活跃度评估**: ⭐⭐⭐⭐ 稳定更新

### 27. OpenHands (原OpenDevin)
- **GitHub链接**: https://github.com/All-Hands-AI/OpenHands
- **简介**: 开源AI软件开发助手
- **Star数**: 47k+
- **主要功能**: 代码生成、命令执行、Web浏览
- **适用场景**: 软件开发自动化
- **技术栈**: Python, TypeScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 极热门

### 28. Sweep
- **GitHub链接**: https://github.com/sweepai/sweep
- **简介**: AI驱动的GitHub Issue自动化解决工具
- **Star数**: 8k+
- **主要功能**: Issue分析、代码修改、PR生成
- **适用场景**: 开源项目维护
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐ 活跃

### 29. Bloop
- **GitHub链接**: https://github.com/BloopAI/bloop
- **简介**: 基于RAG的代码搜索引擎
- **Star数**: 12k+
- **主要功能**: 自然语言代码搜索、问答
- **适用场景**: 代码库理解、新成员上手
- **技术栈**: Rust
- **活跃度评估**: ⭐⭐⭐⭐ 稳定

### 30. GPT Pilot
- **GitHub链接**: https://github.com/Pythagora-io/gpt-pilot
- **简介**: 开发完整应用的AI开发者
- **Star数**: 32k+
- **主要功能**: 应用规划、代码生成、调试
- **适用场景**: 全栈应用开发
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 热门

---

## 三、RAG与知识库Agent

### 31. Dify
- **GitHub链接**: https://github.com/langgenius/dify
- **简介**: 开源LLM应用开发平台，支持工作流和Agent
- **Star数**: 85k+
- **主要功能**: 可视化编排、RAG、Agent、多模型
- **适用场景**: AI应用快速开发、知识库
- **技术栈**: Python, TypeScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 极热门

### 32. RAGFlow
- **GitHub链接**: https://github.com/infiniflow/ragflow
- **简介**: 基于深度文档理解的RAG引擎
- **Star数**: 45k+
- **主要功能**: 文档解析、向量检索、引用溯源
- **适用场景**: 企业知识库、文档问答
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 快速增长

### 33. QAnything
- **GitHub链接**: https://github.com/netease-youdao/QAnything
- **简介**: 网易有道开源的本地知识库问答系统
- **Star数**: 22k+
- **主要功能**: 文档上传、问答、本地部署
- **适用场景**: 本地知识库、隐私保护
- **技术栈**: Python, C++
- **活跃度评估**: ⭐⭐⭐⭐⭐ 国产优秀

### 34. FastGPT
- **GitHub链接**: https://github.com/labring/FastGPT
- **简介**: 基于LLM的知识库问答系统
- **Star数**: 24k+
- **主要功能**: 知识库构建、对话流编排、Agent
- **适用场景**: 客服系统、知识管理
- **技术栈**: TypeScript, Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 国内热门

### 35. MaxKB
- **GitHub链接**: https://github.com/1Panel-dev/MaxKB
- **简介**: 基于LLM的知识库问答系统
- **Star数**: 15k+
- **主要功能**: 知识库管理、模型对接、工作流
- **适用场景**: 企业知识管理、智能客服
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 活跃

### 36. DB-GPT
- **GitHub链接**: https://github.com/eosphoros-ai/DB-GPT
- **简介**: 数据库领域的AI Agent框架
- **Star数**: 15k+
- **主要功能**: 数据库问答、SQL生成、数据分析
- **适用场景**: 数据库管理、数据查询
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 专业领域

### 37. Quiver
- **GitHub链接**: https://github.com/StanGirard/quivr
- **简介**: 第二大脑工具，RAG个人知识管理
- **Star数**: 36k+
- **主要功能**: 文件上传、知识检索、多模态
- **适用场景**: 个人知识管理、笔记整理
- **技术栈**: Python, TypeScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 热门

### 38. AnythingLLM
- **GitHub链接**: https://github.com/Mintplex-Labs/anything-llm
- **简介**: 全栈私有文档聊天工具
- **Star数**: 42k+
- **主要功能**: 多文档支持、多用户、API接口
- **适用场景**: 团队知识库、私有部署
- **技术栈**: JavaScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 非常热门

### 39. PrivateGPT
- **GitHub链接**: https://github.com/imartinez/privategpt
- **简介**: 本地私有文档问答系统
- **Star数**: 57k+
- **主要功能**: 离线运行、文档索引、隐私保护
- **适用场景**: 敏感数据处理、隐私优先
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 隐私领域热门

### 40. LocalAI
- **GitHub链接**: https://github.com/mudler/LocalAI
- **简介**: 本地推理的OpenAI API替代品
- **Star数**: 31k+
- **主要功能**: 模型管理、API兼容、多后端
- **适用场景**: 本地部署、成本优化
- **技术栈**: Go
- **活跃度评估**: ⭐⭐⭐⭐⭐ 活跃

### 41. Cherry Studio
- **GitHub链接**: https://github.com/CherryHQ/cherry-studio
- **简介**: 支持多模型服务的桌面客户端
- **Star数**: 12k+
- **主要功能**: 多模型切换、知识库、MCP工具
- **适用场景**: 个人AI助手、多模型管理
- **技术栈**: TypeScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 快速增长

### 42. Open WebUI
- **GitHub链接**: https://github.com/open-webui/open-webui
- **简介**: 自托管的AI聊天平台
- **Star数**: 80k+
- **主要功能**: 多模型支持、RAG、多用户管理
- **适用场景**: 团队协作、知识共享
- **技术栈**: Svelte, Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 极热门

### 43. Lobe Chat
- **GitHub链接**: https://github.com/lobehub/lobe-chat
- **简介**: 现代化设计的开源AI聊天框架
- **Star数**: 55k+
- **主要功能**: 多模型、插件系统、多模态
- **适用场景**: AI应用界面、聊天机器人
- **技术栈**: TypeScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 设计优秀

### 44. LibreChat
- **GitHub链接**: https://github.com/danny-avila/LibreChat
- **简介**: 多模型AI聊天界面
- **Star数**: 24k+
- **主要功能**: 多模型支持、插件、多用户
- **适用场景**: ChatGPT替代、团队部署
- **技术栈**: JavaScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 活跃

### 45. One API
- **GitHub链接**: https://github.com/songquanpeng/one-api
- **简介**: 多LLM API聚合平台
- **Star数**: 24k+
- **主要功能**: 渠道管理、负载均衡、令牌管理
- **适用场景**: 多模型接入、成本控制
- **技术栈**: Go
- **活跃度评估**: ⭐⭐⭐⭐⭐ 国内热门

---

## 四、多Agent协作框架

### 46. Microsoft AutoGen
- **GitHub链接**: https://github.com/microsoft/autogen
- **简介**: 微软开源的多Agent对话编程框架
- **Star数**: 40k+
- **主要功能**: 多Agent对话、代码生成、工具使用
- **适用场景**: 复杂任务分解、团队协作模拟
- **技术栈**: Python, .NET
- **活跃度评估**: ⭐⭐⭐⭐⭐ 微软官方维护

### 47. CAMEL
- **GitHub链接**: https://github.com/camel-ai/camel
- **简介**: 大规模语言模型社会仿真的Agent框架
- **Star数**: 11k+
- **主要功能**: 角色扮演、社会模拟、协作学习
- **适用场景**: 社会研究、协作任务
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 学术研究背景

### 48. OpenManus
- **GitHub链接**: https://github.com/mannaandpoem/OpenManus
- **简介**: 开源通用AI Agent框架
- **Star数**: 40k+
- **主要功能**: 工具调用、任务规划、多Agent
- **适用场景**: 通用自动化、研究探索
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 快速增长

### 49. ANUS
- **GitHub链接**: https://github.com/nikmcfly/ANUS
- **简介**: AI任务自动化与多Agent协作框架
- **Star数**: 5k+
- **主要功能**: 任务分解、多Agent协作、工具集成
- **适用场景**: 复杂任务自动化
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐ 新兴项目

### 50. DSPy
- **GitHub链接**: https://github.com/stanfordnlp/dspy
- **简介**: 斯坦福NLP的LLM编程框架
- **Star数**: 23k+
- **主要功能**: 提示优化、模块化编程、自动调优
- **适用场景**: 算法优化、提示工程
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 学术界热门

### 51. ControlFlow
- **GitHub链接**: https://github.com/PrefectHQ/ControlFlow
- **简介**: Prefect推出的Agent工作流框架
- **Star数**: 7k+
- **主要功能**: 工作流编排、Agent任务、状态管理
- **适用场景**: 数据工作流、AI管道
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐ 稳步增长

### 52. PraisonAI
- **GitHub链接**: https://github.com/MervinPraison/PraisonAI
- **简介**: 自包含的AutoAI框架
- **Star数**: 5k+
- **主要功能**: Agent创建、任务编排、UI界面
- **适用场景**: AI工作流、自动化
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐ 活跃

### 53. Taskweaver
- **GitHub链接**: https://github.com/microsoft/taskweaver
- **简介**: 微软开源的代码优先Agent框架
- **Star数**: 14k+
- **主要功能**: 代码生成、数据分析、插件系统
- **适用场景**: 数据分析、代码任务
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 微软官方

### 54. Magentic-One
- **GitHub链接**: https://github.com/microsoft/autogen/tree/main/python/packages/autogen-magentic-one
- **简介**: 微软AutoGen的多Agent办公助手
- **Star数**: 整合在AutoGen中
- **主要功能**: 多Agent协作、办公自动化、Web浏览
- **适用场景**: 办公任务自动化
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 微软最新项目

### 55. PyAutoGUI Agent
- **GitHub链接**: https://github.com/AI-Engineer-Foundation/agent-protocol
- **简介**: 控制GUI的AI Agent
- **Star数**: 3k+
- **主要功能**: GUI自动化、屏幕识别、操作控制
- **适用场景**: 桌面自动化、RPA
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐ 专业领域

---

## 五、自动化与工作流Agent

### 56. n8n
- **GitHub链接**: https://github.com/n8n-io/n8n
- **简介**: 开源工作流自动化平台，支持AI Agent节点
- **Star数**: 68k+
- **主要功能**: 可视化工作流、400+集成、AI节点
- **适用场景**: 业务流程自动化、数据集成
- **技术栈**: TypeScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 极热门

### 57. Flowise
- **GitHub链接**: https://github.com/FlowiseAI/Flowise
- **简介**: 可视化构建LLM工作流的低代码工具
- **Star数**: 40k+
- **主要功能**: 拖拽界面、多模型支持、Agent构建
- **适用场景**: 无代码AI应用开发
- **技术栈**: TypeScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 热门

### 58. ComfyUI
- **GitHub链接**: https://github.com/comfyanonymous/ComfyUI
- **简介**: 节点式Stable Diffusion GUI
- **Star数**: 75k+
- **主要功能**: 可视化工作流、图像生成、自定义节点
- **适用场景**: AI图像生成、工作流设计
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 极热门

### 59. dify-sandbox
- **GitHub链接**: https://github.com/langgenius/dify-sandbox
- **简介**: Dify的代码执行沙箱
- **Star数**: 整合在Dify中
- **主要功能**: 安全代码执行、多语言支持
- **适用场景**: AI代码执行环境
- **技术栈**: Go
- **活跃度评估**: ⭐⭐⭐⭐⭐ 活跃

### 60. Huginn
- **GitHub链接**: https://github.com/huginn/huginn
- **简介**: 创建自动化任务的Agent系统
- **Star数**: 44k+
- **主要功能**: 事件监控、自动化响应、数据抓取
- **适用场景**: 个人自动化、监控告警
- **技术栈**: Ruby
- **活跃度评估**: ⭐⭐⭐⭐ 经典项目

### 61. Activepieces
- **GitHub链接**: https://github.com/activepieces/activepieces
- **简介**: 开源自动化工具，Zapier替代品
- **Star数**: 14k+
- **主要功能**: 工作流自动化、多集成、自托管
- **适用场景**: 业务自动化、流程集成
- **技术栈**: TypeScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 快速增长

### 62. Windmill
- **GitHub链接**: https://github.com/windmill-labs/windmill
- **简介**: 开源工作流引擎和脚本平台
- **Star数**: 12k+
- **主要功能**: 脚本执行、工作流编排、低代码
- **适用场景**: 内部工具、数据管道
- **技术栈**: Rust, TypeScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 活跃

### 63. Node-RED
- **GitHub链接**: https://github.com/node-red/node-red
- **简介**: 基于Node.js的可视化编程工具
- **Star数**: 20k+
- **主要功能**: 流编程、IoT集成、自动化
- **适用场景**: IoT、自动化流程
- **技术栈**: Node.js
- **活跃度评估**: ⭐⭐⭐⭐ 稳定维护

### 64. Temporal
- **GitHub链接**: https://github.com/temporalio/temporal
- **简介**: 微服务编排平台
- **Star数**: 12k+
- **主要功能**: 工作流编排、故障恢复、状态管理
- **适用场景**: 微服务、长期运行工作流
- **技术栈**: Go
- **活跃度评估**: ⭐⭐⭐⭐⭐ 企业级

### 65. Prefect
- **GitHub链接**: https://github.com/PrefectHQ/prefect
- **简介**: 现代数据工作流编排
- **Star数**: 18k+
- **主要功能**: 数据管道、监控、调度
- **适用场景**: 数据工程、ETL流程
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 活跃

---

## 六、数据分析Agent

### 66. Chat2DB
- **GitHub链接**: https://github.com/chat2db/Chat2DB
- **简介**: 智能数据库客户端和数据分析工具
- **Star数**: 22k+
- **主要功能**: 自然语言SQL、数据可视化、AI分析
- **适用场景**: 数据库管理、数据分析
- **技术栈**: Java
- **活跃度评估**: ⭐⭐⭐⭐⭐ 国产优秀

### 67. Vanna
- **GitHub链接**: https://github.com/vanna-ai/vanna
- **简介**: SQL生成的RAG框架
- **Star数**: 15k+
- **主要功能**: 自然语言转SQL、训练自定义模型
- **适用场景**: 数据查询、报表生成
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 热门

### 68. DataGPT
- **GitHub链接**: https://github.com/databutton/databutton
- **简介**: 数据分析AI助手
- **Star数**: 8k+
- **主要功能**: 数据探索、可视化、报告生成
- **适用场景**: 数据分析、业务智能
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐ 活跃

### 69. PandasAI
- **GitHub链接**: https://github.com/Sinaptik-AI/pandas-ai
- **简介**: 对话式数据分析工具
- **Star数**: 19k+
- **主要功能**: 自然语言数据分析、图表生成
- **适用场景**: 数据分析、探索性分析
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 热门

### 70. Langchain-extract
- **GitHub链接**: https://github.com/langchain-ai/langchain-extract
- **简介**: 文档信息提取工具
- **Star数**: 2k+
- **主要功能**: 结构化提取、API服务
- **适用场景**: 文档处理、数据提取
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐ 新兴

### 71. LlamaParse
- **GitHub链接**: https://github.com/run-llama/llama_parse
- **简介**: LlamaIndex的文档解析服务
- **Star数**: 5k+
- **主要功能**: PDF解析、表格提取、结构化输出
- **适用场景**: 文档分析、知识库构建
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 专业工具

### 72. Docling
- **GitHub链接**: https://github.com/DS4SD/docling
- **简介**: 文档理解和转换工具
- **Star数**: 25k+
- **主要功能**: 多格式文档解析、AI理解
- **适用场景**: 文档处理、数据提取
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ IBM背书

### 73. Unstructured
- **GitHub链接**: https://github.com/Unstructured-IO/unstructured
- **简介**: 非结构化数据预处理工具
- **Star数**: 11k+
- **主要功能**: 文档解析、元素提取、清洗转换
- **适用场景**: 数据预处理、RAG准备
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 行业标准

### 74. Marker
- **GitHub链接**: https://github.com/VikParuchuri/marker
- **简介**: PDF转Markdown工具
- **Star数**: 23k+
- **主要功能**: 高精度PDF转换、公式识别
- **适用场景**: 文档数字化、知识库构建
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 快速增长

### 75. GPT Researcher
- **GitHub链接**: https://github.com/assafelovic/gpt-researcher
- **简介**: 自主研究报告生成Agent
- **Star数**: 19k+
- **主要功能**: 网络搜索、报告撰写、多源整合
- **适用场景**: 研究分析、信息收集
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 热门

---

## 七、垂直领域Agent

### 76. SWE-agent
- **GitHub链接**: https://github.com/princeton-nlp/SWE-agent
- **简介**: 自动修复GitHub Issue的Agent
- **Star数**: 20k+
- **主要功能**: 代码修复、Issue分析、PR生成
- **适用场景**: 软件维护、Bug修复
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 普林斯顿NLP

### 77. BioGPT
- **GitHub链接**: https://github.com/microsoft/BioGPT
- **简介**: 生物医学领域语言模型
- **Star数**: 8k+
- **主要功能**: 生物医学文本理解、问答
- **适用场景**: 生物医药研究
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐ 微软官方

### 78. ChemCrow
- **GitHub链接**: https://github.com/ur-whitelab/chemcrow
- **简介**: 化学领域的AI Agent
- **Star数**: 3k+
- **主要功能**: 化学计算、文献检索、分子设计
- **适用场景**: 化学研究、药物发现
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐ 学术项目

### 79. Voyager
- **GitHub链接**: https://github.com/MineDojo/Voyager
- **简介**: Minecraft中的终身学习Agent
- **Star数**: 6k+
- **主要功能**: 游戏内学习、技能获取、代码生成
- **适用场景**: 强化学习研究、AI智能体
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐ 研究项目

### 80. OSWorld
- **GitHub链接**: https://github.com/xlang-ai/OSWorld
- **简介**: 操作系统环境的GUI Agent基准
- **Star数**: 4k+
- **主要功能**: GUI操作、任务执行、评测
- **适用场景**: GUI Agent研究、自动化测试
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐ 学术背景

### 81. Browser-use
- **GitHub链接**: https://github.com/browser-use/browser-use
- **简介**: 让LLM控制浏览器
- **Star数**: 15k+
- **主要功能**: 网页自动化、数据抓取、浏览器控制
- **适用场景**: 网络爬虫、自动化测试
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 快速增长

### 82. Skyvern
- **GitHub链接**: https://github.com/Skyvern-AI/skyvern
- **简介**: 浏览器自动化工作流
- **Star数**: 12k+
- **主要功能**: 可视化工作流、浏览器自动化
- **适用场景**: 数据抓取、表单填写
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 活跃

### 83. ScrapeGraphAI
- **GitHub链接**: https://github.com/ScrapeGraphAI/Scrapegraph-ai
- **简介**: 基于LLM的网络爬虫
- **Star数**: 22k+
- **主要功能**: 智能解析、数据提取、多语言支持
- **适用场景**: 数据采集、内容抓取
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 热门

### 84. Crawl4AI
- **GitHub链接**: https://github.com/unclecode/crawl4ai
- **简介**: 为AI应用优化的异步爬虫
- **Star数**: 35k+
- **主要功能**: 异步抓取、数据清洗、LLM优化
- **适用场景**: AI数据收集、RAG数据准备
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 极热门

### 85. MediaCrawler
- **GitHub链接**: https://github.com/NanmiCoder/MediaCrawler
- **简介**: 社交媒体爬虫工具
- **Star数**: 32k+
- **主要功能**: 多平台爬取、数据导出、关键词搜索
- **适用场景**: 舆情监控、数据分析
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 国内热门

### 86. AutoRAG
- **GitHub链接**: https://github.com/Marker-Inc-Korea/AutoRAG
- **简介**: RAG自动化优化框架
- **Star数**: 4k+
- **主要功能**: 自动调优、策略搜索、评估
- **适用场景**: RAG系统优化
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐ 新兴

### 87. LATS
- **GitHub链接**: https://github.com/lmt-trade/lats
- **简介**: 交易领域的Agent系统
- **Star数**: 2k+
- **主要功能**: 量化交易、策略执行、风险管理
- **适用场景**: 金融交易、量化投资
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐ 专业领域

### 88. DevOpsGPT
- **GitHub链接**: https://github.com/kuafuai/DevOpsGPT
- **简介**: DevOps领域的AI助手
- **Star数**: 7k+
- **主要功能**: 自动化部署、运维管理、故障排查
- **适用场景**: DevOps自动化、运维管理
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐ 实用工具

---

## 八、Agent开发工具与平台

### 89. Coze
- **GitHub链接**: https://github.com/coze-dev/coze-js
- **简介**: 字节跳动推出的AI Bot开发平台
- **Star数**: 3k+
- **主要功能**: Bot开发、工作流、插件系统
- **适用场景**: 聊天机器人、AI应用
- **技术栈**: TypeScript
- **活跃度评估**: ⭐⭐⭐⭐ 字节支持

### 90. FastAPI
- **GitHub链接**: https://github.com/fastapi/fastapi
- **简介**: 高性能Python Web框架，常用于Agent服务
- **Star数**: 82k+
- **主要功能**: API开发、异步支持、自动文档
- **适用场景**: Agent服务部署
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 行业标准

### 91. Chainlit
- **GitHub链接**: https://github.com/Chainlit/chainlit
- **简介**: 快速构建对话式AI界面
- **Star数**: 9k+
- **主要功能**: 聊天界面、多步对话、数据可视化
- **适用场景**: Agent演示界面、聊天应用
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 活跃

### 92. Gradio
- **GitHub链接**: https://github.com/gradio-app/gradio
- **简介**: 快速构建ML演示界面
- **Star数**: 37k+
- **主要功能**: 界面构建、多模态、部署分享
- **适用场景**: 模型演示、原型开发
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ HuggingFace官方

### 93. Streamlit
- **GitHub链接**: https://github.com/streamlit/streamlit
- **简介**: 数据应用快速开发框架
- **Star数**: 38k+
- **主要功能**: 数据可视化、交互组件、快速部署
- **适用场景**: 数据应用、AI界面
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 广泛流行

### 94. Prompt flow
- **GitHub链接**: https://github.com/microsoft/promptflow
- **简介**: 微软的LLM应用开发工具
- **Star数**: 10k+
- **主要功能**: 提示管理、工作流编排、评估
- **适用场景**: LLM应用开发、提示工程
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 微软官方

### 95. AgentScope
- **GitHub链接**: https://github.com/modelscope/agentscope
- **简介**: 阿里ModelScope的多Agent平台
- **Star数**: 6k+
- **主要功能**: Agent构建、多模态、分布式
- **适用场景**: 多Agent应用、团队协作
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 阿里支持

### 96. ModelScope
- **GitHub链接**: https://github.com/modelscope/modelscope
- **简介**: 阿里开源模型平台，提供Agent能力
- **Star数**: 9k+
- **主要功能**: 模型库、推理部署、Agent框架
- **适用场景**: 模型应用、AI开发
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 国内主流

### 97. Xinference
- **GitHub链接**: https://github.com/xorbitsai/inference
- **简介**: 模型推理平台，支持多种开源模型
- **Star数**: 7k+
- **主要功能**: 模型部署、API服务、多后端
- **适用场景**: 模型推理服务、Agent后端
- **技术栈**: Python
- **活跃度评估**: ⭐⭐⭐⭐⭐ 活跃

### 98. Ollama
- **GitHub链接**: https://github.com/ollama/ollama
- **简介**: 本地运行大模型的工具
- **Star数**: 135k+
- **主要功能**: 模型管理、本地推理、OpenAI兼容API
- **适用场景**: 本地开发、隐私保护
- **技术栈**: Go
- **活跃度评估**: ⭐⭐⭐⭐⭐ 极热门

### 99. LM Studio
- **GitHub链接**: https://github.com/lmstudio-ai/lms
- **简介**: 桌面LLM应用和模型管理
- **Star数**: 10k+
- **主要功能**: 模型下载、本地推理、API服务
- **适用场景**: 本地开发、模型测试
- **技术栈**: TypeScript
- **活跃度评估**: ⭐⭐⭐⭐⭐ 热门工具

### 100. vLLM
- **GitHub链接**: https://github.com/vllm-project/vllm
- **简介**: 高吞吐量LLM推理引擎
- **Star数**: 43k+
- **主要功能**: PagedAttention、高并发、多模型
- **适用场景**: 生产环境推理、Agent后端
- **技术栈**: Python, C++
- **活跃度评估**: ⭐⭐⭐⭐⭐ 工业标准

---

## 📊 汇总统计

| 类别 | 项目数量 | 平均Star数 |
|------|----------|------------|
| 通用Agent框架 | 15 | 35k+ |
| 编程Agent | 15 | 28k+ |
| RAG与知识库Agent | 15 | 32k+ |
| 多Agent协作框架 | 10 | 17k+ |
| 自动化与工作流Agent | 10 | 31k+ |
| 数据分析Agent | 10 | 15k+ |
| 垂直领域Agent | 13 | 11k+ |
| Agent开发工具与平台 | 12 | 32k+ |

---

## 🔍 如何选择

### 新手入门推荐
1. **编程Agent**: OpenCode, Claude Code
2. **知识库**: Dify, FastGPT, AnythingLLM
3. **学习框架**: CrewAI, smolagents

### 企业级应用推荐
1. **通用框架**: LangChain, Semantic Kernel, LlamaIndex
2. **多Agent**: AutoGen, CrewAI, MetaGPT
3. **工作流**: n8n, Flowise, Dify

### 本地/隐私优先推荐
1. **本地模型**: Ollama, vLLM, LocalAI
2. **知识库**: PrivateGPT, QAnything
3. **编程**: Tabby, Aider

---

## 📌 注意事项

1. **Star数仅供参考**: 随时间变化，请以GitHub实际数据为准
2. **活跃度评估**: 基于近期提交频率和社区活跃度
3. **技术栈**: 主要开发语言，实际可能包含多种技术
4. **适用场景**: 基于项目文档和社区反馈总结

---

*本文档由AI整理生成，如有遗漏或错误，欢迎补充指正*
