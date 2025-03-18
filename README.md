## About
Example wiki creation / updating scripts, using [mwcleric](https://github.com/RheingoldRiver/mwcleric)

SORCERER the game: https://sorcerer.river.me/

SORCERER wiki: https://sorcererbyriver.wiki.gg/wiki/Main_Page

## Files included

<code>create.py</code> is an example new-page-creation script.
<code>update.py</code> is an example wiki updating script.

Because there may be user content that you don't want to overwrite (e.g. trivia, strategy sections, etc) a different method is needed for updating.

For the sake of example, these two scripts are self-contained, but in reality you would probably want much of the logic to be handled in a shared formatter class.

## Test wiki
The scripts currently point to https://test.wiki.gg. This is a public test wiki that you can feel free to use for sandboxing!

## Please fork this repo

If you are going to base your own create/update scripts on this repo, please fork it instead of making a new repo! This way, the [list of forks](https://github.com/RheingoldRiver/sorcerer-update/forks) will be useful to people. You could also consider submitting a PR with a link to your repo in the README of [example_wiki_scripts](https://github.com/RheingoldRiver/example_wiki_scripts).

You could also star it ;)

## Python wiki class
[This wiki class](https://www.youtube.com/watch?v=YQZ1cZQJzUk) has an example of me writing some Python code for a the ONI wiki
