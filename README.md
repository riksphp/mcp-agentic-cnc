# Gmail MCP Server Integration - Agentic AI Email Automation

> AI agent that performs calculations and automatically sends results via email using dual MCP servers.

**Gmail MCP Server**: https://github.com/jasonsum/gmail-mcp-server.git

---

## 📑 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start) 🆕 **Interactive Mode!**
- [Gmail OAuth Setup](#gmail-oauth-setup)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Architecture](#architecture)
- [Available Tools](#available-tools)
- [Troubleshooting](#troubleshooting)
- [File Structure](#file-structure)
- [Credits](#credits)

---

## Overview

This project integrates the [Gmail MCP Server](https://github.com/jasonsum/gmail-mcp-server.git) with an agentic workflow, enabling Gemini AI to connect to **two MCP servers simultaneously**:

1. **Math MCP Server** - Mathematical calculations and canvas visualization
2. **Gmail MCP Server** - Email operations (send, read, manage)

---

## Features

- ✅ **Interactive Mode** - Enter queries from terminal, no code editing needed!
- ✅ Perform complex mathematical calculations (ASCII conversion, exponential sums)
- ✅ Visualize results on canvas with rectangles and text
- ✅ **Automatically send results via Gmail**
- ✅ Read and manage Gmail messages
- ✅ Intelligent tool routing between servers
- ✅ Multiple queries in one session
- ✅ Configurable workflows (math-only, visualization, email, or all)

---

## Prerequisites

### Required Software

- Python 3.12+
- Gmail account
- Google Cloud Project (for OAuth)
- Gemini API key

### Install Dependencies

```bash
cd /Users/rishikesh.kumar/Desktop/EAGV2/mcp-agentic-cnc
pip install -r requirements.txt
```

**Dependencies installed:**

- `mcp` - Model Context Protocol
- `google-genai` - Gemini AI client
- `google-api-python-client` - Gmail API
- `google-auth-oauthlib` - OAuth authentication
- `python-dotenv` - Environment variables

---

## Quick Start

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Set Up Gmail OAuth (see detailed steps below)

```bash
# Place your OAuth credentials here:
/Users/rishikesh.kumar/Desktop/EAGV2/gmail-mcp-server/src/.google/client_creds.json
```

### 3️⃣ Run in Interactive Mode

```bash
python3 talk2mcp.py
```

**First run:** Browser opens for Gmail authentication → authorize → tokens saved automatically.

### 4️⃣ Enter Your Queries

```
💬 Your Query: Calculate ASCII sum for HELLO
💬 Your Query: Calculate ASCII sum for WORLD and visualize it
💬 Your Query: Calculate ASCII sum for AI and email to user@example.com
💬 Your Query: quit
```

> 💡 **New!** No more editing code! Just type your queries interactively. See `INTERACTIVE_MODE.md` for details.

---

## Gmail OAuth Setup

**⚠️ CRITICAL:** Follow the official Gmail MCP Server setup guide:
👉 **https://github.com/jasonsum/gmail-mcp-server#setup**

### Step-by-Step

#### 1. Create Google Cloud Project

- Go to: https://console.cloud.google.com/projectcreate
- Create a new project (e.g., "MCP Email Agent")

#### 2. Enable Gmail API

- Go to: https://console.cloud.google.com/workspace-api/products
- Search for "Gmail API" → Enable

#### 3. Configure OAuth Consent Screen

- Go to: https://console.cloud.google.com/apis/credentials/consent
- User type: **External**
- Add your email as **Test user**
- Add OAuth scope: `https://www.googleapis.com/auth/gmail.modify`

#### 4. Create OAuth Client ID

- Go to: https://console.cloud.google.com/apis/credentials/oauthclient
- Application type: **Desktop App**
- Name: "Gmail MCP Client"
- Click **Create** → Download JSON

#### 5. Save Credentials

```bash
# Rename downloaded file to:
client_creds.json

# Place in:
/Users/rishikesh.kumar/Desktop/EAGV2/gmail-mcp-server/src/.google/client_creds.json
```

✅ **Done!** The token file (`app_tokens.json`) will be auto-generated on first run.

---

## Configuration

### File Paths in `talk2mcp.py`

Verify these paths (lines 73-81):

| Configuration         | Path                                                                                  |
| --------------------- | ------------------------------------------------------------------------------------- |
| **Gmail MCP Server**  | `/Users/rishikesh.kumar/Desktop/EAGV2/gmail-mcp-server/src/gmail/server.py`           |
| **OAuth Credentials** | `/Users/rishikesh.kumar/Desktop/EAGV2/gmail-mcp-server/src/.google/client_creds.json` |
| **Access Tokens**     | `/Users/rishikesh.kumar/Desktop/EAGV2/gmail-mcp-server/src/.google/app_tokens.json`   |
| **Math MCP Server**   | `example_macp_server_mac.py` (relative path)                                          |

### Current Configuration (Line 214)

```python
# Active query:
query = """Find the ASCII values of characters in RISHIKESH, calculate the sum
of exponentials of those values, visualize it on canvas, and then send the query
and result via email to rishi.shrma06@gmail.com with subject 'EGA v2 Calculation Result'."""
```

**Customize:**

- **Recipient**: Change `rishi.shrma06@gmail.com` to your email
- **Subject**: Change `'EGA v2 Calculation Result'`
- **Input**: Change `RISHIKESH` to any text

---

## Usage Examples

> 💡 **Want more test prompts?** Check out `TEST_PROMPTS.md` for 20+ ready-to-use examples!

### Mode 1: Basic Calculation (No Visualization, No Email)

```python
query = """Find the ASCII values of characters in RISHIKESH and calculate
the sum of exponentials of those values."""
```

**Output:** Just returns the calculated value.

---

### Mode 2: Calculation + Visualization

```python
query = """Find the ASCII values of characters in RISHIKESH, calculate the sum
of exponentials, and visualize the result on canvas."""
```

**Output:** Calculation + canvas window with result displayed.

---

### Mode 3: Calculation + Email

```python
query = """Find the ASCII values of characters in RISHIKESH, calculate the sum
of exponentials, and send the result via email to user@example.com with
subject 'Calculation Result'."""
```

**Output:** Calculation + email sent to recipient.

---

### Mode 4: Everything (Current Configuration)

```python
query = """Find the ASCII values of characters in RISHIKESH, calculate the sum
of exponentials, visualize it on canvas, and send the result via email to
user@example.com with subject 'Result'."""
```

**Output:** Calculation + visualization + email.

---

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────┐
│              talk2mcp.py (Gemini Agent)             │
│  • Query processing                                 │
│  • Tool selection & routing                         │
│  • Workflow orchestration                           │
└─────────────┬───────────────────────┬───────────────┘
              │                       │
    ┌─────────▼──────────┐  ┌────────▼──────────────┐
    │  Math MCP Server   │  │  Gmail MCP Server     │
    │  • ASCII convert   │  │  • Send email         │
    │  • Calculations    │  │  • Read email         │
    │  • Canvas viz      │  │  • Manage email       │
    └────────────────────┘  └───────────────────────┘
```

### Execution Flow

```
User Query
    ↓
[1] Gemini Agent receives query
    ↓
[2] Agent discovers tools from both MCP servers
    ↓
[3] Agent decides workflow based on query keywords
    ↓
[4] Execute calculations (Math MCP)
    ↓
[5] Visualize if requested (Math MCP)
    ↓
[6] Send email if requested (Gmail MCP)
    ↓
[7] Return FINAL_ANSWER
```

### Example Execution

```
Query: "Calculate ASCII sum for RISHIKESH and email it to me"

┌──────────────────────────────────────────────────────────┐
│ Step 1: strings_to_chars_to_int|RISHIKESH               │
│         → Math MCP Server                                │
│         → [82, 73, 83, 72, 73, 75, 69, 83, 72]          │
├──────────────────────────────────────────────────────────┤
│ Step 2: int_list_to_exponential_sum|82,73,83,...        │
│         → Math MCP Server                                │
│         → 1.234e+35                                      │
├──────────────────────────────────────────────────────────┤
│ Step 3: send-email|user@example.com|Subject|Message     │
│         → Gmail MCP Server                               │
│         → Email sent successfully                        │
├──────────────────────────────────────────────────────────┤
│ Step 4: FINAL_ANSWER: [1.234e+35]                       │
└──────────────────────────────────────────────────────────┘
```

---

## Available Tools

### Math MCP Server Tools

| Tool                          | Description                    | Parameters                  |
| ----------------------------- | ------------------------------ | --------------------------- |
| `strings_to_chars_to_int`     | Convert string to ASCII values | `text`                      |
| `int_list_to_exponential_sum` | Calculate sum of exponentials  | `numbers` (comma-separated) |
| `open_canvas`                 | Open canvas window             | None                        |
| `draw_rectangle`              | Draw rectangle on canvas       | `x1`, `y1`, `x2`, `y2`      |
| `add_text_in_paint`           | Add text to canvas             | `text_x`, `text_y`, `text`  |
| `refresh_canvas`              | Refresh canvas display         | None                        |

### Gmail MCP Server Tools

| Tool                 | Description           | Parameters                           |
| -------------------- | --------------------- | ------------------------------------ |
| `send-email`         | Send an email         | `recipient_id`, `subject`, `message` |
| `get-unread-emails`  | Get unread emails     | None                                 |
| `read-email`         | Read specific email   | `email_id`                           |
| `trash-email`        | Move email to trash   | `email_id`                           |
| `mark-email-as-read` | Mark email as read    | `email_id`                           |
| `open-email`         | Open email in browser | `email_id`                           |

---

## Troubleshooting

### ❌ "client_creds.json not found"

**Solution:**

1. Follow [Gmail OAuth Setup](#gmail-oauth-setup)
2. Download OAuth credentials from Google Cloud Console
3. Rename to `client_creds.json`
4. Place in: `/Users/rishikesh.kumar/Desktop/EAGV2/gmail-mcp-server/src/.google/`

---

### ❌ "Gmail authentication failed"

**Solution:**

```bash
# Delete tokens and re-authenticate
rm /Users/rishikesh.kumar/Desktop/EAGV2/gmail-mcp-server/src/.google/app_tokens.json
python3 talk2mcp.py
```

---

### ❌ "MCP server connection failed"

**Test Gmail server independently:**

```bash
cd /Users/rishikesh.kumar/Desktop/EAGV2/gmail-mcp-server
python3 src/gmail/server.py \
  --creds-file-path src/.google/client_creds.json \
  --token-path src/.google/app_tokens.json
```

**Test Math server:**

```bash
cd /Users/rishikesh.kumar/Desktop/EAGV2/mcp-agentic-cnc
python3 example_macp_server_mac.py
```

---

### ❌ "Email not received"

**Checklist:**

- ✅ Check spam folder
- ✅ Verify recipient email in line 214 of `talk2mcp.py`
- ✅ Check DEBUG output for "send-email" tool call
- ✅ Verify Gmail API quota in Google Cloud Console
- ✅ Ensure OAuth scope includes `gmail.modify`

---

### ❌ "Tools not found" or "Unknown tool"

**Solution:**

```bash
# Check if both servers are starting correctly
# Look for these lines in output:
Successfully retrieved X math tools and 6 gmail tools
Total tools available: Y
```

If tools are missing, verify both server scripts exist and are executable.

---

## File Structure

```
EAGV2/
├── mcp-agentic-cnc/
│   ├── talk2mcp.py                    # Main integration script ⭐
│   ├── example_macp_server_mac.py     # Math MCP server
│   ├── requirements.txt                # Python dependencies
│   └── README.md                       # This file
│
└── gmail-mcp-server/                   # Official Gmail MCP Server
    ├── src/
    │   ├── gmail/
    │   │   └── server.py              # Gmail MCP server
    │   └── .google/
    │       ├── client_creds.json      # OAuth credentials (CREATE THIS) 🔑
    │       └── app_tokens.json        # Auto-generated access tokens
    ├── pyproject.toml
    └── README.md                       # Official documentation
```

---

## Verification Checklist

Before running, verify:

- [ ] Python 3.12+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Google Cloud project created
- [ ] Gmail API enabled
- [ ] OAuth credentials downloaded
- [ ] `client_creds.json` placed in `.google/` folder
- [ ] Email address updated in line 214
- [ ] GEMINI_API_KEY set in environment
- [ ] Both MCP server scripts exist

**Quick verification:**

```bash
# Check files exist
ls /Users/rishikesh.kumar/Desktop/EAGV2/gmail-mcp-server/src/.google/client_creds.json
ls /Users/rishikesh.kumar/Desktop/EAGV2/gmail-mcp-server/src/gmail/server.py
ls /Users/rishikesh.kumar/Desktop/EAGV2/mcp-agentic-cnc/example_macp_server_mac.py
```

---

## Expected Output

```bash
$ python3 talk2mcp.py

Starting main execution...
Establishing connection to Math MCP server...
Establishing connection to Gmail MCP server...
Connections established, creating sessions...
Sessions created, initializing...
Successfully retrieved 6 math tools and 6 gmail tools
Total tools available: 12
Starting iteration loop...
Query: Find the ASCII values of characters in RISHIKESH...

--- Iteration 1 ---
LLM Response: FUNCTION_CALL: strings_to_chars_to_int|RISHIKESH
DEBUG: Routing to Math session
DEBUG: Final iteration result: [82, 73, 83, 72, 73, 75, 69, 83, 72]

--- Iteration 2 ---
LLM Response: FUNCTION_CALL: int_list_to_exponential_sum|82,73,83,72,73,75,69,83,72
DEBUG: Routing to Math session
DEBUG: Final iteration result: 1.234e+35

--- Iteration 3 ---
LLM Response: FUNCTION_CALL: open_canvas
DEBUG: Routing to Math session
[Canvas window opens]

--- Iteration 4 ---
LLM Response: FUNCTION_CALL: draw_rectangle|100|100|600|200
DEBUG: Routing to Math session
[Rectangle drawn]

--- Iteration 5 ---
LLM Response: FUNCTION_CALL: send-email|rishi.shrma06@gmail.com|EGA v2 Result|The result is 1.234e+35
DEBUG: Routing to Gmail session
Email sent successfully. Message ID: 1a2b3c4d

--- Iteration 6 ---
=== Agent Execution Complete ===
Agent returned: FINAL_ANSWER: [1.234e+35]

✓ All tasks completed including visualization!
```

---

## Credits

- **Gmail MCP Server**: [Jason Summer](https://github.com/jasonsum/gmail-mcp-server)
- **Model Context Protocol**: [Anthropic](https://modelcontextprotocol.io/)
- **Integration**: EGA V2 Project

---

## Additional Resources

- **Gmail MCP Server Repository**: https://github.com/jasonsum/gmail-mcp-server
- **MCP Documentation**: https://modelcontextprotocol.io/
- **Gmail API**: https://developers.google.com/gmail/api
- **Google Cloud Console**: https://console.cloud.google.com

---

## License

This integration follows the licensing of the original Gmail MCP Server (GPL-3.0).

---

## Support

**Issues with Gmail OAuth:** Follow https://github.com/jasonsum/gmail-mcp-server#troubleshooting-with-mcp-inspector

**Issues with this integration:** Check the troubleshooting section above or verify your configuration matches the [Configuration](#configuration) section.

---

**🚀 Ready to run? Execute:** `python3 talk2mcp.py`
