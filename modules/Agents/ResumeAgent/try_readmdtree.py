from utils import add_root_to_path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
hereiz_root = add_root_to_path()

from common.utils import load_config, parse_safety_settings
from helpers import extract_json_from_string, replace_input_sentence

config = load_config(f'{hereiz_root}/config/llm.json')
safety_settings = parse_safety_settings(config['safety_settings'])

llm = ChatGoogleGenerativeAI(
    google_api_key=config['api_key'],
    model=config['model'],
    temperature=0.7,
    safety_settings=safety_settings
)


prompt = """
you will be given a tree of dirs and files from a user of his project and you task
is too see the files and dirs from the user and choose which dirs and files are important 
and select them where this files will be given to another AI model so he can write readme file
for this files and dirs so your task is to classify the important files and dirs for the user.
note that you take prompt from user where he tells you what does he need you to focus on.

your max output should be atmost 5 files and 5 dirs (the most important one)


{input}

"""

query = """
.
├── assets
├── common
│   ├── __init__.py
│   ├── manage_memory.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── manage_memory.cpython-310.pyc
│   │   └── utils.cpython-310.pyc
│   └── utils.py
├── config
│   ├── llm.json
│   ├── settings.json
│   └── terminal.json
├── data
│   ├── history
│   │   ├── memory
│   │   │   └── chat_memory_buffer
│   │   └── search
│   │       └── search_history.txt
│   └── tmp
├── docs
│   └── Future_updated.md
├── fonts
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   └── terminal_out_customize.cpython-310.pyc
│   └── terminal_out_customize.py
├── helpers
│   ├── fetch_data.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── fetch_data.cpython-310.pyc
│   │   ├── __init__.cpython-310.pyc
│   │   └── reformat_strings.cpython-310.pyc
│   └── reformat_strings.py
├── hereiz
├── logs
│   └── hereiz.logs
├── log.sh
├── modules
│   ├── Agents
│   │   ├── base.py
│   │   ├── CodeAgent
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── base.cpython-310.pyc
│   │   │   └── __init__.cpython-310.pyc
│   │   ├── ResumeAgent
│   │   │   ├── dummy.py
│   │   │   ├── __init__.py
│   │   │   ├── ProfilerAgent.py
│   │   │   ├── __pycache__
│   │   │   │   └── utils.cpython-310.pyc
│   │   │   ├── ReasercherAgent.py
│   │   │   ├── ResumeMakerRuntime.py
│   │   │   ├── ResumeMakerTools.py
│   │   │   ├── StrategistAgent.py
│   │   │   ├── try_agentloop.py
│   │   │   ├── try_humanloop.py
│   │   │   ├── try_scrapeurl.py
│   │   │   └── utils.py
│   │   └── SearchAgent
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   ├── __init__.cpython-310.pyc
│   │       │   ├── SearcherAgent.cpython-310.pyc
│   │       │   ├── SearcherRuntime.cpython-310.pyc
│   │       │   ├── SearcherTools.cpython-310.pyc
│   │       │   └── utils.cpython-310.pyc
│   │       ├── SearcherAgent.py
│   │       ├── SearcherRuntime.py
│   │       ├── SearcherTools.py
│   │       └── utils.py
│   ├── Models
│   │   ├── base.py
│   │   ├── ChainModel.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── Agents.cpython-310.pyc
│   │   │   ├── base.cpython-310.pyc
│   │   │   ├── ChainModel.cpython-310.pyc
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── SummarizeModel.cpython-310.pyc
│   │   │   └── SummerizeModel.cpython-310.pyc
│   │   ├── SummarizeModel.py
│   │   └── utils.py
│   └── Tools
│       ├── base.py
│       ├── __init__.py
│       ├── MakeSearchTool.py
│       ├── __pycache__
│       │   ├── base.cpython-310.pyc
│       │   ├── __init__.cpython-310.pyc
│       │   ├── MakeSearchTool.cpython-310.pyc
│       │   ├── manage_search.cpython-310.pyc
│       │   ├── ModelToolBase.cpython-310.pyc
│       │   ├── ReadDocTool.cpython-310.pyc
│       │   ├── ScrapeGithubTool.cpython-310.pyc
│       │   ├── SummarizeSearchTool.cpython-310.pyc
│       │   ├── SummerizeSearchTool.cpython-310.pyc
│       │   └── utils.cpython-310.pyc
│       ├── ReadDocTool.py
│       ├── ScrapeGithubTool.py
│       ├── SummarizeSearchTool.py
│       └── utils.py
├── README.md
├── requirments.txt
├── scripts
│   ├── manage_logs.sh
│   ├── manage_memory.sh
│   ├── manage_search.sh
│   ├── manage_templates.sh
│   ├── run_ask.sh
│   ├── run_chat.sh
│   └── run_search.sh
├── src
│   ├── features
│   │   ├── Ask
│   │   │   ├── __init__.py
│   │   │   ├── __main__.py
│   │   │   ├── model_ask.py
│   │   │   ├── __pycache__
│   │   │   │   ├── ask.cpython-310.pyc
│   │   │   │   ├── __init__.cpython-310.pyc
│   │   │   │   ├── __main__.cpython-310.pyc
│   │   │   │   ├── model_ask.cpython-310.pyc
│   │   │   │   ├── run_ask.cpython-310.pyc
│   │   │   │   └── utils.cpython-310.pyc
│   │   │   ├── run_ask.py
│   │   │   └── utils.py
│   │   ├── Chat
│   │   │   ├── __init__.py
│   │   │   ├── __main__.py
│   │   │   ├── model_chat.py
│   │   │   ├── __pycache__
│   │   │   │   ├── ask.cpython-310.pyc
│   │   │   │   ├── chat.cpython-310.pyc
│   │   │   │   ├── __init__.cpython-310.pyc
│   │   │   │   ├── __main__.cpython-310.pyc
│   │   │   │   ├── model_chat.cpython-310.pyc
│   │   │   │   ├── run_chat.cpython-310.pyc
│   │   │   │   └── utils.cpython-310.pyc
│   │   │   ├── run_chat.py
│   │   │   └── utils.py
│   │   ├── Code
│   │   │   ├── agents_code.py
│   │   │   ├── Agents.py
│   │   │   ├── __init__.py
│   │   │   ├── Parsers.py
│   │   │   └── __pycache__
│   │   │       ├── Agents.cpython-310.pyc
│   │   │       └── Parsers.cpython-310.pyc
│   │   └── Search
│   │       ├── __init__.py
│   │       ├── __main__.py
│   │       ├── __pycache__
│   │       │   ├── __main__.cpython-310.pyc
│   │       │   ├── manage_search.cpython-310.pyc
│   │       │   ├── run_fullsearch.cpython-310.pyc
│   │       │   ├── run_search_agent.cpython-310.pyc
│   │       │   ├── run_search.cpython-310.pyc
│   │       │   ├── run_search_model.cpython-310.pyc
│   │       │   ├── run_searchopen.cpython-310.pyc
│   │       │   ├── search_bot.cpython-310.pyc
│   │       │   ├── search_manage.cpython-310.pyc
│   │       │   └── utils.cpython-310.pyc
│   │       ├── run_fullsearch.py
│   │       ├── run_searchopen.py
│   │       ├── run_search.py
│   │       └── utils.py
│   └── managment
│       ├── manage_logs
│       │   ├── logs_clrlogs.sh
│       │   └── logs_viewlogs.sh
│       ├── manage_memory
│       │   ├── memory_memclr.sh
│       │   ├── memory_memlst.sh
│       │   └── memory_memshow.sh
│       ├── manage_search
│       │   ├── search_searchclr.sh
│       │   └── search_searchshow.sh
│       └── manage_templates
│           ├── template_tl.sh
│           └── template_t.sh
├── templates
│   ├── ask_template.txt
│   ├── chat_template.txt
│   ├── coder_agent.txt
│   ├── debugger_agent.txt
│   ├── filerunner_agent.txt
│   ├── planner_agent.txt
│   └── search_template.txt
└── tests
"""


prompt = replace_input_sentence(template=prompt,user_input="I want to focus to show my skills in making scripts")
prompt += query


r = llm.predict(text=prompt)
print(r)

