from utils import get_arguments, add_root_to_path
from PIL import Image

root_dir = add_root_to_path()
from common import load_config
from modules.screen_agents import ScreenLMM, ScreenPrompt, ScreenAgent
from customAgents.agent_tools import BashRuntimeTool


def hande_screen():
    
    get_screen = BashRuntimeTool()
    cap_screen_file = f"{root_dir}/hereiz_screen.sh"
    output_screen_dir = f"{root_dir}/data/tmp/"

    get_screen.execute_func(code=f"bash {cap_screen_file} {output_screen_dir}")

    config = load_config(f'{root_dir}/config/llm.json')
    img = Image.open(f"{output_screen_dir}/screenshot.png")
    
    args = get_arguments()
    if not args.screen:
        print("Usage: hereiz --screen 'your question'")
        return 
    
    screen_lmm = ScreenLMM(api_key=config['api_key'],model=config['model'],temperature=0.7)
    screen_prompt = ScreenPrompt(user_question=args.screen,img=img)
    screen_agent = ScreenAgent(llm=screen_lmm,prompt=screen_prompt)

    agent_response = screen_agent.loop()


def continue_screen_chat():

    while True:
        new_query = input("\n\nEnter feedback (or 'exit' to end loop): ")

        if new_query.lower() == "exit":
            break
        else:
            get_screen = BashRuntimeTool()
            cap_screen_file = f"{root_dir}/hereiz_screen.sh"
            output_screen_dir = f"{root_dir}/data/tmp/"
            get_screen.execute_func(code=f"bash {cap_screen_file} {output_screen_dir}")

            config = load_config(f'{root_dir}/config/llm.json')
            img = Image.open(f"{output_screen_dir}/screenshot.png")
            
            screen_lmm = ScreenLMM(api_key=config['api_key'],model=config['model'],temperature=0.7)
            screen_prompt = ScreenPrompt(user_question=new_query,img=img)
            screen_agent = ScreenAgent(llm=screen_lmm,prompt=screen_prompt)

            agent_response = screen_agent.loop()