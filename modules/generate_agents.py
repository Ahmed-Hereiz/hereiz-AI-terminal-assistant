from gradio_client import Client
from customAgents.agent_llm import BaseLLM
from customAgents.agent_prompt import ReActPrompt
from customAgents.agent_runtime import ReActRuntime
from customAgents.agent_models import GradioClientModels
from customAgents.agent_tools import ToolKit, ModelInferenceTool

from helpers import save_imgs, show_images_side_by_side, sketch_window

class txt2imgModel(GradioClientModels):
    def __init__(self, saved_imgs_dir: str, gradio_client_id: str = "mukaist/DALLE-4k", api_name: str = None):
        
        self.saved_imgs_dir = saved_imgs_dir

        super().__init__(gradio_client_id, api_name)

    def inference(self, input_prompt):
        client_output = super().inference(input_prompt)
        try:
            img_dirs = [img_dir['image'] for img_dir in client_output[0]]
            img_dirs = save_imgs(img_dirs,self.saved_imgs_dir)
            show_images_side_by_side(saved_imgs_dir=self.saved_imgs_dir)
            return img_dirs
        except:
            return client_output


class sketch2imgModel(GradioClientModels):
    def __init__(self, saved_imgs_dir: str, gradio_client_id: str = "https://gparmar-img2img-turbo-sketch.hf.space/", api_name: str = None):
        
        self.saved_imgs_dir = saved_imgs_dir

        super().__init__(gradio_client_id, api_name)

    def inference(self, input_prompt):

        img_path = sketch_window()

        client = Client(self.gradio_client_id)
        client_output = client.predict(
            img_path,
            input_prompt,
            "ethereal fantasy concept art of  {prompt} . magnificent, celestial, ethereal, painterly, epic, majestic, magical, fantasy art, cover art, dreamy",
            "Fantasy art",
            "42",
            0.4,
            fn_index=9,
        )

        try:
            img_dirs_path = []
            img_dirs_path.append(client_output[0])
            img_dirs = save_imgs(img_dirs_path,self.saved_imgs_dir)
            show_images_side_by_side(saved_imgs_dir=self.saved_imgs_dir)
            return f"Generated image succesfully saved in {img_dirs} (Now end the loop and tell the user that the image is generated succesfully and tell him where he can find it)"
        except:
            return f"Generated image succesfully saved in {client_output[0]} (Now end the loop and tell the user that the image is generated succesfully and tell him where he can find it)"
        


class GenerativeAILLM(BaseLLM):
    def __init__(self, api_key: str, model: str, temperature: float, safety_settings=None):
        super().__init__(api_key, model, temperature, safety_settings)

    def llm_generate(self, input: str) -> str:
        return super().generate_response(input)
    

class GenerativeAIPrompt(ReActPrompt):
    def __init__(self, question: str):

        prompt_string = """
You have access to generative ai tools where user will ask you to do some generative AI task and you have to use the tool to generate content for him.
you have to choose the right tool from the tools for the task.
your name is Hereiz and you are an AI assistant, after you generate the content the tools will give you message if the content is generated or no and the dir where the content is saved if it needs to be saved.
you have to tell the user in friendly way that you saved for him the content in this dir and ask if he needs some thing else
NEVER FORGET : the action input to the tool is a plain string with no '' or list
"""

        super().__init__(question, example_workflow="", prompt_string=prompt_string)



class GenerativeAIAgent(ReActRuntime):
    def __init__(self, llm, prompt):

        txt2img_tool = ModelInferenceTool(description="tool used to use text to image model (take input as single text prompt without list or '' in between) Note once the tool finish generation you will get message of where the output is found you have to tell the user the where the output dir is and stop also if you didn't get any output from the tool confirming it genrated rerun the tool some times if still no output clarify that there is problem with the tool",tool_name="text_to_image_tool",model=txt2imgModel(saved_imgs_dir="imgs"))
        sketch2img_tool = ModelInferenceTool(description="This tool is designed to convert a user’s sketch and prompt into a refined image. When the user expresses the intent to create a sketch, the tool will take a single input: a clear and detailed text prompt describing the desired modifications or enhancements to the sketch. The prompt should be provided as plain text (not using quotes or an input list). Once the image generation is complete, the tool will return the directory where the final image, refined from the user’s sketch, is saved.",tool_name="sketch_to_image_tool",model=sketch2imgModel(saved_imgs_dir="sketchimgs"))
        toolKit = ToolKit(tools=[txt2img_tool,sketch2img_tool])

        super().__init__(llm, prompt, toolKit)
