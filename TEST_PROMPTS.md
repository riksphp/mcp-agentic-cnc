# Test Prompts for Gmail MCP Integration

Here are various prompts to test different capabilities of your dual MCP server setup.

---

## 🎯 Quick Tests (Basic Functionality)

### 1. Math Only (No Visualization, No Email)

```python
query = """Find the ASCII values of characters in PYTHON and calculate the sum of exponentials of those values."""
```

**Expected:** Quick calculation, returns final answer immediately.

---

### 2. Math + Visualization

```python
query = """Find the ASCII values of characters in GEMINI, calculate the sum of exponentials, and visualize the result on canvas with a rectangle and the result displayed as text."""
```

**Expected:** Calculation + canvas window opens with result displayed.

---

### 3. Math + Email

```python
query = """Find the ASCII values of characters in AGENTIC, calculate the sum of exponentials of those values, and send the result via email to rishi.shrma06@gmail.com with subject 'Test Result - Agentic'."""
```

**Expected:** Calculation + email sent (no canvas).

---

## 🚀 Advanced Tests (Multiple Features)

### 4. Everything: Math + Viz + Email (Current Default)

```python
query = """Find the ASCII values of characters in RISHIKESH, calculate the sum of exponentials of those values, visualize it on canvas, and then send the query and result via email to rishi.shrma06@gmail.com with subject 'Complete Test Result'."""
```

**Expected:** Full workflow - calculation → visualization → email.

---

### 5. Custom String with Detailed Email

```python
query = """Calculate the ASCII sum of exponentials for the word CONGRATULATIONS, visualize the result beautifully on canvas, and email a detailed summary to rishi.shrma06@gmail.com with subject 'ASCII Calculation Report' including the input string, ASCII values, and final result."""
```

**Expected:** More detailed email content with full breakdown.

---

## 📊 Real-World Use Cases

### 6. Daily Report Style

```python
query = """Find the ASCII values for the string MONDAY, calculate their exponential sum, display it on canvas, and send a professional email to rishi.shrma06@gmail.com with subject 'Daily ASCII Report - Monday' containing the calculation details."""
```

**Expected:** Professional formatted email with calculation details.

---

### 7. Short String Test

```python
query = """Calculate ASCII exponential sum for AI, visualize it, and email the result to rishi.shrma06@gmail.com with subject 'Short String Test'."""
```

**Expected:** Quick test with short string (only 2 characters).

---

### 8. Long String Test

```python
query = """Calculate ASCII exponential sum for ARTIFICIALINTELLIGENCE, visualize the result on canvas with a large rectangle, and send a comprehensive email to rishi.shrma06@gmail.com with subject 'Long String Analysis'."""
```

**Expected:** Tests handling of longer strings (23 characters).

---

## 🎨 Creative/Fun Tests

### 9. Your Name Calculation

```python
query = """Find out what my name RISHIKESH looks like in ASCII exponentials! Calculate the sum, show it beautifully on canvas, and email me the result at rishi.shrma06@gmail.com with subject 'Your Name in Exponentials'."""
```

**Expected:** Personalized calculation and email.

---

### 10. Code Word Test

```python
query = """Decode the word PYTHON by converting to ASCII, calculating exponential sum, visualizing on canvas, and sending analysis to rishi.shrma06@gmail.com with subject 'Python Analysis Complete'."""
```

**Expected:** Theme-based calculation.

---

### 11. Motivational Test

```python
query = """Calculate the exponential power of the word SUCCESS, visualize it dramatically on canvas, and send an inspiring email to rishi.shrma06@gmail.com with subject 'The Power of Success'."""
```

**Expected:** Creative phrasing test.

---

## 🧪 Edge Cases & Testing

### 12. Single Character

```python
query = """Calculate ASCII exponential for just the letter Z and email the result to rishi.shrma06@gmail.com with subject 'Single Character Test'."""
```

**Expected:** Tests minimal input (1 character).

---

### 13. Numbers in String (if supported)

```python
query = """Calculate ASCII values for ABC123, compute exponential sum, visualize, and email to rishi.shrma06@gmail.com with subject 'Alphanumeric Test'."""
```

**Expected:** Tests alphanumeric handling.

---

### 14. Multiple Calculations

```python
query = """First calculate ASCII exponential sum for ALPHA, then calculate it for BETA, visualize both results on canvas if possible, and send both results in one email to rishi.shrma06@gmail.com with subject 'Dual Calculation Test'."""
```

