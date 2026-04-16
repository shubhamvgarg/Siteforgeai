# SiteForge AI

## Description
SiteForge AI is an AI-powered tool for generating website requirements based on user input. This project is in its initial development stage and uses LangGraph and LangChain to analyze user ideas and produce structured requirements for website creation.

## Installation
1. Clone the repository.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables (e.g., API keys for NVIDIA AI endpoints) in a `.env` file.

## Usage
Run the main graph to analyze user input:
```python
from graph import build_graph

app_graph = build_graph()
user_input = "Describe your website idea here."
result = app_graph.invoke({"user_input": user_input})
print(result['requirements'])
```

## Requirements
- Python 3.x
- Dependencies listed in `requirements.txt`

## Current Status
This project is in its initial state. Core functionality includes input analysis and requirements generation. Future updates will expand features and improve the system.

## Contributing
Contributions are welcome. Please submit issues or pull requests for improvements.
