# MCP Agentic Calculator with Optional Canvas Visualization

An intelligent agentic system that solves mathematical problems using the Model Context Protocol (MCP) and optionally visualizes results on a canvas using macOS Preview.

## ⭐ Key Highlights

- 🤖 **Truly Autonomous Agent** - Zero hardcoded logic, agent makes ALL decisions
- 🎨 **Conditional Visualization** - Agent detects if user wants visual output
- 🛠️ **24 MCP Tools** - Math operations + Canvas drawing capabilities
- 🔄 **Iterative Workflow** - Agent chains function calls intelligently
- 🎯 **PIL-based Drawing** - Programmatic image generation (no GUI automation)
- ⚡ **Fast & Reliable** - Optimized canvas refresh, no lag

## 🎯 What It Does

This project demonstrates an **truly agentic AI workflow** where:

1. An LLM agent (Gemini 2.0 Flash) receives a mathematical problem
2. The agent **autonomously decides** which tools to call and in what order
3. The agent determines **if visualization is needed** based on user request
4. Multiple function calls are executed in iterations until the solution is found
5. **Optional:** If requested, displays the result on a canvas with rectangle and text

### Key Feature: Autonomous Decision Making

**The agent is NOT programmatically controlled** - it makes ALL decisions including:

- Which math functions to call
- Whether to visualize the result
- When to open canvas and draw
- What text to display

### Example Task (WITH Visualization)

**Query:** "Find the ASCII values of characters in RISHIKESH, calculate the sum of exponentials of those values, and then visualize the final answer on a canvas with a rectangle and text."

**Agent Workflow:**

1. Calls `strings_to_chars_to_int("RISHIKESH")` → Returns ASCII values
2. Calls `int_list_to_exponential_sum([...])` → Returns sum
3. Calls `open_canvas()` → Opens blank canvas
4. Calls `draw_rectangle(100, 100, 600, 200)` → Draws rectangle
5. Calls `add_text_in_paint(110, 110, "Result: ...")` → Adds text
6. Calls `refresh_canvas()` → Refreshes display
7. Returns `FINAL_ANSWER: [result]`

### Example Task (WITHOUT Visualization)

**Query:** "Find the ASCII values of characters in RISHIKESH and calculate the sum of exponentials of those values."

**Agent Workflow:**

1. Calls `strings_to_chars_to_int("RISHIKESH")` → Returns ASCII values
2. Calls `int_list_to_exponential_sum([...])` → Returns sum
3. Returns `FINAL_ANSWER: [result]` → Done! (No canvas tools called)

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

### Customize Your Query

Edit `talk2mcp.py` (lines 166-171) to change the query:

**Option 1: With Visualization**

```python
query = """Find the ASCII values of characters in RISHIKESH, calculate the sum of exponentials of those values, and then visualize the final answer on a canvas with a rectangle and text."""
```

**Option 2: Without Visualization**

```python
query = """Find the ASCII values of characters in RISHIKESH and calculate the sum of exponentials of those values."""
```

### What Happens:

1. **MCP Server starts** - Exposes math and canvas tools
2. **LLM Agent receives task** - Analyzes query to understand requirements
3. **Autonomous execution** - Agent decides which functions to call:
   - Math iterations: Converts string → Calculates result
   - Visualization (if requested): Opens canvas → Draws → Adds text → Refreshes
4. **Result** - Agent returns FINAL_ANSWER when complete

### Visualization Trigger Words

The agent will visualize if your query contains keywords like:

- "visualize"
- "draw"
- "show on canvas"
- "paint"
- "display on canvas"

Otherwise, it returns just the calculated result!

---

## 🛠️ Key Components

### `talk2mcp.py` - MCP Client & Agent Orchestrator

- Connects to MCP server via STDIO
- Sends prompts to Gemini LLM with available tools
- Agent autonomously decides function calls based on query
- Parses agent responses (`FUNCTION_CALL:` or `FINAL_ANSWER:`)
- Executes MCP tool calls requested by agent
- Handles iterative execution (max 10 iterations)
- **No hardcoded logic** - agent makes ALL decisions

### `example_macp_server_mac.py` - MCP Server

- **Math Tools**: Arithmetic, trigonometry, string operations
- **Canvas Tools**: PIL-based programmatic image generation
  - `open_canvas()` - Creates blank canvas
  - `draw_rectangle()` - Draws rectangle outline
  - `add_text_in_paint()` - Adds text at specified position
  - `refresh_canvas()` - Refreshes Preview display
- Uses FastMCP for easy tool registration
- Runs on STDIO transport for direct client communication

---

## 🔧 Configuration

### Adjust Max Iterations

In `talk2mcp.py` (line 17):

```python
max_iterations = 10  # Increase for complex tasks with visualization
```

### Change Query/Task

In `talk2mcp.py` (lines 166-171):

```python
# Customize the task for the agent
query = """Your custom query here"""
```

### Modify Canvas Coordinates

The agent uses default coordinates, but you can guide it in the system prompt or query:

- Rectangle: `(100, 100, 600, 200)`
- Text position: `(110, 110)` with 10px padding

### Modify LLM Model

In `talk2mcp.py` (line 32):

```python
model="gemini-2.0-flash"  # Change to other Gemini models
```

### Adjust LLM Timeout

In `talk2mcp.py` (line 22):

```python
async def generate_with_timeout(client, prompt, timeout=10):  # seconds
```

---

## 🧪 Example Output

### With Visualization Request

