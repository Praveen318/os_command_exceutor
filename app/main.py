from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import subprocess
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model=genai.GenerativeModel(
model_name="gemini-1.5-flash",
system_instruction="You are chatbot which only gives os command for mac os according to user request and nothing else. You don't answer about anything else")

class CommandRequest(BaseModel):
    user_prompt: str

@app.post("/execute")
async def execute_command(request: CommandRequest):
    user_prompt = request.user_prompt

    # Use GPT to interpret the user's prompt
    prompt=f"User prompt: {user_prompt}\n\nDetermine the appropriate OS command"
    
    gpt_response = model.generate_content(f"{prompt}")
    response_text = gpt_response.text.strip()
    print(response_text)
    try:
        result = execute_os_command(response_text)
        print(result)
        return {"command": response_text, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def execute_os_command(command):
    # Execute the command using subprocess
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return result.strip()  # Strip trailing newlines and spaces
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.output.strip()}"
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import os
# import subprocess
# import google.generativeai as genai
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv, find_dotenv
# from googleapiclient.discovery import build

# _ = load_dotenv(find_dotenv())  # read local .env file
# genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# # Google Custom Search API configuration
# GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
# # <script async src="https://cse.google.com/cse.js?cx=24ed70d8d42884e87">
# # </script>
# # <div class="gcse-search"></div>
# SEARCH_ENGINE_ID = os.environ['SEARCH_ENGINE_ID']

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust as needed
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# model = genai.GenerativeModel(
#     model_name="gemini-1.5-flash",
#     system_instruction="You are a chatbot that only gives OS commands according to user requests for mac os and nothing else. You don't answer about anything else."
# )

# class CommandRequest(BaseModel):
#     user_prompt: str

# @app.post("/execute")
# async def execute_command(request: CommandRequest):
#     user_prompt = request.user_prompt

#     # Use GPT to interpret the user's prompt
#     prompt = f"User prompt: {user_prompt}\n\nDetermine the appropriate OS command"
    
#     gpt_response = model.generate_content(f"{prompt}")
#     response_text = gpt_response.text.strip()
#     print(response_text)
#     try:
#         result = execute_os_command(response_text)
#         print(result)
#         return {"command": response_text, "result": result}
#     except Exception as e:
#         error_message = str(e)
#         print(f"Error: {error_message}")
        
#         # Search for a solution to the error
#         solution = search_for_solution(error_message)
#         if solution:
#             try:
#                 solution_result = execute_os_command(solution)
#                 return {
#                     "command": response_text,
#                     "error": error_message,
#                     "solution": solution,
#                     "solution_result": solution_result
#                 }
#             except Exception as e:
#                 raise HTTPException(status_code=500, detail=f"Error executing solution: {str(e)}")
#         else:
#             raise HTTPException(status_code=500, detail=error_message)

# def execute_os_command(command):
#     # Execute the command using subprocess
#     try:
#         result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
#         return result.strip()  # Strip trailing newlines and spaces
#     except subprocess.CalledProcessError as e:
#         raise Exception(f"Error executing command: {e.output.strip()}")

# def search_for_solution(error_message):
#     # Initialize the Custom Search API
#     service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)

#     # Perform the search
#     res = service.cse().list(
#         q=error_message,
#         cx=SEARCH_ENGINE_ID,
#     ).execute()

#     # Extract the snippet from the first result (or more results as needed)
#     try:
#         search_results = res['items']
#         for item in search_results:
#             snippet = item['snippet']
#             # Simple heuristic to determine if snippet contains a command
#             if 'sudo' in snippet or 'apt' in snippet or 'yum' in snippet:
#                 return snippet.split('\n')[0]  # Return the first line of the snippet
#     except KeyError:
#         return None  # No results found

#     return None

