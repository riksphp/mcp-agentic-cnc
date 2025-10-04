# Interactive Mode - User Input from Terminal

## Overview

The `talk2mcp.py` script now supports **interactive mode** where you can:

- ✅ Enter queries directly from terminal
- ✅ Get results immediately
- ✅ Ask multiple queries in a row
- ✅ Type 'quit' to exit anytime

No more editing the script for each query!

---

## How to Use

### Start Interactive Mode

```bash
cd /Users/rishikesh.kumar/Desktop/EAGV2/mcp-agentic-cnc
python3 talk2mcp.py
```

### You'll See This Welcome Screen:

```
======================================================================
🤖 AGENTIC AI ASSISTANT - Interactive Mode
======================================================================

Capabilities:
  • Mathematical calculations (ASCII, exponentials, etc.)
  • Canvas visualization
  • Email results via Gmail

Examples:
  "Calculate ASCII sum for HELLO"
  "Calculate ASCII sum for WORLD and visualize it"
  "Calculate ASCII sum for AI and email to me@example.com"

Type 'quit', 'exit', or 'q' to stop.

======================================================================

💬 Your Query: _
```

### Enter Your Query

Just type naturally and press Enter:

```
💬 Your Query: Calculate ASCII sum for PYTHON
```

### Agent Processes Your Request

```
🔄 Processing: Calculate ASCII sum for PYTHON
----------------------------------------------------------------------

--- Iteration 1 ---
LLM Response: FUNCTION_CALL: strings_to_chars_to_int|PYTHON
DEBUG: Routing to Math session
...

--- Iteration 2 ---
LLM Response: FUNCTION_CALL: int_list_to_exponential_sum|80,89,84,72,79,78
...

======================================================================
✅ QUERY COMPLETE
======================================================================
Final Answer: FINAL_ANSWER: [1.234e+50]
======================================================================
```

### Ask Another Query

The prompt returns automatically:

```
💬 Your Query: Calculate ASCII sum for AI and visualize it
```

### Exit Anytime

Type any of these:

- `quit`
- `exit`
- `q`
- Press `Ctrl+C`

```
💬 Your Query: quit

👋 Goodbye!

======================================================================
👋 Thank you for using the Agentic AI Assistant!
======================================================================
```

---

## Example Session

```bash
$ python3 talk2mcp.py

======================================================================
🤖 AGENTIC AI ASSISTANT - Interactive Mode
======================================================================

Capabilities:
  • Mathematical calculations (ASCII, exponentials, etc.)
  • Canvas visualization
  • Email results via Gmail

Examples:
  "Calculate ASCII sum for HELLO"
  "Calculate ASCII sum for WORLD and visualize it"
  "Calculate ASCII sum for AI and email to me@example.com"

Type 'quit', 'exit', or 'q' to stop.

======================================================================

💬 Your Query: Calculate ASCII sum for HELLO

🔄 Processing: Calculate ASCII sum for HELLO
----------------------------------------------------------------------

--- Iteration 1 ---
[calculations happen...]

======================================================================
✅ QUERY COMPLETE
======================================================================
Final Answer: FINAL_ANSWER: [2.54e+32]
======================================================================

💬 Your Query: Now visualize it on canvas

🔄 Processing: Now visualize it on canvas
----------------------------------------------------------------------

[visualization happens...]

======================================================================
✅ QUERY COMPLETE
======================================================================

💬 Your Query: Calculate ASCII sum for PYTHON and email to rishi.shrma06@gmail.com

🔄 Processing: Calculate ASCII sum for PYTHON and email to rishi.shrma06@gmail.com
----------------------------------------------------------------------

[calculation and email happen...]

======================================================================
✅ QUERY COMPLETE
======================================================================

💬 Your Query: quit

👋 Goodbye!

======================================================================
👋 Thank you for using the Agentic AI Assistant!
======================================================================
```

---

## Query Examples

### Simple Calculations

```
Calculate ASCII sum for HELLO
Find ASCII values for WORLD
Calculate exponential sum for TESTING
```

### With Visualization

```
Calculate ASCII sum for GEMINI and visualize it
Calculate ASCII for PYTHON and show on canvas
Visualize ASCII exponential sum for AI
```

### With Email

```
Calculate ASCII sum for DATA and email to me@example.com
Calculate exponential sum for HELLO and send result to user@gmail.com with subject 'Result'
```

### Combined (All Features)

```
Calculate ASCII sum for COMPLETE, visualize it, and email to me@example.com
Find ASCII values for SUCCESS, show on canvas, and email the result
```

