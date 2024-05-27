from colorama import Fore, Style
import json


class CustomizeOutputTerminal:
    def __init__(self,base_dir):

        self.color_dict = {
            'black': Fore.BLACK,
            'red': Fore.RED,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'magenta': Fore.MAGENTA,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE
        }

        self.style_dict = {
            'normal': Style.NORMAL,
            'bold': Style.BRIGHT,
        }

        self.available_colors = list(self.color_dict.keys())
        self.available_styles = list(self.style_dict.keys())

        self.base_dir = base_dir
    
    def customize_output(self, text, color=None, style=None):

        terminal_config = self._load_config(self.base_dir)

        color_code = self.color_dict.get(terminal_config['color']) if color is None else self.color_dict.get(color.lower(), Fore.WHITE)
        style_code = self.style_dict.get(terminal_config['style']) if style is None else self.style_dict.get(style.lower(), Style.NORMAL)

        return f"{style_code}{color_code}{text}"
    
    def reset_all(self):
        print(f"\n{Style.RESET_ALL}")
    
    def _load_config(self, base_dir):

        terminal_config_dir = f"{base_dir}/config/terminal.json"
        
        with open(terminal_config_dir, 'r') as f:
            terminal_config = json.load(f)
        
        return terminal_config
    
    def __str__(self):
        color_list = ", ".join(self.available_colors)
        style_list = ", ".join(self.available_styles)
        return f"Available Colors: {color_list}\nAvailable Styles: {style_list}\n"


