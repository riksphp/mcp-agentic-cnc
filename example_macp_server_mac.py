# -----------------------------
# example_mcp_server.py
# -----------------------------
import asyncio
import uvloop
import sys
import time
import subprocess
import os
import math
from PIL import Image as PILImage, ImageDraw, ImageFont
import pyautogui

from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types

# -----------------------------
# Setup uvloop for async performance
# -----------------------------
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# -----------------------------
# Instantiate MCP
# -----------------------------
mcp = FastMCP("Calculator")

# -----------------------------
# Global variables for canvas
# -----------------------------
canvas_image_path = "/tmp/mcp_canvas.png"
canvas_app_open = False
canvas_position = (100, 100)  # top-left of canvas window

# -----------------------------
# Math / string / image tools
# -----------------------------
@mcp.tool()
def add(a: int, b: int) -> int:
    print("CALLED: add")
    return a + b

@mcp.tool()
def add_list(l: list) -> int:
    print("CALLED: add_list")
    return sum(l)

@mcp.tool()
def subtract(a: int, b: int) -> int:
    print("CALLED: subtract")
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    print("CALLED: multiply")
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float:
    print("CALLED: divide")
    return a / b

@mcp.tool()
def power(a: int, b: int) -> int:
    print("CALLED: power")
    return a ** b

@mcp.tool()
def sqrt(a: int) -> float:
    print("CALLED: sqrt")
    return a ** 0.5

@mcp.tool()
def cbrt(a: int) -> float:
    print("CALLED: cbrt")
    return a ** (1/3)

@mcp.tool()
def factorial(a: int) -> int:
    print("CALLED: factorial")
    return math.factorial(a)

@mcp.tool()
def log(a: int) -> float:
    print("CALLED: log")
    return math.log(a)

@mcp.tool()
def remainder(a: int, b: int) -> int:
    print("CALLED: remainder")
    return a % b

@mcp.tool()
def sin(a: int) -> float:
    print("CALLED: sin")
    return math.sin(a)

@mcp.tool()
def cos(a: int) -> float:
    print("CALLED: cos")
    return math.cos(a)

@mcp.tool()
def tan(a: int) -> float:
    print("CALLED: tan")
    return math.tan(a)

@mcp.tool()
def mine(a: int, b: int) -> int:
    print("CALLED: mine")
    return a - b - b

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    print("CALLED: create_thumbnail")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    print("CALLED: strings_to_chars_to_int")
    return [ord(c) for c in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    print("CALLED: int_list_to_exponential_sum")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    print("CALLED: fibonacci_numbers")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]

# -----------------------------
# Canvas tools (interactive)
# -----------------------------

def _force_preview_refresh(image_path: str):
    """Helper function to force Preview to reload the image."""
    # Close existing Preview window
    subprocess.run(["pkill", "-f", "Preview"], stderr=subprocess.DEVNULL)
    time.sleep(0.2)
    # Reopen the image
    subprocess.Popen(["open", image_path])
    time.sleep(0.3)

@mcp.tool()
async def open_canvas() -> dict:
    global canvas_app_open, canvas_image_path, canvas_position
    try:
        blank = PILImage.new("RGB", (800, 600), color="white")
        blank.save(canvas_image_path)
        subprocess.Popen(["open", canvas_image_path])
        time.sleep(1)
        canvas_app_open = True
        return {"content": [TextContent(type="text", text="Interactive canvas opened")]}
    except Exception as e:
        return {"content": [TextContent(type="text", text=f"Error opening canvas: {e}")]}

@mcp.tool()
async def draw_rectangle(x1: int, y1: int, x2: int, y2: int) -> dict:
    global canvas_app_open, canvas_image_path
    try:
        if not canvas_app_open:
            return {"content": [TextContent(type="text", text="Canvas not open")]}

        # Open existing canvas
        canvas = PILImage.open(canvas_image_path)
        draw = ImageDraw.Draw(canvas)

        # Draw rectangle
        draw.rectangle([x1, y1, x2, y2], outline="black", width=3)

        # Save updated canvas (don't reopen yet)
        canvas.save(canvas_image_path)

        return {"content": [TextContent(type="text", text=f"Rectangle drawn from ({x1},{y1}) to ({x2},{y2})")]}

    except Exception as e:
        return {"content": [TextContent(type="text", text=f"Error: {e}")]}

@mcp.tool()
async def add_text_in_paint(text_x: int, text_y: int, text: str) -> dict:
    global canvas_app_open, canvas_image_path

    try:
        if not canvas_app_open:
            return {"content": [TextContent(type="text", text="Canvas not open")]}

        # Open existing canvas
        canvas = PILImage.open(canvas_image_path)
        draw = ImageDraw.Draw(canvas)

        # Add text at specified position (rectangle should already be drawn)
        try:
            font = ImageFont.truetype("Arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((text_x, text_y), text, fill="black", font=font)

        # Save updated canvas (don't reopen yet)
        canvas.save(canvas_image_path)

        return {"content": [TextContent(type="text", text=f"Text '{text}' added at ({text_x},{text_y})")]}

    except Exception as e:
        return {"content": [TextContent(type="text", text=f"Error: {e}")]}

@mcp.tool()
async def refresh_canvas() -> dict:
    """
    Force refresh the canvas in Preview by closing and reopening.
    This ensures all drawn elements are visible immediately.
    """
    global canvas_app_open, canvas_image_path
    try:
        if not canvas_app_open:
            return {"content": [TextContent(type="text", text="Canvas not open")]}

        # Use helper to force Preview refresh
        _force_preview_refresh(canvas_image_path)
        
        return {"content": [TextContent(type="text", text="Canvas refreshed and displayed in Preview")]}
    except Exception as e:
        return {"content": [TextContent(type="text", text=f"Error refreshing canvas: {e}")]}


# -----------------------------
# Resources
# -----------------------------
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}!"

# -----------------------------
# Prompts
# -----------------------------
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"

@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

# -----------------------------
# RUN MCP SERVER
# -----------------------------
if __name__ == "__main__":
    print("STARTING MCP SERVER ON TCP 8765 WITH UVLOOP")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run(transport="tcp")  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
