def extract_fetched_data(fetched_data):
    all_links = []
    all_titles = []
    all_content = []

    for single_fetch in fetched_data:
        all_links.append(single_fetch['link'])
        all_titles.append(single_fetch['title'])
        all_content.append(single_fetch['content'])

    return all_links, all_titles, all_content


def concat_fetched_content(all_fetched_content):
    full_content = ""

    for content in all_fetched_content:
        full_content += content
        full_content += "\n\n"

    return full_content


def concat_links_and_titles(all_links, all_titles):
    full_links = ""
    full_titles = ""

    for i in range(len(all_links)):
        full_links += all_links[i]
        full_links += "\n"

        full_titles += all_titles[i]
        full_titles += "\n"

    return full_links, full_titles