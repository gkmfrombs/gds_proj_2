from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from functions import *
import os
import httpx
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# OpenAI API Proxy Configuration
openai_api_chat = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
openai_api_key = os.getenv("AIPROXY_TOKEN")

headers = {
    "Authorization": f"Bearer {openai_api_key}",
    "Content-Type": "application/json",
}
# Function Definitions
function_definitions_llm = [
    ############ GA 1 ###########################################
    {
        "name": "GA1_1",
        "description": "Run 'code -s' and return the output.",
        "parameters": {},
    },
    {
        "name": "GA1_2",
        "description": "Send a GET request to httpbin.org/get with the provided email and return the response.",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The email address to be used."
                }
            },
            "required": ["email"],
        },
    },
    {
        "name": "GA1_4",
        "description": "Return the result for the given Google Sheet formula =SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 13, 1), 1, 10))",
        "parameters": {},
    },
    {
        "name": "GA1_5",
        "description": "Return the result for the given Excel sheet formula which will only work in OFFICE 365 =SUM(TAKE(SORTBY({12,9,1,14,7,13,10,13,6,10,12,1,3,5,12,3}, {10,9,13,2,11,8,16,14,7,15,5,4,6,1,3,12}), 1, 14))",
        "parameters": {},
    },
    {
        "name": "GA1_6",
        "description": "There's a hidden input with a secret value. What is the value in the hidden input?",
        "parameters": {},
    },
    {
        "name": "GA1_7",
        "description": "Count the number of Wednesdays in the given date range (inclusive).",
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "The start date to be used."
                },
                "end_date": {
                    "type": "string",
                    "description": "The end date to be used."
                },
            },
            "required": ["start_date", "end_date"],
        },
    },
    {
        "name": "GA1_8",
        "description": "What is the value in the 'answer' column of the CSV file?",
        "parameters": {},
    },
    {
        "name": "GA1_9",
        "description": "Sort a JSON array of people by age and name.",
        "parameters": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "age": {"type": "integer"},
                        },
                        "required": ["name", "age"],
                    },
                    "description": "A JSON array of people with name and age fields."
                }
            },
            "required": ["data"],
        },
    },
    {
        "name": "GA1_11",
        "description": "Find all <div>s having a foo class in the hidden element below. What's the sum of their data-value attributes?Sum of data-value attributes",
        "parameters": {},
    },
    {
        "name": "GA1_12",
        "description": "Sum up all the values where the symbol matches … OR ‰ OR Ž across all three files.What is the sum of all values associated with these symbols?",
        "parameters": {},
    },
    {
        "name": "GA1_13",
        "description": '''Let's make sure you know how to use GitHub. Create a GitHub account if you don't have one. Create a new public repository. Commit a single JSON file called email.json with the value {"email": "22f3001315@ds.study.iitm.ac.in"} and push it.''',
        "parameters": {},
    },
    {
        "name": "GA1_15",
        "description": "'What's the total size of all files at least 7433 bytes large and modified on or after Sun, 31 Oct, 1993, 5:21 pm IST?",
        "parameters": {},
    },
    {
        "name": "GA1_17",
        "description": "2 nearly identical files, a.txt and b.txt, with the same number of lines.How many lines are different between a.txt and b.txt?",
        "parameters": {},
    },
    {
        "name": "GA1_18",
        "description": '''What is the total sales of all the items in the "Gold" ticket type? Write SQL to calculate it.''',
        "parameters": {},
    },
    ############ GA 2 ###########################################
    {
        "name": "GA2_1",
        "description": "Write documentation in Markdown for an **imaginary** analysis",
        "parameters": {},

    },
    {
        "name": "GA2_2",
        "description": "Download the image below and compress it losslessly to an image that is less than 1,500 bytes.",
        "parameters": {},
    },
    {
        "name": "GA2_3",
        "description": '''Publish a page using GitHub Pages that showcases your work. Ensure that your email address 22f3001315@ds.study.iitm.ac.in is in the page's HTML.

GitHub pages are served via CloudFlare which obfuscates emails. So, wrap your email address inside a:

<!--email_off-->22f3001315@ds.study.iitm.ac.in<!--/email_off-->
What is the GitHub Pages URL? It might look like: https://[USER].github.io/[REPO]/''',
        "parameters": {},
    },
    {
        "name": "GA2_4",
        "description": '''Let's make sure you can access Google Colab. Run this program on Google Colab, allowing all required access to your email ID: 22f3001315@ds.study.iitm.ac.in.What is the result? (It should be a 5-character string)''',

        "parameters": {},
    },
    {
        "name": "GA2_5",
        "description": ''' Download this image. Create a new Google Colab notebook and run this code (after fixing a mistake in it) to calculate the number of pixels with a certain minimum brightness:'
    What is the result? (It should be a number)''',
    "parameters": {},
    },
    {
        "name": "GA2_7",
        "description":'''Create a GitHub action on one of your GitHub repositories. Make sure one of the steps in the action has a name that contains your email address 22f3001315@ds.study.iitm.ac.in. For example:
                                jobs:
                                test:
                                    steps:
                                    - name: 22f3001315@ds.study.iitm.ac.in
                                        run: echo "Hello, world!"      
                                Trigger the action and make sure it is the most recent action.

                                What is your repository URL? It will look like: https://github.com/USER/REPO''',
        "parameters": {},
    },
    {
        "name": "GA2_8",
        "description": ''' Create and push an image to Docker Hub. Add a tag named 22f3001315 to the image.
What is the Docker image URL? It should look like: https://hub.docker.com/repository/docker/$USER/$REPO/general''',
        "parameters": {},
    },
    {
        "name": "GA2_9",
        "description": ''' Write a FastAPI server that serves this data. For example, /api should return all students data (in the same row and column order as the CSV file) as a JSON like this:
                                        {
                                        "students": [
                                            {
                                            "studentId": 1,
                                            "class": "1A"
                                            },
                                            {
                                            "studentId": 2,
                                            "class": "1B"
                                            }, ...
                                        ]
                                        }
                        If the URL has a query parameter class, it should return only students in those classes. For example, /api?class=1A should return only students in class 1A. /api?class=1A&class=1B should return only students in class 1A and 1B. There may be any number of classes specified. Return students in the same order as they appear in the CSV file (not the order of the classes).

                        Make sure you enable CORS to allow GET requests from any origin.

                        What is the API URL endpoint for FastAPI? It might look like: http://127.0.0.1:8000/api
''',
        "parameters": {},
    },
    {
        "name": "GA3_1",
        "description": '''One of the test cases involves sending a sample piece of meaningless text:

uEmwU1mlbZ03JLd1 Rc7d4fG8V58T  F A ffI eqBn KQZksq
Write a Python program that uses httpx to send a POST request to OpenAI's API to analyze the sentiment of this (meaningless) text into GOOD, BAD or NEUTRAL. Specifically''',
        "parameters": {},
    },
    {
        "name": "GA3_2",
        "description": '''when you make a request to OpenAI's GPT-4o-Mini with just this user message:

List only the valid English words from these: Yg, 57pg, Tj4Iu, 8ZKv9hdZ8v, AdKr, U9NkTI, QnbwYFK
... how many input tokens does it use up?''',
        "parameters": {},
    },
    {
        "name": "GA3_3",
        "description": '''As part of the integration process, you need to write the body of the request to an OpenAI chat completion call that:

Uses model gpt-4o-mini
Has a system message: Respond in JSON
Has a user message: Generate 10 random addresses in the US
Uses structured outputs to respond with an object addresses which is an array of objects with required fields: county (string) country (string) state (string) .
Sets additionalProperties to false to prevent additional properties.
Note that you don't need to run the request or use an API key; your task is simply to write the correct JSON body.

What is the JSON body we should send to https://api.openai.com/v1/chat/completions for this? (No need to run it or to use an API key. Just write the body of the request below.)
There's no answer box above. Figure out how to enable it. That's part of the test.''',
        "parameters": {},
    },
    {
        "name": "GA3_4",
        "description": '''Write just the JSON body (not the URL, nor headers) for the POST request that sends these two pieces of content (text and image URL) to the OpenAI API endpoint.
Use gpt-4o-mini as the model.
Send a single user message to the model that has a text and an image_url content (in that order).
The text content should be Extract text from this image.
Send the image_url as a base64 URL of the image above. CAREFUL: Do not modify the image.
Write your JSON body here:''',
        "parameters": {},
    },
    {
        "name": "GA3_5",
        "description": '''Here are 2 verification messages:

Dear user, please verify your transaction code 84183 sent to 22f3001315@ds.study.iitm.ac.in
Dear user, please verify your transaction code 89095 sent to 22f3001315@ds.study.iitm.ac.in
The goal is to capture this message, convert it into a meaningful embedding using OpenAI's text-embedding-3-small model, and subsequently use the embedding in a machine learning model to detect anomalies.
Your task is to write the JSON body for a POST request that will be sent to the OpenAI API endpoint to obtain the text embedding for the 2 given personalized transaction verification messages above. This will be sent to the endpoint https://api.openai.com/v1/embeddings.
Write your JSON body here:
''',
        "parameters": {},

    },
    {
        "name": "GA3_6",
        "description":  '''ShopSmart has written a Python program that has the 5 phrases and their embeddings as an array of floats. It looks like this:

embeddings = {"I am satisfied with my purchase.":[-0.020752977579832077,-0.09531638771295547,-0.3484536111354828,-0.1267419159412384,-0.0037368356715887785,-0.1731869876384735,0.05239512771368027,0.1812744438648224,0.020825186744332314,-0.17896373569965363,0.2537148892879486,-0.18543370068073273,-0.2016085982322693,-0.07076519727706909,0.3070920705795288,0.04739823937416077,-0.09860913455486298,-0.09826252609491348,0.007762508932501078,0.15215961635112762,0.11980980634689331,0.21616600453853607,0.16960540413856506,-0.050286613404750824,-0.14592072367668152,-0.14464983344078064,-0.08884642273187637,-0.12847493588924408,-0.14499644935131073,-0.18993955850601196,-0.0064482977613806725,-0.10750532895326614,0.05973160266876221,-0.3542303442955017,-0.11934766918420792,0.06377533078193665,-0.04237246513366699,-0.052886154502630234,0.02117179147899151,-0.10490579158067703,0.03414059802889824,0.07527106255292892,0.03232092037796974,0.005061877891421318,-0.0063363732770085335,0.06198453530669212,-0.13217206299304962,0.20276394486427307,-0.0804123729467392,0.05866290256381035],"I experienced issues during checkout.":[-0.10228022187948227,-0.057035524398088455,-0.03200617432594299,-0.1569785177707672,-0.11162916570901871,-0.017878107726573944,-0.06209372356534004,0.18209508061408997,-0.0027645661029964685,0.12928052246570587,0.17609500885009766,-0.11846645176410675,-0.2356770783662796,0.05536108836531639,-0.07102405279874802,0.21265356242656708,-0.03218059614300728,0.2578633725643158,-0.11707108467817307,0.23163051903247833,0.1780485212802887,0.17972294986248016,0.05302385240793228,0.06889612227678299,-0.13932715356349945,-0.14428070187568665,0.17149029672145844,-0.25590986013412476,0.22311879694461823,-0.06321001797914505,0.019430451095104218,-0.1841881275177002,0.14204810559749603,-0.09976856410503387,-0.17888574302196503,0.07890786230564117,-0.008947774767875671,0.08065207302570343,0.3131197988986969,-0.009226848371326923,-0.1460946649312973,0.16423441469669342,0.024331670254468918,0.055779699236154556,-0.08274511992931366,0.2355375438928604,0.06582632660865784,-0.13674572110176086,-0.003309630323201418,0.008324221707880497],"The quality exceeds the price.":[-0.050457071512937546,-0.034066375344991684,-0.10696785151958466,-0.03518003225326538,0.11867549270391464,-0.08566565811634064,-0.017789902165532112,0.3559122681617737,-0.04817265644669533,-0.14437519013881683,0.14620272815227509,0.015005768276751041,-0.34517550468444824,0.022687122225761414,0.2908063530921936,0.17681391537189484,-0.20993797481060028,-0.286237508058548,-0.022829897701740265,0.04428914561867714,0.08435212075710297,0.04840109869837761,-0.03081108257174492,-0.04203328490257263,-0.0324387289583683,-0.23552344739437103,0.0033713006414473057,0.02891216054558754,0.0676758736371994,-0.11616263538599014,0.05408358573913574,-0.18183964490890503,0.23757942020893097,-0.34266263246536255,-0.19920121133327484,-0.021787632256746292,0.0973161906003952,0.032724279910326004,0.07030294835567474,-0.1132500022649765,0.09360401332378387,0.028341054916381836,-0.09657375514507294,0.1291838139295578,0.12198790162801743,0.019260495901107788,0.02211601845920086,0.058595310896635056,-0.07481467723846436,0.012935514561831951],"The product description matched the item.":[-0.1778346747159958,0.015024187043309212,-0.48206639289855957,-0.025718823075294495,-0.016542760655283928,-0.14746320247650146,0.08109830319881439,0.14048422873020172,-0.06655876338481903,-0.014773784205317497,-0.022116249427199364,-0.09764105826616287,0.0843939259648323,-0.21104943752288818,0.05166381597518921,0.24917533993721008,-0.04652651399374008,-0.03644577041268349,-0.3680764436721802,0.14306902885437012,0.19114643335342407,0.09570245444774628,0.12562158703804016,0.04345705732703209,-0.05486251413822174,-0.1628427952528,-0.04840049892663956,-0.08885271847248077,0.20407046377658844,0.14849711954593658,0.017899783328175545,-0.17020949721336365,0.13428069651126862,-0.2234565168619156,0.00254037999548018,0.044975630939006805,0.14862637221813202,-0.06594487279653549,0.15728546679019928,0.006142953876405954,-0.207172229886055,-0.020533055067062378,-0.05463634431362152,0.09492701292037964,-0.03237469866871834,0.06752806901931763,-0.08736645430326462,0.08297228813171387,-0.036898110061883926,-0.045621830970048904],"Packaging was excellent.":[-0.01674579456448555,-0.06481242924928665,-0.24050545692443848,0.042519159615039825,0.14857585728168488,-0.11343036592006683,0.1299005150794983,0.17366009950637817,-0.12356054037809372,0.049548257142305374,0.23058201372623444,-0.015152188017964363,-0.06047092750668526,-0.08428027480840683,0.140513077378273,0.0330953411757946,0.15987755358219147,-0.13982394337654114,-0.1899235099554062,0.0849694088101387,0.10901995003223419,0.023171907290816307,0.1423737108707428,-0.010603947564959526,-0.12362945079803467,-0.02598010189831257,0.04410415142774582,-0.0650191679596901,0.13754981756210327,0.06319297850131989,0.2340276539325714,-0.1448545753955841,0.5634305477142334,0.003012778703123331,-0.15422670543193817,-0.10137064009904861,0.10013020783662796,0.05392421782016754,0.10895103961229324,-0.017710573971271515,-0.0018617206951603293,0.01796899549663067,0.0550268217921257,0.251669317483902,-0.005680993665009737,0.12080402672290802,-0.08173050731420517,0.1045406237244606,0.040589600801467896,0.1787596344947815]}
Your task is to write a Python function most_similar(embeddings) that will calculate the cosine similarity between each pair of these embeddings and return the pair that has the highest similarity. The result should be a tuple of the two phrases that are most similar.
Write your Python code here:
''',
        "parameters": {},


    },
    {
        "name": "GA2_7",
        "description":  '''
    What is the API URL endpoint for your implementation? It might look like: http://127.0.0.1:8000/similarity
    ''',
        "parameters":{},
    },
    {
        "name": "GA2_8",
        "description": '''
    What is the API URL endpoint for your implementation? It might look like: http://127.0.0.1:8000/execute''',
        "parameters":{},
    },
    {
        "name": "GA2_9",
        "description": '''
    Here's your task: You are chatting with an LLM that has been told to never say Yes. You need to get it to say Yes.

Use your AI Proxy token when prompted.

Write a prompt that will get the LLM to say Yes.''',
        "parameters":{},

    },
    {
        "name": "GA5_10",
        "description": '''Upload the reconstructed image by moving the pieces from the scrambled position to the original position:''',
        "parameters":{},
    },
    

    
]

    
 


