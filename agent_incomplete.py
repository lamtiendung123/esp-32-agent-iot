import os
import requests
from google import genai
from google.genai import types


# Workshop Part 1
# Configure the ESP32 and Gemini


# TODO 1
# Fill in the name of the environment variable that stores the ESP32 IP
ESP32_IP = os.getenv("________________", "172.20.10.3")


# TODO 2
# Fill in the environment variable for the ESP32 authentication secret
AUTH_TOKEN = os.getenv("________________", "workshop-secret-2026")


# TODO 3
# Fill in the Gemini model name
MODEL = "________________"


# Gemini uses GEMINI_API_KEY from your environment
client = genai.Client()



# Workshop Part 2
# Create the function that connects Gemini tools to the ESP32


def call_esp32_tool(name: str, args: dict) -> dict:

    try:

        # TODO 4
        # Fill in the tool name used to control the LED
        if name == "________________":

            # TODO 5
            # Read the LED state requested by Gemini
            state = str(
                args.get("________________", "off")
            ).lower()


            # TODO 6
            # Read the duration requested by Gemini
            duration = int(
                args.get("________________", 0)
            )


            payload = {
                "state": state,
                "duration_ms": duration,
            }


            # TODO 7
            # Which HTTP method should be used to send a command
            r = requests.________________(
                f"http://{ESP32_IP}/led",
                json=payload,
                headers={
                    "X-Device-Auth": AUTH_TOKEN
                },
                timeout=8,
            )


        # TODO 8
        # Fill in the status tool name
        elif name == "________________":

            # TODO 9
            # Which HTTP method should be used to read device information
            r = requests.________________(
                f"http://{ESP32_IP}/status",
                timeout=3
            )


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



# Workshop Part 3
# Describe the tools that Gemini is allowed to request


esp32_tools = types.Tool(

    function_declarations=[


        # TODO 10
        # Give Gemini the name of the LED tool

        types.FunctionDeclaration(

            name="________________",

            description=(
                "Turns the ESP32 LED on or off, "
                "or pulses it briefly."
            ),

            parameters=types.Schema(

                type="OBJECT",

                properties={

                    # TODO 11
                    # Fill in the parameter used for on and off

                    "________________": types.Schema(
                        type="STRING",
                        enum=["on", "off"],
                        description="Whether the LED should be on or off.",
                    ),


                    # TODO 12
                    # Fill in the parameter used for pulse time

                    "________________": types.Schema(
                        type="INTEGER",

                        description=(
                            "0 means stay in the requested state. "
                            "1 to 5000 means pulse for that many milliseconds."
                        ),
                    ),
                },


                # TODO 13
                # Which argument must Gemini always provide

                required=[
                    "________________"
                ],
            ),
        ),



        # TODO 14
        # Create the device status tool

        types.FunctionDeclaration(

            name="________________",

            description=(
                "Checks whether the ESP32 is online "
                "and returns its status and uptime."
            ),
        ),
    ]
)



# Workshop Part 4
# Give the tools to Gemini


# TODO 15
# Fill in the tool variable Gemini should receive

config = types.GenerateContentConfig(

    tools=[
        ________________
    ]
)



# Workshop Part 5
# Create conversation memory


# TODO 16
# What Python data structure should store conversation history

contents = ________________



# Workshop Part 6
# Print the user interface


print("Gemini ESP32 Hardware Agent")
print()
print("Try commands such as:")
print("Is the ESP32 online?")
print("Blink the LED for 500 milliseconds.")
print("Turn the LED on.")
print("Turn the light off.")
print()
print("Type 'quit' or 'exit' to stop.")
print()



# Workshop Part 7
# Create the interactive chat


# TODO 17
# Fill in the Python loop that keeps the program running

while ________________:


    # TODO 18
    # Ask the participant for natural language input

    prompt = input("________________").strip()


    # TODO 19
    # Check whether the participant wants to exit

    if prompt.lower() in [
        "________________",
        "________________"
    ]:

        print("\nGoodbye!")

        # TODO 20
        # Stop the loop
        ________________



    # Ignore empty input

    if not prompt:

        # TODO 21
        # Go back to the beginning of the loop
        ________________



    # Workshop Part 8
    # Add the user's message to Gemini's conversation history


    contents.append(

        types.Content(

            # TODO 22
            # Fill in the role

            role="________________",

            parts=[

                # TODO 23
                # Pass the participant's prompt into Gemini

                types.Part(
                    text=________________
                )
            ]
        )
    )



    # Workshop Part 9
    # Let Gemini reason and call tools


    for _ in range(5):


        # TODO 24
        # Ask Gemini to process the conversation

        response = client.models.________________(

            model=MODEL,

            contents=________________,

            config=________________
        )



        # Workshop Part 10
        # Check whether Gemini needs an ESP32 tool


        # TODO 25
        # Fill in the property that contains Gemini tool requests

        if not response.________________:


            print("\nGemini:")

            print(response.text)

            print()


            # Save Gemini's response for future context

            if response.candidates:

                contents.append(

                    response.candidates[0].content
                )


            break



        # Workshop Part 11
        # Save Gemini's function call in conversation history


        contents.append(

            response.candidates[0].content
        )


        result_parts = []



        # Workshop Part 12
        # Execute every tool Gemini requested


        # TODO 26
        # Loop through Gemini's function calls

        for fc in response.________________:


            # TODO 27
            # Convert Gemini arguments into a Python dictionary

            args = dict(
                fc.________________ or {}
            )


            print("\nGemini wants:")



            if args:

                print(f"{fc.name}(")

                items = list(
                    args.items()
                )


                for index, (key, value) in enumerate(items):


                    comma = "," if index < len(items) - 1 else ""


                    print(
                        f"    {key}={value!r}{comma}"
                    )


                print(")")


            else:

                print(
                    f"{fc.name}()"
                )



            # Workshop Part 13
            # Send Gemini's requested action to the ESP32


            # TODO 28
            # Call the function that communicates with the ESP32

            result = ________________(
                fc.name,
                args
            )



            print("\nESP32:")



            if "error" in result:

                print(
                    result["error"]
                )


            else:

                # TODO 29
                # Print the response body returned by the ESP32

                print(
                    result["________________"]
                )



            # Workshop Part 14
            # Send the ESP32 result back to Gemini


            result_parts.append(

                types.Part(

                    function_response=
                    types.FunctionResponse(

                        # TODO 30
                        # Match Gemini's function call ID

                        id=fc.________________,

                        # TODO 31
                        # Send the function name back to Gemini

                        name=fc.________________,

                        # TODO 32
                        # Send the ESP32 result back to Gemini

                        response=________________,
                    )
                )
            )



        # Workshop Part 15
        # Add ESP32 tool results to conversation memory


        contents.append(

            types.Content(

                # Tool results are returned to Gemini

                role="user",

                # TODO 33
                # Insert all tool results

                parts=________________
            )
        )


    else:

        print(
            "\nGemini used too many tool steps. "
            "Please try a simpler command.\n"
        )