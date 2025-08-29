# ♾️ Research Assistant Agent

> **🧠 Motivation**<br>
> Have a **complex** topic for a deep search?<br>
> Have **no time** managing multiple online sources?<br>
> Want **minimal** search efforts?<br>
> Search report redaction in a **minute**?<br>
> Check this out! 👇

A **multi-agent** AI research assistant that automates deep research using artificial `analysts` and `experts`. It simulates a team of domain analysts conducting **interviews** with virtual domain experts to produce a consolidated report on the given topic.

### ♾️ WorkFlow

1. User provides a research topic and specifies the number of analysts.
2. Generates a set of virtual analysts studying the topic.
3. Each analyst conducts interviews with a virtual expert in that topic.
4. The findings from each analyst are synthesized into a final report.

### ♾️ Project Architecture

- We used `LangGraph` to orchestrate the team of analysts and their interviews.
- The core logic follows a map-reduce pattern, where analysts independently interview the experts in parallel in the "map" phase, then synthesize their individual findings into a single, comprehensive report in the "reduce" phase.
- The entire process is powered by `Anthropic`'s language models.

`Graph`<br>
![workflow-graph](https://raw.githubusercontent.com/yassermessahli/research-assistant/refs/heads/main/static/images/graph.png)

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

`LangGraph Studio`<br>
![langgraph-studio](https://raw.githubusercontent.com/yassermessahli/research-assistant/refs/heads/main/static/images/studio.png)

I will appreciate

- Your feedback
- Your Contribution

#### Happy Researching! 🧐
