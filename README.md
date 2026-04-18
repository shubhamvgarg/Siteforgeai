# SiteForge AI

SiteForge AI is a Streamlit-based project builder powered by a custom LangGraph agent. Enter a project idea, then watch the app run the agent and display live execution logs plus the final agent result.

## Features

- Interactive **Streamlit UI** for prompt entry
- Live agent output logging during generation
- Final agent result displayed in the app
- Built with **LangGraph**, **LangChain**, and **Groq**

## Project Structure

- `app.py` - main Streamlit app and orchestration logic
- `requirements.txt` - Python dependencies
- `agent/` - custom agent implementation and supporting modules
  - `graph.py`
  - `nodes.py`
  - `prompts.py`
  - `states.py`
  - `tools.py`

## Getting Started

1. Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your Groq API credentials (required):

- Create a paid Groq account and get your API key.
- Create a `.env` file in the project root.
- Add your API key to `.env`.

```env
GROQ_API_KEY=your_paid_groq_api_key_here
```

4. Run the Streamlit app:

```bash
streamlit run app.py
```

5. Open the local Streamlit URL shown in the terminal.

## Configuration

This project uses `langchain_groq` and loads environment variables from a `.env` file via `python-dotenv`.

Required environment variable:

- `GROQ_API_KEY` — your paid Groq API key.

Optional environment variables:

- `GROQ_BASE_URL` — custom Groq API base URL if you are using a non-default endpoint.

## Usage

- Enter a clear project idea in the input box.
- Click **Build Project**.
- Watch the live agent log output while the model runs.
- View the final agent result inside the app once generation completes.

## Notes

- The app captures both `stdout` and `stderr` from the agent and streams it to the UI.
- Use **Start New Build** to reset the interface and run a new prompt.

## License

This project does not include a license file. Add one if you want to open source or share the code with others.

## Here is one example of generated app in "generated_project"

<img width="1861" height="506" alt="image" src="https://github.com/user-attachments/assets/e70e13d3-d8cf-4122-a092-357a6651aec4" />

## After giving inputs

<img width="1856" height="615" alt="image" src="https://github.com/user-attachments/assets/3c89c0b0-0212-4f4b-be11-2bc6eba65ebb" />

