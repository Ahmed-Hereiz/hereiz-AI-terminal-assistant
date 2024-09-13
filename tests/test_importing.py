import unittest
from utils import add_root_to_path
add_root_to_path()

class TestcustomAgentsImport(unittest.TestCase):

    def test_import_agent_llm(self):
        try:
            from customAgents.agent_llm import __all__ as llm_all
            print(f"\nagent_llm __all__: {llm_all}")
        except ImportError as e:
            self.fail(f"Import failed for agent_llm: {e}")

    def test_import_agent_prompt(self):
        try:
            from customAgents.agent_prompt import __all__ as prompt_all
            print(f"\nagent_prompt __all__: {prompt_all}")
        except ImportError as e:
            self.fail(f"Import failed for agent_prompt: {e}")

    def test_import_agent_routers(self):
        try:
            from customAgents.agent_routers import __all__ as routers_all
            print(f"\nagent_routers __all__: {routers_all}")
        except ImportError as e:
            self.fail(f"Import failed for agent_routers: {e}")

    def test_import_agent_runtime(self):
        try:
            from customAgents.agent_runtime import __all__ as runtime_all
            print(f"\nagent_runtime __all__: {runtime_all}")
        except ImportError as e:
            self.fail(f"Import failed for agent_runtime: {e}")

    def test_import_agent_env(self):
        try:
            from customAgents.agent_env import __all__ as env_all
            print(f"\nagent_env __all__: {env_all}")
        except ImportError as e:
            self.fail(f"Import failed for agent_env: {e}")

    def test_import_agent_tools(self):
        try:
            from customAgents.agent_tools import __all__ as tools_all
            print(f"\nagent_tools __all__: {tools_all}")
        except ImportError as e:
            self.fail(f"Import failed for agent_tools: {e}")

    def test_import_agent_models(self):
        try:
            from customAgents.agent_models import __all__ as models_all
            print(f"\nagent_models __all__: {models_all}")
        except ImportError as e:
            self.fail(f"Import failed for agent_models: {e}")

if __name__ == '__main__':
    unittest.main()