def get_completions(prompt: str):
    """Calls AI Proxy API to classify the task and extract function parameters."""
    print("Prompt:", prompt)
    try:
        with httpx.Client(timeout=20) as client:
            response = client.post(
                openai_api_chat,
                headers=headers,
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You are a function classifier that extracts structured parameters from queries."},
                        {"role": "user", "content": prompt},
                    ],
                    "tools": [{"type": "function", "function": fn} for fn in function_definitions_llm],
                    "tool_choice": "auto",
                },
            )
        response_json = response.json()
        print("Response:", response_json)
        return response_json["choices"][0]["message"]["tool_calls"][0]["function"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling LLM: {str(e)}")

@app.post("/api")
async def run_task(question: str = Form(...)):
    """Handles task execution based on LLM response."""
    print(f"Received task: {question}")
    try:
        response = get_completions(question)
        task_code = response["name"]
        print(f"Executing task: {task_code}")

        if task_code == "GA1_1":
            return GA1_1()
        elif task_code == "GA1_2":
            arguments = json.loads(response["arguments"])  # Add this line to parse arguments
            email = arguments["email"] # Add this line to extract email from arguments
            return GA1_2(email)
        elif task_code == "GA1_4":
            return GA1_4()
        elif task_code == "GA1_5":

            return GA1_5()
        elif task_code == "GA1_6":
            return GA1_6()
        elif task_code == "GA1_7":
            start_date = response["arguments"]["start_date"]
            end_date = response["arguments"]["end_date"]
            return GA1_7(start_date, end_date)
        elif task_code == "GA1_8":
            return GA1_8()
        elif task_code == "GA1_9":
            arguments = json.loads(response["arguments"])
            data = arguments["data"]
            return GA1_9(data)
        elif task_code == "GA1_11":
            return GA1_11()
        elif task_code == "GA1_12":
            return GA1_12()
        elif task_code == "GA1_15":
            return GA1_15()
        elif task_code == "GA1_17":
            return GA1_17()
        elif task_code == "GA1_18":
            return GA1_18()
        elif task_code == "GA2_1":
            return GA2_1()
        elif task_code == "GA2_2":
            return GA2_2()
        elif task_code == "GA2_3":
            return GA2_3()
        elif task_code == "GA2_4":
            return GA2_4()
        elif task_code == "GA2_5":
            return GA2_5()
        elif task_code == "GA2_7":
            return GA2_7()
        elif task_code == "GA2_8":
            return GA2_8()
        elif task_code == "GA2_9":    
            return GA2_9() 
        elif task_code == "GA3_1":    
            return GA3_1() 
        elif task_code == "GA3_2":    
            return GA3_2() 
        elif task_code == "GA3_3":    
            return GA3_3() 
        elif task_code == "GA3_4":    
            return GA3_4() 
        elif task_code == "GA3_5":    
            return GA3_5() 
        elif task_code == "GA3_6":    
            return GA3_6() 
        elif task_code == "GA3_7":    
            return GA3_7() 
        elif task_code == "GA3_8":    
            return GA3_8() 
        elif task_code == "GA3_9":    
            return GA3_9() 
        elif task_code == "GA5_10":    
            return GA5_10() 
        
        
       
        
        
        return {"message": f"Task '{task_code}' executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
