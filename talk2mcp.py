import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
from google import genai
from concurrent.futures import TimeoutError
from functools import partial

# Load environment variables from .env file
load_dotenv()

# Access your API key and initialize Gemini client correctly
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

max_iterations = 15  # Increased for math + canvas visualization + email steps
last_response = None
iteration = 0
iteration_response = []

# Global sessions for both MCP servers
math_session = None
gmail_session = None

async def generate_with_timeout(client, prompt, timeout=10):
    """Generate content with a timeout"""
    print("Starting LLM generation...")
    try:
        # Convert the synchronous generate_content call to run in a thread
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None, 
                lambda: client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
            ),
            timeout=timeout
        )
        print("LLM generation completed")
        return response
    except TimeoutError:
        print("LLM generation timed out!")
        raise
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        raise

def reset_state():
    """Reset all global variables to their initial state"""
    global last_response, iteration, iteration_response
    last_response = None
    iteration = 0
    iteration_response = []

async def main():
    reset_state()  # Reset at the start of main
    print("Starting main execution...")
    
    global math_session, gmail_session
    
    try:
        # Create MCP server connections for BOTH math and gmail servers
        print("Establishing connection to Math MCP server...")
        math_server_params = StdioServerParameters(
            command="python3",
            args=["example_macp_server_mac.py"]
        )
        
        print("Establishing connection to Gmail MCP server...")
        gmail_server_params = StdioServerParameters(
            command="python3",
            args=[
                "/Users/rishikesh.kumar/Desktop/EAGV2/gmail-mcp-server/src/gmail/server.py",
                "--creds-file-path",
                "/Users/rishikesh.kumar/Desktop/EAGV2/gmail-mcp-server/src/.google/client_creds.json",
                "--token-path",
                "/Users/rishikesh.kumar/Desktop/EAGV2/gmail-mcp-server/src/.google/app_tokens.json"
            ]
        )

        # Connect to both servers
        async with stdio_client(math_server_params) as (math_read, math_write), \
                   stdio_client(gmail_server_params) as (gmail_read, gmail_write):
            print("Connections established, creating sessions...")
            
            async with ClientSession(math_read, math_write) as math_sess, \
                       ClientSession(gmail_read, gmail_write) as gmail_sess:
                print("Sessions created, initializing...")
                
                # Store sessions globally so we can route tool calls
                math_session = math_sess
                gmail_session = gmail_sess
                
                await math_session.initialize()
                await gmail_session.initialize()
                
                # Get available tools from BOTH servers
                print("Requesting tool lists from both servers...")
                math_tools_result = await math_session.list_tools()
                gmail_tools_result = await gmail_session.list_tools()
                
                math_tools = math_tools_result.tools
                gmail_tools = gmail_tools_result.tools
                
                # Merge tools from both servers
                tools = list(math_tools) + list(gmail_tools)
                print(f"Successfully retrieved {len(math_tools)} math tools and {len(gmail_tools)} gmail tools")
                print(f"Total tools available: {len(tools)}")

                # Create system prompt with available tools
                print("Creating system prompt...")
                print(f"Number of tools: {len(tools)}")
                
                try:
                    # First, let's inspect what a tool object looks like
                    # if tools:
                    #     print(f"First tool properties: {dir(tools[0])}")
                    #     print(f"First tool example: {tools[0]}")
                    
                    tools_description = []
                    for i, tool in enumerate(tools):
                        try:
                            # Get tool properties
                            params = tool.inputSchema
                            desc = getattr(tool, 'description', 'No description available')
                            name = getattr(tool, 'name', f'tool_{i}')
                            
                            # Format the input schema in a more readable way
                            if 'properties' in params:
                                param_details = []
                                for param_name, param_info in params['properties'].items():
                                    param_type = param_info.get('type', 'unknown')
                                    param_details.append(f"{param_name}: {param_type}")
                                params_str = ', '.join(param_details)
                            else:
                                params_str = 'no parameters'

                            tool_desc = f"{i+1}. {name}({params_str}) - {desc}"
                            tools_description.append(tool_desc)
                            print(f"Added description for tool: {tool_desc}")
                        except Exception as e:
                            print(f"Error processing tool {i}: {e}")
                            tools_description.append(f"{i+1}. Error processing tool")
                    
                    tools_description = "\n".join(tools_description)
                    print("Successfully created tools description")
                except Exception as e:
                    print(f"Error creating tools description: {e}")
                    tools_description = "Error loading tools"
                
                print("Created system prompt...")
                
                system_prompt = f"""You are a math agent that solves problems. You have access to mathematical, canvas drawing, and email tools.

Available tools:
{tools_description}

You must respond with EXACTLY ONE line in one of these formats (no additional text):
1. For function calls:
   FUNCTION_CALL: function_name|param1|param2|...
   
2. For final completion:
   FINAL_ANSWER: [your_result]

WORKFLOW:
1. Solve the mathematical problem using math tools
2. IF the user asks to "visualize", "draw", "show on canvas", or "paint", then:
   - Open canvas using open_canvas
   - Draw rectangle using draw_rectangle with coordinates (e.g., x1=100, y1=100, x2=600, y2=200)
   - Add text with result using add_text_in_paint (text_x=110, text_y=110, text="your answer")
   - Refresh canvas using refresh_canvas to display
3. IF the user asks to "send email", "email the result", or "notify via email", then:
   - Use send-email tool with recipient_id, subject, and message containing your final answer
4. Return FINAL_ANSWER with your result

Important Rules:
- ONLY use canvas tools if user specifically requests visualization/drawing/canvas
- ONLY use email tools if user specifically requests sending email
- If no visualization or email requested, return FINAL_ANSWER immediately after calculations
- Canvas workflow when needed: open_canvas → draw_rectangle → add_text_in_paint → refresh_canvas
- Text position should be inside rectangle bounds (add ~10px padding from rectangle x1, y1)
- Include your calculated result in the text parameter
- Do not repeat function calls with the same parameters
- For send-email, use format: send-email|recipient@email.com|Subject Line|Message body with result

Examples WITHOUT visualization or email:
- FUNCTION_CALL: strings_to_chars_to_int|INDIA
- FUNCTION_CALL: int_list_to_exponential_sum|73,78,68,73,65
- FINAL_ANSWER: [8.599e+33]

Examples WITH email (if user asks):
- FUNCTION_CALL: strings_to_chars_to_int|RISHIKESH
- FUNCTION_CALL: int_list_to_exponential_sum|82,73,83,72,73,75,69,83,72
- FUNCTION_CALL: send-email|user@example.com|Calculation Result|The exponential sum result is: 1.234e+35
- FINAL_ANSWER: [1.234e+35]

DO NOT include any explanations or additional text.
Your entire response should be a single line starting with either FUNCTION_CALL: or FINAL_ANSWER:"""

                # Interactive Query Loop
                print("\n" + "="*70)
                print("🤖 AGENTIC AI ASSISTANT - Interactive Mode")
                print("="*70)
                print("\nCapabilities:")
                print("  • Mathematical calculations (ASCII, exponentials, etc.)")
                print("  • Canvas visualization")
                print("  • Email results via Gmail")
                print("\nExamples:")
                print('  "Calculate ASCII sum for HELLO"')
                print('  "Calculate ASCII sum for WORLD and visualize it"')
                print('  "Calculate ASCII sum for AI and email to me@example.com"')
                print("\nType 'quit', 'exit', or 'q' to stop.\n")
                print("="*70 + "\n")
                
                while True:
                    # Get query from user
                    try:
                        query = input("\n💬 Your Query: ").strip()
                    except (EOFError, KeyboardInterrupt):
                        print("\n\n👋 Goodbye!")
                        break
                    
                    if not query:
                        print("⚠️  Please enter a query.")
                        continue
                    
                    if query.lower() in ['quit', 'exit', 'q']:
                        print("\n👋 Goodbye!")
                        break
                    
                    # Reset state for new query
                    reset_state()
                    
                    print(f"\n🔄 Processing: {query}")
                    print("-" * 70)
                    
                    # Use global iteration variables
                    global iteration, last_response
                
                    while iteration < max_iterations:
                        print(f"\n--- Iteration {iteration + 1} ---")
                        if last_response is None:
                            current_query = query
                        else:
                            current_query = current_query + "\n\n" + " ".join(iteration_response)
                            current_query = current_query + "  What should I do next?"

                        # Get model's response with timeout
                        print("Preparing to generate LLM response...")
                        prompt = f"{system_prompt}\n\nQuery: {current_query}"
                        try:
                            response = await generate_with_timeout(client, prompt)
                            response_text = response.text.strip()
                            print(f"LLM Response: {response_text}")
                            
                            # Find the FUNCTION_CALL or FINAL_ANSWER line in the response
                            for line in response_text.split('\n'):
                                line = line.strip()
                                if line.startswith("FUNCTION_CALL:") or line.startswith("FINAL_ANSWER:"):
                                    response_text = line
                                    print(f"Extracted command: {response_text}")
                                    break
                            
                        except Exception as e:
                            print(f"Failed to get LLM response: {e}")
                            break


                        if response_text.startswith("FUNCTION_CALL:"):
                            _, function_info = response_text.split(":", 1)
                            parts = [p.strip() for p in function_info.split("|")]
                            func_name, params = parts[0], parts[1:]
                            
                            print(f"\nDEBUG: Raw function info: {function_info}")
                            print(f"DEBUG: Split parts: {parts}")
                            print(f"DEBUG: Function name: {func_name}")
                            print(f"DEBUG: Raw parameters: {params}")
                            
                            try:
                                # Find the matching tool to get its input schema
                                tool = next((t for t in tools if t.name == func_name), None)
                                if not tool:
                                    print(f"DEBUG: Available tools: {[t.name for t in tools]}")
                                    raise ValueError(f"Unknown tool: {func_name}")

                                print(f"DEBUG: Found tool: {tool.name}")
                                print(f"DEBUG: Tool schema: {tool.inputSchema}")

                                # Determine which session to use based on tool name
                                # Gmail tools: send-email, get-unread-emails, read-email, trash-email, mark-email-as-read, open-email
                                gmail_tool_names = ['send-email', 'get-unread-emails', 'read-email', 'trash-email', 
                                                   'mark-email-as-read', 'open-email']
                                
                                if func_name in gmail_tool_names:
                                    active_session = gmail_session
                                    print(f"DEBUG: Routing to Gmail session")
                                else:
                                    active_session = math_session
                                    print(f"DEBUG: Routing to Math session")

                                # Prepare arguments according to the tool's input schema
                                arguments = {}
                                schema_properties = tool.inputSchema.get('properties', {})
                                print(f"DEBUG: Schema properties: {schema_properties}")

                                for param_name, param_info in schema_properties.items():
                                    if not params:  # Check if we have enough parameters
                                        raise ValueError(f"Not enough parameters provided for {func_name}")
                                        
                                    value = params.pop(0)  # Get and remove the first parameter
                                    param_type = param_info.get('type', 'string')
                                    
                                    print(f"DEBUG: Converting parameter {param_name} with value {value} to type {param_type}")
                                    
                                    # Convert the value to the correct type based on the schema
                                    if param_type == 'integer':
                                        arguments[param_name] = int(value)
                                    elif param_type == 'number':
                                        arguments[param_name] = float(value)
                                    elif param_type == 'array':
                                        # Handle array input
                                        if isinstance(value, str):
                                            value = value.strip('[]').split(',')
                                        arguments[param_name] = [int(x.strip()) for x in value]
                                    else:
                                        arguments[param_name] = str(value)

                                print(f"DEBUG: Final arguments: {arguments}")
                                print(f"DEBUG: Calling tool {func_name} on appropriate session")
                                
                                result = await active_session.call_tool(func_name, arguments=arguments)
                                print(f"DEBUG: Raw result: {result}")
                                
                                # Get the full result content
                                if hasattr(result, 'content'):
                                    print(f"DEBUG: Result has content attribute")
                                    # Handle multiple content items
                                    if isinstance(result.content, list):
                                        iteration_result = [
                                            item.text if hasattr(item, 'text') else str(item)
                                            for item in result.content
                                        ]
                                    else:
                                        iteration_result = str(result.content)
                                else:
                                    print(f"DEBUG: Result has no content attribute")
                                    iteration_result = str(result)
                                    
                                print(f"DEBUG: Final iteration result: {iteration_result}")
                                
                                # Format the response based on result type
                                if isinstance(iteration_result, list):
                                    result_str = f"[{', '.join(iteration_result)}]"
                                else:
                                    result_str = str(iteration_result)
                                
                                iteration_response.append(
                                    f"In the {iteration + 1} iteration you called {func_name} with {arguments} parameters, "
                                    f"and the function returned {result_str}."
                                )
                                last_response = iteration_result

                            except Exception as e:
                                print(f"DEBUG: Error details: {str(e)}")
                                print(f"DEBUG: Error type: {type(e)}")
                                import traceback
                                traceback.print_exc()
                                iteration_response.append(f"Error in iteration {iteration + 1}: {str(e)}")
                                break

                        elif response_text.startswith("FINAL_ANSWER:"):
                            print("\n" + "="*70)
                            print("✅ QUERY COMPLETE")
                            print("="*70)
                            print(f"Final Answer: {response_text}")
                            print("="*70)
                            break
                        
                        else:
                            # Neither FUNCTION_CALL nor FINAL_ANSWER was detected
                            print(f"WARNING: Unexpected response format: {response_text}")
                            print("Expected FUNCTION_CALL: or FINAL_ANSWER:")
                            iteration_response.append(f"Iteration {iteration + 1} returned unexpected format")

                        iteration += 1
                    
                    # If loop completes without FINAL_ANSWER
                    if iteration >= max_iterations:
                        print("\n!!! Maximum iterations reached without FINAL_ANSWER !!!")
                        print("Iteration history:")
                        for item in iteration_response:
                            print(f"  - {item}")
                    
                    # End of query processing - loop back to ask for next query

    except Exception as e:
        print(f"\n❌ Error in main execution: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n" + "="*70)
        print("👋 Thank you for using the Agentic AI Assistant!")
        print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
    
    
