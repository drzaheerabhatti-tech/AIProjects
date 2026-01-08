# Cohere Demos

Hands-on demos exploring the Cohere platform (Chat, embeddings, rerank, RAG).  
These examples are intentionally small and focused, designed for learning and discussion.

---

## Quickstart

### 1) Prerequisites
- Python 3.10+ recommended
- A Cohere API key (from the Cohere dashboard)

> ✅ Never commit secrets. `.env` files are gitignored.

---

### 2) Create and activate a virtual environment

```powershell
Windows:
cd AIProjects
python -m venv .venv
.\.venv\Scripts\Activate

Linux/macOS (bash/zsh)
cd AIProjects
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies
```
pip install cohere
(Optional sanity check)
python -c "import cohere; print(cohere.__version__)"
Set your Cohere API key
The demos read the API key from the environment variable:

COHERE_API_KEY

Option A (recommended): set an environment variable
Windows (PowerShell) — persistent
powershell

setx COHERE_API_KEY "YOUR_KEY_HERE"

Close and re-open PowerShell, then verify:

powershell
echo $env:COHERE_API_KEY
Windows (PowerShell) — current session only
powershell
$env:COHERE_API_KEY="YOUR_KEY_HERE"
Linux/macOS — current session only
export COHERE_API_KEY="YOUR_KEY_HERE"
(Optional) make it persistent by adding the export line to ~/.bashrc or ~/.zshrc.

Option B: .env file (local only)
You may keep a local .env file for convenience, but it should remain uncommitted.

Example .env (do not commit):

env
Copy code
COHERE_API_KEY=YOUR_KEY_HERE
Note: the provided scripts use os.getenv(...). If you want Python to load .env automatically, install python-dotenv and load it explicitly (optional enhancement).
```
### 4) Run the first demo
```Hello Cohere (Chat API)
python cohere-demos/basics/hello_cohere.py
This demo uses Cohere’s Chat API and prints the assistant’s response by parsing structured content blocks.

Customizing the demo
Open:

cohere-demos/basics/hello_cohere.py

You can adjust:

1) The user message (prompt)
Update the messages list:

messages=[
  {"role": "user", "content": "Explain TLS in simple terms."}
]

2) Token limit (max_tokens)
Controls the maximum length of the model output.

max_tokens=200
If output seems cut off, increase it.

3) Model
Use a supported model ID (snapshot models recommended). Example:

model="command-a-03-2025"
If you get a 404 model error, check Cohere’s current model catalog and update the ID.
```
### 5) Notes & troubleshooting
```Response structure: content blocks
Cohere Chat responses return structured content items:

response.message.content is a list of content blocks

text content is typically available via block.text

That’s why the demo extracts text by iterating blocks and concatenating text.
```

### 6) Friction log
```
Development notes, API changes, and setup friction are captured here:

cohere-demos/basics/notes/friction_log.md
```
