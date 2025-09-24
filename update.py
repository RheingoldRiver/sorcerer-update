import json
import string

from mwcleric import AuthCredentials
from mwcleric import TemplateModifierBase
from mwcleric import WikiggClient
from mwparserfromhell.nodes import Template

credentials = AuthCredentials(user_file="me")
# the following login has been changed to edit test.wiki.gg rather than sorcererbyriver.wiki.gg
# test.wiki.gg is our sandbox wiki that anyone may edit for any reason to test scripts
# so while you are testing your code, you can leave this as-is and view changes at test.wiki.gg
# then change it to your wiki afterwards
site = WikiggClient('test', credentials=credentials)
summary = 'Automatically updating infobox from changed data'

with open('items.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


class TemplateModifier(TemplateModifierBase):
    def update_template(self, template: Template):
        # TemplateModifier is a generic framework for modifying templates
        # It will iterate through all pages containing at least one instance
        # of the specified template in the initialization call below and then
        # update every instance of the template in question with one batched edit per page
        if self.current_page.namespace != 0:
            # don't do anything outside of the main namespace
            # for example, we don't want to modify template documentation or user sandboxes
            return
        info = data[self.current_page.name.lower()]
        template.add('Weight', info['weight'])
        template.add('Element', info['element'])
        if (recipe := self.get_recipe_text(info)) is None:
            return
        template.add('Recipe', recipe)
        # any changes made before returning will automatically be saved by the runner

    @staticmethod
    def get_recipe_text(info):
        if len(info['ingredients']) == 0:
            return None
        recipe_string = '{{{{RecipePart|item={ing}|quantity={q}}}}}'
        return ''.join(
            [recipe_string.format(ing=string.capwords(x['ingredient']), q=x['quantity']) for x in info['ingredients']])


TemplateModifier(site, 'Item infobox',
                 summary=summary).run()
