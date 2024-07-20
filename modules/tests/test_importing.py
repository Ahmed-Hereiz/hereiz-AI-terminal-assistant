import unittest
from utils import add_root_to_path
add_root_to_path()

class TestModulesImport(unittest.TestCase):

    def test_import_agent_llm(self):
        try:
            from modules.agent_llm import __all__ as llm_all
            print(f"\nagent_llm __all__: {llm_all}")
        except ImportError as e:
            self.fail(f"Import failed for agent_llm: {e}")

    def test_import_agent_prompt(self):
        try:
            from modules.agent_prompt import __all__ as prompt_all
            print(f"\nagent_prompt __all__: {prompt_all}")
        except ImportError as e:
            self.fail(f"Import failed for agent_prompt: {e}")

    def test_import_agent_routers(self):
        try:
            from modules.agent_routers import __all__ as routers_all
            print(f"\nagent_routers __all__: {routers_all}")
        except ImportError as e:
            self.fail(f"Import failed for agent_routers: {e}")

    def test_import_agent_runtime(self):
        try:
            from modules.agent_runtime import __all__ as runtime_all
            print(f"\nagent_runtime __all__: {runtime_all}")
        except ImportError as e:
            self.fail(f"Import failed for agent_runtime: {e}")

    def test_import_agent_env(self):
        try:
            from modules.agent_env import __all__ as env_all
            print(f"\nagent_env __all__: {env_all}")
        except ImportError as e:
            self.fail(f"Import failed for agent_env: {e}")

if __name__ == '__main__':
    unittest.main()
