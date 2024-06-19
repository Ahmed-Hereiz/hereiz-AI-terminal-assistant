from utils import add_root_to_path
hereiz_root = add_root_to_path()

from fonts import CustomizeOutputTerminal
from helpers import (
    replace_instructions_sentence,
    replace_input_sentence,
    extract_fetched_data,
    concat_fetched_content,
    concat_links_and_titles
)


class RedirectSearchRuntime:
    def __init__(self, agent, search_manager, summarizer, prompt, parser, history_file_path):
        self.agent = agent
        self.prompt = prompt
        self.parser = parser
        self.search_manager = search_manager
        self.summarizer = summarizer
        self.history_file_path = history_file_path
        

    def _prepare_prompt(self, query):
        prompt = replace_instructions_sentence(self.prompt, self.parser.get_format_instructions())
        prompt = replace_input_sentence(prompt, query)
        return prompt
    

    def step(self, query):

        prompt = self._prepare_prompt(query=query)
        redirected_response = self.agent.generate_response(input=prompt)
        search_query, search_description = redirected_response['search'], redirected_response['description']
        print(CustomizeOutputTerminal(hereiz_root).customize_output(f"redirecting your query from \"{query}\" to \"{search_query}\" for better search results",color="green"))
        fetched_data = self.search_manager.integrated_search(query=search_query)
        links, titles, contents = extract_fetched_data(fetched_data)
        full_content = concat_fetched_content(contents)
        full_links, full_titles = concat_links_and_titles(links, titles)
        print(CustomizeOutputTerminal(hereiz_root).customize_output(f"Using this description to show the output : \"{search_description}\"\n",color="green"))
        print(CustomizeOutputTerminal(hereiz_root).customize_output(f"summary of the search results :\n",color="cyan"))
        summarized_text = self.summarizer.make_search_summary(input=full_content,description=search_description)
        self.summarizer.store_search_history(self.history_file_path,query,summarized_text,full_titles,full_links)
        print(CustomizeOutputTerminal(hereiz_root).customize_output("\n\nThis search summary is based on this links : ",color="white"))
        print(CustomizeOutputTerminal(hereiz_root).customize_output(f"{full_links}",color="blue"))
        


    def agent_loop(self, query, steps=1):

        print(CustomizeOutputTerminal(hereiz_root).customize_output("Hereiz : \n"))
        print(CustomizeOutputTerminal(hereiz_root).customize_output("Starting the Searching process with the redirectional agents...\n",color="green"))

        for step in range(steps):
            print(CustomizeOutputTerminal(hereiz_root).customize_output(f"Entering step {step+1} in the agent loop",color="green"))
            self.step(query=query)

        CustomizeOutputTerminal(hereiz_root).reset_all()
        

class RedirectedLinksRuntime:
    def __init__(self, agent, search_manager, prompt, parser):
        self.agent = agent
        self.prompt = prompt
        self.parser = parser
        self.search_manager = search_manager
    

    def _prepare_prompt(self, query):
        prompt = replace_instructions_sentence(self.prompt, self.parser.get_format_instructions())
        prompt = replace_input_sentence(prompt, query)
        return prompt
    

    def step(self, query):
        
        prompt = self._prepare_prompt(query=query)
        redirected_response = self.agent.generate_response(input=prompt)
        search_query, _ = redirected_response['search'], redirected_response['description']
        print(CustomizeOutputTerminal(hereiz_root).customize_output(f"redirecting your query from \"{query}\" to \"{search_query}\" for better search results\n",color="green"))
        response = self.search_manager.make_search(query=query)

        print(CustomizeOutputTerminal(hereiz_root).customize_output(f"Finished searching here is some relevant links for you query :) \n", color="cyan"))

        for index, dictionary in enumerate(response):
            print(CustomizeOutputTerminal(hereiz_root).customize_output(dictionary['title'],color="white") +
                   " : " + CustomizeOutputTerminal(hereiz_root).customize_output(dictionary['link'],color="blue"))
            
            if index == 0:
                browse_link = dictionary['link']

        return browse_link
    

    def agent_loop(self, query, steps=1):

        print(CustomizeOutputTerminal(hereiz_root).customize_output("Hereiz : \n"))
        print(CustomizeOutputTerminal(hereiz_root).customize_output("Starting the Searching process with the redirectional agents...\n",color="green"))

        for step in range(steps):
            print(CustomizeOutputTerminal(hereiz_root).customize_output(f"Entering step {step+1} in the agent loop",color="green"))
            browse_link = self.step(query=query)

        CustomizeOutputTerminal(hereiz_root).reset_all()

        return browse_link
    

class RedirectFullSearchRuntime:
    def __init__(self, agent, search_manager, summarizer, prompt, parser, history_file_path):
        self.agent = agent
        self.prompt = prompt
        self.parser = parser
        self.search_manager = search_manager
        self.summarizer = summarizer
        self.history_file_path = history_file_path
        

    def _prepare_prompt(self, query):
        prompt = replace_instructions_sentence(self.prompt, self.parser.get_format_instructions())
        prompt = replace_input_sentence(prompt, query)
        return prompt
    

    def step(self, query):

        prompt = self._prepare_prompt(query=query)
        redirected_response = self.agent.generate_response(input=prompt)
        search_query, search_description = redirected_response['search'], redirected_response['description']
        print(CustomizeOutputTerminal(hereiz_root).customize_output(f"redirecting your query from \"{query}\" to \"{search_query}\" for better search results",color="green"))
        response = self.search_manager.make_search(query=query)

        print(CustomizeOutputTerminal(hereiz_root).customize_output(f"Finished searching here is some relevant links for you query :) \n", color="cyan"))
        
        for index, dictionary in enumerate(response):
            print(CustomizeOutputTerminal(hereiz_root).customize_output(dictionary['title'],color="white") +
                   " : " + CustomizeOutputTerminal(hereiz_root).customize_output(dictionary['link'],color="blue"))
            
            if index == 0:
                browse_link = dictionary['link']
    
        print(CustomizeOutputTerminal(hereiz_root).customize_output(f"\nresearching for making summary out of new content \n", color="green"))
        fetched_data = self.search_manager.integrated_search(query=search_query)
        links, titles, contents = extract_fetched_data(fetched_data)
        full_content = concat_fetched_content(contents)
        full_links, full_titles = concat_links_and_titles(links, titles)
        print(CustomizeOutputTerminal(hereiz_root).customize_output(f"Using this description to show the output : \"{search_description}\"\n",color="green"))
        print(CustomizeOutputTerminal(hereiz_root).customize_output(f"summary of the search results :\n",color="cyan"))
        summarized_text = self.summarizer.make_search_summary(input=full_content,description=search_description)
        self.summarizer.store_search_history(self.history_file_path,query,summarized_text,full_titles,full_links)
        print(CustomizeOutputTerminal(hereiz_root).customize_output("\n\nThis search summary is based on this links : ",color="white"))
        print(CustomizeOutputTerminal(hereiz_root).customize_output(f"{full_links}",color="blue"))

        return browse_link


    def agent_loop(self, query, steps=1):

        print(CustomizeOutputTerminal(hereiz_root).customize_output("Hereiz : \n"))
        print(CustomizeOutputTerminal(hereiz_root).customize_output("Starting the Searching process with the redirectional agents...\n",color="green"))

        for step in range(steps):
            print(CustomizeOutputTerminal(hereiz_root).customize_output(f"Entering step {step+1} in the agent loop",color="green"))
            browse_link = self.step(query=query)

        CustomizeOutputTerminal(hereiz_root).reset_all()

        return browse_link