### Natural Language

The agent understands natural phrasing:

```
What's the ASCII exponential sum for MACHINE?
Can you calculate ASCII values for LEARNING and show it?
Please find the exponential sum for CODE and send it to me@example.com
```

---

## Features

### ✅ Automatic State Reset

Each new query starts fresh:

- Previous calculations cleared
- Iteration counter reset
- Response history cleared

### ✅ Error Handling

If a query fails:

- Error is displayed
- You can try again with a new query
- System continues running

```
💬 Your Query: bad query that fails

❌ Error: [error details]

💬 Your Query: [try again]
```

### ✅ Empty Query Protection

```
💬 Your Query: [just press Enter]

⚠️  Please enter a query.

💬 Your Query: _
```

### ✅ Graceful Exit

Multiple ways to exit:

- Type `quit`, `exit`, or `q`
- Press `Ctrl+C`
- Close terminal

All trigger clean shutdown.

---

## Tips

### 1. Be Specific

✅ Good: "Calculate ASCII sum for HELLO and visualize it"
❌ Vague: "Do something"

### 2. Include Email When Needed

✅ Good: "Calculate ASCII sum for WORLD and email to user@example.com"
❌ Missing: "Calculate ASCII sum for WORLD and email it" (missing address)

### 3. Use Keywords

The agent recognizes:

- **Calculate**, **find**, **compute** - for calculations
- **Visualize**, **show**, **display**, **canvas** - for visualization
- **Email**, **send** - for email operations

### 4. Natural Language Works

You don't need exact syntax:

- "What is the ASCII sum for HELLO?"
- "Can you find exponential sum for WORLD?"
- "Please calculate ASCII values for PYTHON and show me"

All work fine!

---

## Troubleshooting

### Query Hangs or Doesn't Respond

**Press Ctrl+C once** to cancel current query, then try again.

### Can't Type After Result

**Press Enter** - the prompt may be waiting for input.

### Want to Exit But Stuck in Loop

**Press Ctrl+C** - forces exit immediately.

### MCP Servers Not Connecting

Restart the script:

```bash
python3 talk2mcp.py
```

Servers reconnect on each run.

---

## Comparison: Old vs New

### Old Way (Hardcoded Query)

```python
# Edit talk2mcp.py
query = """Calculate ASCII sum for HELLO"""

# Save file

# Run
python3 talk2mcp.py

# Want different query? Edit file again!
```

### New Way (Interactive)

```bash
# Run once
python3 talk2mcp.py

# Enter queries interactively
💬 Your Query: Calculate ASCII sum for HELLO
[result]

💬 Your Query: Calculate ASCII sum for WORLD
[result]

💬 Your Query: Calculate ASCII sum for PYTHON
[result]

💬 Your Query: quit
```

**Much faster!** 🚀

---

## Advanced Usage

### Multiple Related Queries

```bash
💬 Your Query: Calculate ASCII sum for ALPHA

[result shows number]

💬 Your Query: Calculate ASCII sum for BETA

[result shows different number]

💬 Your Query: Which one is larger?

[agent can reason about previous context]
```

### Chain Operations

```bash
💬 Your Query: Calculate ASCII sum for HELLO

[gets result]

💬 Your Query: Now visualize it

[uses previous calculation to visualize]
```

**Note:** Context between queries depends on LLM's conversation memory. Each query technically starts fresh in current implementation.

---

## Configuration

### Change Default Email

No configuration needed - just include email in your query:

```
💬 Your Query: Calculate ASCII sum for TEST and email to myemail@example.com
```

### Disable DEBUG Output

If you want less verbose output, you can comment out DEBUG print statements in the code (lines 277-280, 289-290, etc.).

---

## Summary

| Feature               | Status                                      |
| --------------------- | ------------------------------------------- |
| **Interactive Input** | ✅ Enter queries from terminal              |
| **Multiple Queries**  | ✅ Ask many questions in one session        |
| **Auto State Reset**  | ✅ Each query starts fresh                  |
| **Easy Exit**         | ✅ Type quit/exit/q or Ctrl+C               |
| **Error Recovery**    | ✅ Continue after errors                    |
| **Natural Language**  | ✅ Conversational queries work              |
| **All Features**      | ✅ Math, visualization, email all supported |

---

## Try It Now!

```bash
cd /Users/rishikesh.kumar/Desktop/EAGV2/mcp-agentic-cnc
python3 talk2mcp.py
```

**Start chatting with your AI assistant! 🤖💬**
