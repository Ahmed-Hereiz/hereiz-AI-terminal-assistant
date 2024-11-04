from customAgents.agent_llm.base_multimodal import BaseMultiModal
from PIL import Image
from utils import add_root_to_path
root_path = add_root_to_path()

from common.utils import load_config
config = load_config(f"{root_path}/config/llm.json")


def test_multimodal_generate():
    img = Image.new('RGB', (100, 100), color='red')

    prompt = "What can you see in this image?, then tell me a beautiful poem about it in about 20 lines"

    base_multimodal = BaseMultiModal(api_key=config['api_key'], model=config['model'])

    response = base_multimodal.multimodal_generate(prompt, img, stream=True) 
    
    return response


if __name__ == "__main__":
    print(test_multimodal_generate())


