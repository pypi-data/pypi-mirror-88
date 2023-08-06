# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_section_index']

package_data = \
{'': ['*']}

install_requires = \
['mkdocs>=1.0,<2.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'mkdocs.plugins': ['section-index = '
                    'mkdocs_section_index.plugin:SectionIndexPlugin']}

setup_kwargs = {
    'name': 'mkdocs-section-index',
    'version': '0.2.2',
    'description': 'MkDocs plugin to allow clickable sections that lead to an index page',
    'long_description': '# mkdocs-section-index\n\n[Plugin][] for [MkDocs][] to allow clickable sections that lead to an index page.\n\n[![PyPI](https://img.shields.io/pypi/v/mkdocs-section-index)](https://pypi.org/project/mkdocs-section-index/)\n[![GitHub](https://img.shields.io/github/license/oprypin/mkdocs-section-index)](LICENSE.md)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/oprypin/mkdocs-section-index/CI)](https://github.com/oprypin/mkdocs-section-index/actions?query=event%3Apush+branch%3Amaster)\n\n```shell\npip install mkdocs-section-index\n```\n\n[mkdocs]: https://www.mkdocs.org/\n[plugin]: https://www.mkdocs.org/user-guide/plugins/\n\n## [Example](example/)\n\n![Screencast with comparison](https://user-images.githubusercontent.com/371383/99844559-8c4caa00-2b73-11eb-9e97-fad82447746c.gif)\n\nWith this `nav` in *mkdocs.yml* (or without `nav` but with [an equivalent directory structure](example/docs/)):\n\n```yaml\nnav:\n  - Frob: index.md\n  - Baz: baz.md\n  - Borgs:\n    - borgs/index.md\n    - Bar: borgs/bar.md\n    - Foo: borgs/foo.md\n\nplugins:\n  - section-index\n```\n\nThe *borgs/index.md* page is merged as the index of the "Borgs" section. Normally sections in [MkDocs][] cannot be clickable as pages themselves, but this plugin makes that possible.\n\n**See also: [a realistic demo site](https://oprypin.github.io/crystal-book/syntax_and_semantics/literals/).**\n\n## Theme support\n\nThis plugin requires per-theme overrides (implemented within the plugin), or [support from themes themselves](#implementation-within-themes).\n\nCurrently supported [themes][] are:\n\n* [material](https://github.com/squidfunk/mkdocs-material)\n* [readthedocs](https://www.mkdocs.org/user-guide/styling-your-docs/#readthedocs)\n\n[themes]: https://github.com/mkdocs/mkdocs/wiki/MkDocs-Themes\n\n## Usage notes\n\nThe kind of *nav* as shown above also happens to be what MkDocs produces when `nav` is omitted; it detects [`index.md` and `README.md`][nav-gen] pages and automatically puts them as the first item.\n\nTo make writing this kind of `nav` more natural ([in YAML there\'s no better option](https://github.com/mkdocs/mkdocs/pull/1042#issuecomment-290787554)), consider using the **[literate-nav][] plugin** along with this; then the above *nav* might be written like this:\n\n```markdown\n* [Frob](index.md)\n* [Baz](baz.md)\n* [Borgs](borgs/index.md)\n    * [Bar](borgs/bar.md)\n    * [Foo](borgs/foo.md)\n```\n\n[literate-nav]: https://github.com/oprypin/mkdocs-literate-nav\n\n## [Implementation](mkdocs_section_index/plugin.py)\n\n### "Protocol"\n\nNormally in MkDocs [`nav`][nav], the items can be one of:\n\n* a [`Section`][Section], which has a `title` and `children`.\n    * (`url` is always `None`)\n* a [`Page`][Page], which has a `title` and `url`.\n    * (`title` can be omitted, and later deduced from the page content)\n    * ([`children`][children] is always `None`)\n* a [`Link`][Link] (inconsequential for our purposes).\n\nThis plugin introduces a [hybrid kind of `Page`](mkdocs_section_index/__init__.py), which has all of these properties:\n\n* `title`: `str`\n* `url`: `str`\n* `children`: `list`\n* `is_page` = `True`\n* `is_section` = `True`\n\nSuch a special item gets put into a nav in the place of a `Section` which has a `Page` with an intentionally omitted title as its first child. Those two are naturally combined into a special [section-page](mkdocs_section_index/__init__.py) that\'s a hybrid of the two.\n\n[nav]: https://www.mkdocs.org/user-guide/custom-themes/#nav\n[Section]: https://www.mkdocs.org/user-guide/custom-themes/#section\n[Page]: https://www.mkdocs.org/user-guide/custom-themes/#page\n[children]: https://github.com/mkdocs/mkdocs/blob/2f833a1a29095733e53a04d062d315629d974ebe/mkdocs/structure/pages.py#L26\n[Link]: https://www.mkdocs.org/user-guide/custom-themes/#link\n\n### Implementation within themes\n\nThen all that a theme\'s template needs to do is to meaningfully support such nav items -- ones that have both a `url` and `children`. The item should be directly clickable to go to the corresponding page, and also be able to house sub-items.\n\nOf course, currently templates don\'t expect such a case; or if they did, it would be purely by chance. So currently this plugin "hacks into" templates of supported themes, [patching their source on the fly](mkdocs_section_index/rewrites.py) to fit its needs. The hope is that, once this plugin gains enough traction, theme authors will be happy to directly support this scenario (which is totally non-intrusive and backwards-compatible), and then the patches could be dropped.\n\n### "Alternatives considered"\n\nEven if all the template patches are gone, this plugin will still remain as the implementation of this special nav "protocol", and as the **opt-in mechanism**. In the author\'s view, such an approach is advantageous, because:\n\n* This is too controversial to be enabled by default, or even be part of MkDocs at all. This has been [discussed in the past and dropped](https://github.com/mkdocs/mkdocs/pull/1042#issuecomment-260813540). The main reason is that in MkDocs there\'s no requirement for a *nav*\'s structure to follow the actual directory structure of the doc files. Consequently, there\'s no natural way to deduce that a document should become the index page of a section just from its location, even if it\'s named *index.md*. Although if the *nav* is [omitted & generated][nav-gen], then yes, such an assumption works. It also works in the vast majority of actual usages *with* a *nav*, but that doesn\'t help.\n\n* Themes themselves also probably shouldn\'t directly try to detect logic such as "first child of a section if it has no title" and manually collapse the child *within Jinja template code*, as that\'s too messy. This also shouldn\'t be enabled by default. And even though templates could also make this opt-in, a centralized approach like this one ensures that accessing this feature is done uniformly. Not to mention that templates might never implement this themselves.\n\n[nav-gen]: https://www.mkdocs.org/user-guide/writing-your-docs/#configure-pages-and-navigation\n',
    'author': 'Oleh Prypin',
    'author_email': 'oleh@pryp.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oprypin/mkdocs-section-index',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
