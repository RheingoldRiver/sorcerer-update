import json
import string

from mwcleric import AuthCredentials
from mwcleric import WikiggClient

WIKITEXT = """{{{{Item infobox
|Weight={weight}
|Element={element}
{recipe}}}}}
{builds_into}
"""


class Creator:
    summary = 'Creating new pages from data file'

    def __init__(self):
        credentials = AuthCredentials(user_file="me")
        self.site = WikiggClient('sorcererbyriver', credentials=credentials)
        with open('items.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def run(self):
        for k, v in self.data.items():
            # split out into multiple lines for clarity
            page_name = string.capwords(k)
            page = self.site.client.pages[page_name]
            page_text = WIKITEXT.format(
                weight=v['weight'],
                element=v['element'],
                recipe=self.get_recipe_text(v),
                builds_into=self.get_builds_into_text(k)
            )

            # this is the general form for saving a page
            # the page is a Page object gotten from site.client.pages[page_name]
            # page_text is the text you want to save
            # summary is the edit summary to use
            page.save(page_text, summary=self.summary)

    @staticmethod
    def get_recipe_text(info):
        if len(info['ingredients']) == 0:
            # We could also choose to always return something here, and simply sometimes
            # have an empty |Recipe= parameter in the item infobox.
            # That would simplify the code a bit and not really cause any problems,
            # I just wanted to show a slightly more complex operation that you can simplify
            # rather than the other way around
            return ''
        # when doing string.format, {{ will be condensed down to {
        # so there are often a lot of { and } when you put wikitext here
        recipe_string = '{{{{RecipePart|item={ing}|quantity={q}}}}}'
        ingredients = ''.join(
            [recipe_string.format(ing=string.capwords(x['ingredient']), q=x['quantity']) for x in info['ingredients']])
        return f'|Recipe={ingredients}\n'

    def get_builds_into_text(self, item):
        for _, other in self.data.items():
            for ing in other['ingredients']:
                if ing['ingredient'] == item:
                    # as this string won't be in any string.format call, there is
                    # no need to escape the open & closing braces here
                    return '== Builds into ==\n{{BuildsInto}}'
        return ''


if __name__ == '__main__':
    Creator().run()
