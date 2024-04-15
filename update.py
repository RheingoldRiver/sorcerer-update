import json
import string

from mwcleric import AuthCredentials
from mwcleric import TemplateModifierBase
from mwcleric import WikiggClient
from mwparserfromhell.nodes import Template

credentials = AuthCredentials(user_file="me")
site = WikiggClient('sorcererbyriver', credentials=credentials)
summary = 'Automatically updating infobox from changed data'

with open('items.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


class TemplateModifier(TemplateModifierBase):
    def update_template(self, template: Template):
        if self.current_page.namespace != 0:
            return
        info = data[self.current_page.name.lower()]
        template.add('Weight', info['weight'])
        template.add('Element', info['element'])
        if (recipe := self.get_recipe_text(info)) is None:
            return
        template.add('Recipe', recipe)

    @staticmethod
    def get_recipe_text(info):
        if len(info['ingredients']) == 0:
            return None
        recipe_string = '{{{{RecipePart|item={ing}|quantity={q}}}}}'
        return ''.join(
            [recipe_string.format(ing=string.capwords(x['ingredient']), q=x['quantity']) for x in info['ingredients']])


TemplateModifier(site, 'Item infobox',
                 summary=summary).run()
