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
    def __init__(self):
        credentials = AuthCredentials(user_file="me")
        self.site = WikiggClient('sorcererbyriver', credentials=credentials)
        self.summary = 'Tabber -> Gallery'
        with open('items.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def run(self):
        for k, v in self.data.items():
            self.site.client.pages[string.capwords(k)].save(WIKITEXT.format(
                weight=v['weight'],
                element=v['element'],
                recipe=self.get_recipe_text(v),
                builds_into=self.get_builds_into_text(k)
            ))

    @staticmethod
    def get_recipe_text(info):
        if len(info['ingredients']) == 0:
            return ''
        recipe_string = '{{{{RecipePart|item={ing}|quantity={q}}}}}'
        ingredients = ''.join(
            [recipe_string.format(ing=string.capwords(x['ingredient']), q=x['quantity']) for x in info['ingredients']])
        return f'|Recipe={ingredients}\n'

    def get_builds_into_text(self, item):
        for _, other in self.data.items():
            for ing in other['ingredients']:
                if ing['ingredient'] == item:
                    return '== Builds into ==\n{{BuildsInto}}'
        return ''


if __name__ == '__main__':
    Creator().run()
