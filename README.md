# ♾️ Intellex

> Intellex is a **multi-agent** AI research assistant that turns complex topics into clear, consolidated research reports. 

> It automates deep research with artificial `analysts` and `experts`. It simulates a team of domain analysts conducting **interviews** with virtual domain experts to produce a consolidated Markdown report on the given topic.

<br>

![langgraph-studio](https://raw.githubusercontent.com/yassermessahli/research-assistant/refs/heads/main/static/images/studio.png)

### ♾️ Features
- **Parallel virtual analysts** simulated with Anthropic models
- **Expert interviews** orchestration powered by LangGraph
- **Markdown-ready final reports**  
- Want to try? just **Plug-and-play** 

### ♾️ WorkFlow

1. Provide a research topic + number of analysts.  
2. Intellex spawns analysts who each interview an expert.  
3. Each analyst produces a mini-report.  
4. Reports are merged into one consolidated Markdown file.  

![workflow-graph](https://raw.githubusercontent.com/yassermessahli/research-assistant/refs/heads/main/static/images/graph.png)

### ♾️ Project Architecture

- Using `LangGraph` to orchestrate the team of analysts and their interviews.
- The core logic follows a Map-Reduce pattern, where analysts independently interview the experts in parallel in the "map" phase, then synthesize their individual findings into a single, comprehensive report in the "reduce" phase.
- The entire process is powered by `Anthropic`'s language models.

## ♾️ Quickstart

**Prerequisites**

- Python 3.11+ (python 3.13 recommended)
- `uv` installed (`pip install uv`)

Follow these simple steps to get the project running locally.

1. Clone the repository

```bash
git clone https://github.com/your-username/research-assistant.git
cd research-assistant
```

2. Sync the project with original project dependencies and versions

```bash
# just run this simple command and you've done!
uv sync
```

3. Create a `.env` file from `env.example` in the project root and add your API keys.

4. Start the LangGraph studio to interact with the agent.

```bash
cd agent/
langgraph dev
```

5. Once the server is running, the **LangGraph Studio** WebUI will open in the browser, and you can interact with it.

## 🤝 Contributing

Feedback and PRs are welcome! Please open an issue before major changes. I am still working on it.

**Happy Researching!** 🔍
