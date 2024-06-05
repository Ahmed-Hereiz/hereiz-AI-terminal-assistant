from utils import add_root_to_path
from langchain_google_genai import ChatGoogleGenerativeAI
from utils import add_root_to_path
hereiz_root = add_root_to_path()

from common.utils import load_config, parse_safety_settings
from helpers import extract_json_from_string
from modules.Tools import (
    PDFDocReader,
    GithubAccountScraper,
    SearchManager
)


config = load_config(f'{hereiz_root}/config/llm.json')
safety_settings = parse_safety_settings(config['safety_settings'])

llm = ChatGoogleGenerativeAI(
    google_api_key=config['api_key'],
    model=config['model'],
    temperature=0.7,
    safety_settings=safety_settings
)

read_pdf_tool = PDFDocReader()
scrape_tool = GithubAccountScraper()
# search_tool = SearchManager()


prompt = """
You run in a loop of Thought, Action, PAUSE, Action_Response.
At the end of the loop you output an Answer.
Use Thought to understand the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Action_Response will be the result of running those actions.

Your available actions are:
read_pdf_tool:
e.g. read_pdf_tool: resume.pdf
Returns md file of the resume.pdf
scrape_github_tool:
e.g. scrape_github_tool: username
Returns md file of scraped github account

your role is : Personal Profiler for Engineers
your goal is : to take the user portfolio based on the user resume and his github account data, and the user will give you the job description so make the best profile for the user
your output is : the new resume based on the job deescription and the user profile as the md file, make the output near the size of the user resume.pdf you have to just remake it in a better way
make sure that : you choose only the needed informations for the job requirments not all the informations in the resume where you don't choose all the projects in the resume or all the keywords,
you have to remake the new resume with the best way to match the job requirments make much changes on the old one and use the resume and the github account both of them to get better data for the pojects.

Example session:
job_description:
We are looking for a highly skilled Machine Learning Engineer to join our team. The ideal candidate will have a strong background in machine learning, data science, and software development. You will be responsible for developing machine learning models, creating data pipelines, and collaborating with cross-functional teams to deliver cutting-edge AI solutions.

Responsibilities:
- Design, develop, and deploy machine learning models
- Collaborate with data scientists and engineers to build data pipelines
- Analyze large datasets to derive insights and inform decisions
- Optimize and fine-tune algorithms for performance and scalability
- Stay up-to-date with the latest research and advancements in machine learning

Requirements:
- Bachelor's or Master's degree in Computer Science, Engineering, or related field
- 3+ years of experience in machine learning and data analysis
- Proficiency in Python and experience with frameworks such as TensorFlow, PyTorch, or Scikit-learn
- Strong understanding of statistical analysis and modeling techniques
- Experience with cloud platforms such as AWS, GCP, or Azure
- Excellent problem-solving skills and ability to work in a team environment

user data:
Github:github-username
resume:resume.pdf

Thought: I need to gather the user's resume data and their GitHub account information to create the best profile for the Machine Learning Engineer job description provided. First, I will request the user's resume file and GitHub username.
Action: 
{
  "function_name": "scrape_github_tool",
  "function_parms": {
    "url": "github-username"
  }
}
PAUSE

You will be called again with this:
Action_Response: 'returned md from scrape_github_tool the md file'

Thought: Now that I have the user's resume and GitHub information, I will create a tailored profile highlighting the user's experience and skills relevant to the Machine Learning Engineer position.
Action: 
{
  "function_name": "read_pdf_tool",
  "function_parms": {
    "url": "resume.pdf"
  }
}
PAUSE

You will be called again with this:
Action_Response: 'returned md from scrape_github_tool, read_pdf_tool'

You then output:
New Resume :
'the new resume with near the size of the resume.pdf file remaked to make high chance of job acceptance'

job_description: 
"""


query = """
Position: AI Engineer

We are seeking a talented AI Engineer to join our dynamic team. The successful candidate will have a strong foundation in artificial intelligence, machine learning, and software development. You will be responsible for building AI models, designing AI algorithms, and collaborating with various teams to integrate AI solutions into our products.

Responsibilities:
- Develop and deploy AI models and algorithms
- Collaborate with software engineers and data scientists to integrate AI solutions
- Research and implement state-of-the-art AI techniques
- Analyze and preprocess data for AI applications
- Optimize AI models for performance and scalability

Requirements:
- Bachelor's or Master's degree in Computer Science, Engineering, or related field
- 3+ years of experience in AI and machine learning
- Proficiency in Python and AI frameworks such as TensorFlow, PyTorch, or Keras
- Strong understanding of neural networks, deep learning, and natural language processing
- Experience with cloud platforms like AWS, GCP, or Azure
- Excellent problem-solving skills and the ability to work in a collaborative environment

user data:
Github:Ahmed-Hereiz
Resume:Ahmed_Hany Hereiz_Resume_.pdf
"""


available_actions = {
    "scrape_github_tool": GithubAccountScraper().scrape_tool,
    "read_pdf_tool":PDFDocReader().extract_text_from_pdf
}

prompt += query

for step in range(5):
    print(prompt)
    print(f"step : {step}")
    print("-"*100)

    llm_response = llm.predict(prompt)
    print(llm_response)
    prompt += f"\n{llm_response}"
    extracted_json = extract_json_from_string(llm_response)

    if len(extracted_json) > 0:
        function_name = extracted_json[0]['function_name']
        function_parms = extracted_json[0]['function_parms']
        if function_name not in available_actions:
            raise Exception(f"Unknown action: {function_name}")
        
        print(f" -- running {function_name} {function_parms}")
        action_function = available_actions[function_name]
        result = f"\nAction_Response: {action_function(*function_parms.values())}"
        prompt += result
    else:
        break