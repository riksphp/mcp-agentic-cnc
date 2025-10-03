# MCP Agentic Calculator with Canvas Visualization

An intelligent agentic system that solves mathematical problems using the Model Context Protocol (MCP) and visualizes results on a canvas using macOS Preview.

## 🎯 What It Does

This project demonstrates an **agentic AI workflow** where:

1. An LLM agent (Gemini 2.0 Flash) receives a mathematical problem
2. The agent autonomously decides which tools to call and in what order
3. Multiple function calls are executed in iterations until the solution is found
4. The final answer is displayed on a canvas with a rectangle and text annotation

### Example Task

**Query:** "Find the ASCII values of characters in INDIA and then return sum of exponentials of those values."

**Agent Workflow:**

1. Calls `strings_to_chars_to_int("INDIA")` → Returns `[73, 78, 68, 73, 65]`
2. Calls `int_list_to_exponential_sum([73, 78, 68, 73, 65])` → Returns sum
3. Returns `FINAL_ANSWER: [7.59982224609308e+33]`
4. Visualizes the result on a canvas

---

## 🏗️ Architecture

```
┌─────────────────────┐
│   talk2mcp.py       │  ← Main client (orchestrates agent)
│   (MCP Client)      │
└──────────┬──────────┘
           │
           │ STDIO Communication
           │
┌──────────▼─────────────────────┐
│  example_macp_server_mac.py    │  ← MCP Server
│  (Exposes Tools)               │
├────────────────────────────────┤
│  Math Tools:                   │
│  - add, subtract, multiply     │
│  - strings_to_chars_to_int     │
│  - int_list_to_exponential_sum │
│  - factorial, log, sin, cos    │
│  - fibonacci_numbers, etc.     │
├────────────────────────────────┤
│  Canvas Tools:                 │
│  - open_canvas()               │
│  - draw_rectangle()            │
│  - add_text_in_paint()         │
│  - refresh_canvas()            │
└────────────────────────────────┘
           │
           │ Uses PIL & subprocess
           │
┌──────────▼──────────┐
│  macOS Preview      │  ← Visual Output
│  (Canvas Display)   │
└─────────────────────┘
```

---

## 📋 Prerequisites

- **Python 3.8+**
- **macOS** (uses Preview for canvas visualization)
- **Gemini API Key** (for LLM agent)

---

## 🚀 Setup

### 1. Create Virtual Environment

```bash
cd /Users/rishikesh.kumar/Desktop/EAGV2/mcp-agentic-cnc
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install python-dotenv google-genai mcp pillow uvloop pyautogui
```

### 3. Create `.env` File

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your API key from: https://aistudio.google.com/app/apikey

---

## 🎮 Usage

### Run the Agent

```bash
source .venv/bin/activate
python talk2mcp.py
```

### What Happens:

1. **MCP Server starts** - Exposes math and canvas tools
2. **LLM Agent receives task** - "Find ASCII values of INDIA and sum exponentials"
3. **Iterative execution** - Agent calls functions autonomously:
   - Iteration 1: Converts "INDIA" to ASCII values
   - Iteration 2: Calculates exponential sum
   - Iteration 3: Returns FINAL_ANSWER
4. **Canvas visualization**:
   - Opens blank canvas in Preview
   - Draws rectangle
   - Adds final answer text inside rectangle
   - Refreshes canvas to show result

---

## 🛠️ Key Components

### `talk2mcp.py` - MCP Client & Agent Orchestrator

- Connects to MCP server via STDIO
- Sends prompts to Gemini LLM
- Parses agent responses (`FUNCTION_CALL:` or `FINAL_ANSWER:`)
- Calls appropriate MCP tools
- Handles iterative execution (max 5 iterations)

### `example_macp_server_mac.py` - MCP Server

- **Math Tools**: Arithmetic, trigonometry, string operations
- **Canvas Tools**: Create and manipulate visual canvas
- Uses FastMCP for easy tool registration
- Runs on STDIO transport for direct client communication

---

## 🔧 Configuration

### Adjust Max Iterations

