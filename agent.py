import os
import requests
from google import genai
from google.genai import types

# Computer must be on the SAME Wi-Fi network as the ESP32.
ESP32_IP = os.getenv("ESP32_IP", "172.20.10.3")
AUTH_TOKEN = os.getenv("DEVICE_SECRET", "workshop-secret-2026")
MODEL = "gemini-3.5-flash"

# GEMINI_API_KEY must be set before running this program.
client = genai.Client()


#Esp32 tool execution 

def call_esp32_tool(name: str, args: dict) -> dict:
    """
    Executes the tool requested by Gemini.

    Gemini decides WHAT it wants to do.
    This function decides HOW to send that command to the ESP32.
    """

    try:

      
        # Tool 1: Control LED
       
        if name == "control_led":

            payload = {
                "state": str(args.get("state", "off")).lower(),
                "duration_ms": int(args.get("duration_ms", 0)),
            }

            r = requests.post(
                f"http://{ESP32_IP}/led",
                json=payload,
                headers={
                    "X-Device-Auth": AUTH_TOKEN
                },
                timeout=8,
            )

     
        # Tool 2: Get ESP32 status
  
        elif name == "get_device_status":

            r = requests.get(
                f"http://{ESP32_IP}/status",
                timeout=3
            )

   
        # Unknown tool
  
        else:
            return {
                "error": f"Unknown tool: {name}"
            }

        return {
            "http_status": r.status_code,
            "body": r.text
        }

    except requests.RequestException as e:

        return {
            "error": f"ESP32 unreachable: {e}"
        }



# Define tools used by Gemini 


esp32_tools = types.Tool(
    function_declarations=[

     
        # control_led()
    
        types.FunctionDeclaration(
            name="control_led",

            description=(
                "Turns the ESP32 LED on or off, "
                "or pulses it briefly."
            ),

            parameters=types.Schema(
                type="OBJECT",

                properties={

                    "state": types.Schema(
                        type="STRING",
                        enum=["on", "off"],
                        description="Whether the LED should be on or off.",
                    ),

                    "duration_ms": types.Schema(
                        type="INTEGER",
                        description=(
                            "0 means stay in the requested state. "
                            "1-5000 means pulse for that many milliseconds."
                        ),
                    ),
                },

                required=["state"],
            ),
        ),

  
        # get_device_status()
 
        types.FunctionDeclaration(
            name="get_device_status",

            description=(
                "Checks whether the ESP32 is online "
                "and returns its status and uptime."
            ),
        ),
    ]
)


# Give Gemini access to the ESP32 tools.
config = types.GenerateContentConfig(
    tools=[esp32_tools]
)



# Conversation history

contents = []


print("==========================================")
print("      Gemini ESP32 Hardware Agent")
print("==========================================")
print()
print("Examples:")
print("  Is the ESP32 online?")
print("  Blink the LED for 500 milliseconds.")
print("  Turn the LED on.")
print("  Turn the light off.")
print()
print("Type 'quit' or 'exit' to stop.")
print()



# INTERACTIVE CHAT LOOP
while True:
    prompt = input("You: ").strip()
    # Exit command


    if prompt.lower() in ["quit", "exit"]:
        print("\nGoodbye!")
        break

    # Ignore empty input.
    if not prompt:
        continue


    # Add user's message to conversation history


    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part(text=prompt)
            ]
        )
    )


  
    # Gemini tool calling loop
  
    # Gemini may need more than one tool call before it can produce its final answer.
    for _ in range(5):

        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config
        )


       
        # CASE 1:
        # Gemini does NOT need another ESP32 tool.
        if not response.function_calls:

            print("\nGemini:")
            print(response.text)
            print()

            #Gemini's final response in conversation history for future context
            if response.candidates:
                contents.append(
                    response.candidates[0].content
                )

            break


        # CASE 2:
        # Gemini wants to call ESP32 tool(s).

        # Keep Gemini's function-call message in history.
        contents.append(
            response.candidates[0].content
        )


        result_parts = []


        # Gemini may request multiple tools.
        for fc in response.function_calls:

            args = dict(fc.args or {})
            print("\nGemini wants:")

            if args:

                print(f"{fc.name}(")

                items = list(args.items())

                for index, (key, value) in enumerate(items):

                    comma = "," if index < len(items) - 1 else ""

                    print(
                        f"    {key}={value!r}{comma}"
                    )

                print(")")

            else:

                print(f"{fc.name}()")


            # Execute command on ESP32
       
            result = call_esp32_tool(
                fc.name,
                args
            )


            print("\nESP32:")

            if "error" in result:

                print(result["error"])

            else:

                # Print the ESP32 response body to make
                print(result["body"])


       
            # Send the ESP32 result back to Gemini

            result_parts.append(

                types.Part(

                    function_response=
                    types.FunctionResponse(
                        id=fc.id,
                        name=fc.name,
                        response=result,
                    )
                )
            )


        # Add tool results to conversation history.
        contents.append(

            types.Content(
                role="user",
                parts=result_parts
            )
        )

    else:

        print(
            "\nGemini used too many tool steps. "
            "Please try a simpler command.\n"
        )