```
Starting main execution...
Establishing connection to MCP server...
Successfully retrieved 24 tools

Query: Find the ASCII values of characters in RISHIKESH, calculate the sum
       of exponentials, and visualize the final answer on a canvas.

--- Iteration 1 ---
LLM Response: FUNCTION_CALL: strings_to_chars_to_int|RISHIKESH
Called: strings_to_chars_to_int with {'string': 'RISHIKESH'}
Result: [82, 73, 83, 72, 73, 75, 69, 83, 72]

--- Iteration 2 ---
LLM Response: FUNCTION_CALL: int_list_to_exponential_sum|82,73,83,72,73,75,69,83,72
Result: 8.599e+35

--- Iteration 3 ---
LLM Response: FUNCTION_CALL: open_canvas
Result: Interactive canvas opened

--- Iteration 4 ---
LLM Response: FUNCTION_CALL: draw_rectangle|100|100|600|200
Result: Rectangle drawn from (100,100) to (600,200)

--- Iteration 5 ---
LLM Response: FUNCTION_CALL: add_text_in_paint|110|110|Result: 8.599e+35
Result: Text 'Result: 8.599e+35' added at (110,110)

--- Iteration 6 ---
LLM Response: FUNCTION_CALL: refresh_canvas
Result: Canvas refreshed in Preview

--- Iteration 7 ---
LLM Response: FINAL_ANSWER: [8.599e+35]

=== Agent Execution Complete ===
✓ All tasks completed including visualization!
```

### Without Visualization Request

```
Query: Find the ASCII values of characters in RISHIKESH and calculate
       the sum of exponentials.

--- Iteration 1 ---
LLM Response: FUNCTION_CALL: strings_to_chars_to_int|RISHIKESH
Result: [82, 73, 83, 72, 73, 75, 69, 83, 72]

--- Iteration 2 ---
LLM Response: FUNCTION_CALL: int_list_to_exponential_sum|82,73,83,72,73,75,69,83,72
Result: 8.599e+35

--- Iteration 3 ---
LLM Response: FINAL_ANSWER: [8.599e+35]

=== Agent Execution Complete ===
✓ All tasks completed!
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

### 1. Truly Autonomous Agent Decision Making

The LLM agent receives a structured prompt with:

- **Available tools** and their signatures (24 tools)
- **Current task/query** from user
- **Previous iteration results** for context
- **Conditional workflow instructions** for visualization
- **Response format** requirements

**Key Difference:** The agent analyzes the query to determine if visualization is requested, then autonomously decides which tools to call and when.

### 2. Iterative Execution Loop

```
┌─────────────────────────────────┐
│  User Query                     │
│  (with or without "visualize")  │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Agent analyzes query           │
│  - What math operations needed? │
│  - Visualization requested?     │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Agent decides next action      │
│  Returns: FUNCTION_CALL or      │
│           FINAL_ANSWER           │
└────────────┬────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌──────────────┐  ┌──────────────┐
│ Function     │  │ FINAL_ANSWER │
│ Call         │  │ (when done)  │
│ - Math       │  └──────────────┘
│ - Canvas     │
│ - Any tool   │
└────┬─────────┘
     │
     ▼
┌─────────────────────┐
│ Execute & Return    │
│ Add to context      │
└────────┬────────────┘
         │
         └──────► (Loop back to agent)
```

### 3. Canvas Visualization (When Agent Decides)

- Agent calls `open_canvas()` when visualization is needed
- Uses PIL (Python Imaging Library) to draw programmatically
- Agent calls `draw_rectangle()` with coordinates
- Agent calls `add_text_in_paint()` with result
- Agent calls `refresh_canvas()` to update display
- Saves to `/tmp/mcp_canvas.png` and opens in macOS Preview

**No hardcoded logic** - every step is an agent decision!

---

## 🎨 Available Tools

### Math Tools

- `add`, `subtract`, `multiply`, `divide`
- `power`, `sqrt`, `cbrt`
- `sin`, `cos`, `tan`
- `log`, `factorial`
- `strings_to_chars_to_int` - Convert string to ASCII values
- `int_list_to_exponential_sum` - Sum of e^x for each x
- `fibonacci_numbers` - Generate Fibonacci sequence

### Canvas Tools

- `open_canvas()` - Create blank 800x600 canvas
- `draw_rectangle(x1, y1, x2, y2)` - Draw rectangle outline
- `add_text_in_paint(text_x, text_y, text)` - Add text at position
- `refresh_canvas()` - Refresh Preview display

---

## 🖼️ Implementation Approach: PIL vs GUI Automation

This project uses **PIL (Pillow)** for programmatic image generation rather than GUI automation.

### Our Approach (PIL)

```python
# Direct image manipulation
canvas = PILImage.new("RGB", (800, 600), "white")
draw = ImageDraw.Draw(canvas)
draw.rectangle([100, 100, 600, 200], outline="black")
draw.text((110, 110), "Result", fill="black")
canvas.save("/tmp/canvas.png")
```

### Alternative Approach (GUI Automation - Windows Paint)

```python
# Simulating user clicks
pyautogui.click(150, 80)  # Click rectangle tool
pyautogui.dragTo(500, 400)  # Draw rectangle
pyautogui.click(180, 80)  # Click text tool
pyautogui.write("Result")  # Type text
```

### Why PIL?

- ✅ **Cross-platform** - Works on macOS, Linux, Windows
- ✅ **Reliable** - No dependency on UI element positions
- ✅ **Fast** - Direct image manipulation
- ✅ **Maintainable** - Code-based, not coordinate-based
- ✅ **Headless capable** - Can run without display

### Trade-off

- GUI automation teaches UI interaction techniques (win32gui, pyautogui)
- PIL approach teaches image processing and programmatic drawing
- Both are valid; PIL is more production-ready

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