In `talk2mcp.py` (line 17):

```python
max_iterations = 5  # Change as needed
```

### Change Canvas Dimensions

In `talk2mcp.py` (lines 287-290):

```python
"x1": 100,  # Top-left X
"y1": 100,  # Top-left Y
"x2": 600,  # Bottom-right X
"y2": 200   # Bottom-right Y
```

### Modify LLM Model

In `talk2mcp.py` (line 32):

```python
model="gemini-2.0-flash"  # Change to other Gemini models
```

---

## 🧪 Example Output

```
Starting main execution...
Establishing connection to MCP server...
Session created, initializing...
Successfully retrieved 20 tools

--- Iteration 1 ---
LLM Response: FUNCTION_CALL: strings_to_chars_to_int|INDIA
Called: strings_to_chars_to_int with {'string': 'INDIA'}
Result: [73, 78, 68, 73, 65]

--- Iteration 2 ---
LLM Response: FUNCTION_CALL: int_list_to_exponential_sum|73,78,68,73,65
Called: int_list_to_exponential_sum
Result: 7.59982224609308e+33

--- Iteration 3 ---
LLM Response: FINAL_ANSWER: [7.59982224609308e+33]

=== Agent Execution Complete ===
Step 1: Opening canvas...
Step 2: Drawing rectangle...
Step 3: Adding text inside rectangle...
Step 4: Refreshing canvas in Preview...

=== Canvas creation complete! ===
```

---

## 📂 Project Structure

```
mcp-agentic-cnc/
├── talk2mcp.py                  # MCP client & agent orchestrator
├── example_macp_server_mac.py   # MCP server with tools
├── .env                         # API keys (gitignored)
├── .gitignore                   # Git ignore file
├── .venv/                       # Virtual environment
└── README.md                    # This file
```

---

## 🔍 How It Works

### 1. Agent Decision Making

The LLM agent receives a structured prompt with:

- Available tools and their signatures
- Current task/query
- Previous iteration results
- Response format instructions

### 2. Iterative Execution

```
┌─────────────────────────────────┐
│  User Query                     │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  LLM decides next action        │
│  Returns: FUNCTION_CALL or      │
│           FINAL_ANSWER           │
└────────────┬────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────┐    ┌──────────────┐
│Function │    │ FINAL_ANSWER │
│Call     │    │ → Visualize  │
└────┬────┘    └──────────────┘
     │
     ▼
┌─────────────────────┐
│ Execute & Return    │
│ Add to context      │
└────────┬────────────┘
         │
         └──────► (Loop back)
```

### 3. Canvas Visualization

- Uses PIL (Python Imaging Library) to draw on canvas
- Saves to `/tmp/mcp_canvas.png`
- Opens in macOS Preview
- Refresh updates the preview without closing

---

## 🎨 Available Math Tools

- `add`, `subtract`, `multiply`, `divide`
- `power`, `sqrt`, `cbrt`
- `sin`, `cos`, `tan`
- `log`, `factorial`
- `strings_to_chars_to_int` - Convert string to ASCII values
- `int_list_to_exponential_sum` - Sum of e^x for each x
- `fibonacci_numbers` - Generate Fibonacci sequence

---

## 🐛 Troubleshooting

### Issue: "Import mcp could not be resolved"

**Solution:** Make sure virtual environment is activated:

```bash
source .venv/bin/activate
pip install mcp
```

### Issue: Canvas doesn't appear

**Solution:** Check that you're on macOS and Preview is available:

```bash
which open  # Should return /usr/bin/open
```

### Issue: LLM not responding

**Solution:** Verify your Gemini API key in `.env`:

```bash
cat .env  # Should show GEMINI_API_KEY=...
```

---

## 📝 License

This is an educational project for learning MCP and agentic AI workflows.

---

## 🙏 Acknowledgments

- **Model Context Protocol (MCP)** by Anthropic
- **Google Gemini** for LLM capabilities
- **FastMCP** for easy MCP server creation

---

## 📧 Contact

For questions or issues, please refer to the course materials or instructor.