**Expected:** Tests multiple sequential calculations.

---

## 📧 Email-Focused Tests

### 15. Email with Detailed Report

```python
query = """Calculate ASCII exponential sum for MACHINE, and send a detailed technical report email to rishi.shrma06@gmail.com with subject 'Technical Report: ASCII Analysis' that includes: 1) Original string, 2) Individual ASCII values, 3) Exponential calculation, 4) Final sum with scientific notation."""
```

**Expected:** Well-structured email with multiple sections.

---

### 16. Quick Email Notification

```python
query = """Calculate ASCII sum for URGENT and immediately email the result to rishi.shrma06@gmail.com with subject 'Quick Calculation Complete'."""
```

**Expected:** Fast calculation → email (no visualization).

---

### 17. Email with Custom Message

```python
query = """Calculate ASCII exponentials for HELLO, and send a friendly email to rishi.shrma06@gmail.com with subject 'Greetings from AI Agent' saying hello and including the calculation result in a conversational way."""
```

**Expected:** Natural language in email content.

---

## 🎓 Learning/Demo Tests

### 18. Educational Example

```python
query = """For the word LEARNING, calculate ASCII values step by step, show the exponential sum calculation, visualize the result on canvas, and send an educational email to rishi.shrma06@gmail.com with subject 'How ASCII Exponentials Work' explaining each step."""
```

**Expected:** Detailed explanatory email.

---

### 19. Comparison Test

```python
query = """Calculate ASCII exponential sums for both SMALL and LARGE, compare the results, visualize both on canvas, and email a comparison report to rishi.shrma06@gmail.com with subject 'Size Comparison Analysis'."""
```

**Expected:** Tests comparative analysis.

---

### 20. Summary Report

```python
query = """Analyze the string COMPLETE by calculating its ASCII exponential sum, create a comprehensive visualization on canvas, and send a summary report email to rishi.shrma06@gmail.com with subject 'Comprehensive Analysis Report - Complete' including all calculation steps, visualizations mentioned, and final conclusion."""
```

**Expected:** Full-featured comprehensive test.

---

## 🔧 Configuration Tips

### To Use These Prompts:

1. **Copy any prompt** from above
2. **Edit line 214** in `talk2mcp.py`
3. **Replace the existing query** with your chosen prompt
4. **Customize:**
   - Change the word (e.g., `PYTHON` → `YOUR_WORD`)
   - Change email address if needed
   - Change subject line
5. **Run:** `python3 talk2mcp.py`

### Example:

```python
# In talk2mcp.py, line 214:
query = """Calculate ASCII exponential sum for TESTING, visualize it, and email to rishi.shrma06@gmail.com with subject 'Test Complete'."""
```

---

## 📊 Recommended Testing Order

Start with these in order:

1. **Test #1** (Math Only) - Verify basic calculation works
2. **Test #2** (Math + Viz) - Verify canvas works
3. **Test #3** (Math + Email) - Verify email works
4. **Test #4** (Everything) - Verify full integration
5. Then try **creative tests** (#9-11)
6. Finally try **edge cases** (#12-14)

---

## 🎯 Quick Customization Template

```python
query = """
Calculate ASCII exponential sum for [YOUR_WORD],
[visualize it on canvas,]
[and] send [description] email to rishi.shrma06@gmail.com
with subject '[YOUR_SUBJECT]'
[including additional details you want].
"""
```

**Fill in:**

- `[YOUR_WORD]` - Any word to analyze
- `[visualize...]` - Include or remove
- `[description]` - a detailed/quick/professional/friendly
- `[YOUR_SUBJECT]` - Email subject
- `[including...]` - Any additional instructions

---

## 💡 Pro Tips

### For Better Results:

- ✅ Use **clear keywords**: "visualize", "email", "send to"
- ✅ Be **specific** about what goes in the email
- ✅ Include **subject line** in your prompt
- ✅ Use **natural language** - the agent understands context
- ✅ Test **incrementally** - start simple, add complexity

### Avoid:

- ❌ Vague instructions like "do something"
- ❌ Conflicting requests
- ❌ Missing email address when requesting email
- ❌ Too many tasks in one prompt (max 3-4 operations)

---

## 🚀 Ready to Test!

Pick a prompt, customize it, and run:

```bash
cd /Users/rishikesh.kumar/Desktop/EAGV2/mcp-agentic-cnc
python3 talk2mcp.py
```

**Have fun experimenting! 🎉**
