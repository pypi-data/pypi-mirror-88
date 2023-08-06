# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mighty', 'mighty.game']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.1.2,<7.0.0']

setup_kwargs = {
    'name': 'mighty',
    'version': '1.0.1',
    'description': 'Mighty card game engine',
    'long_description': "# Mighty Engine\n\n## Example\n\n```python\ngame = PledgePhase(start_player=0, min_count=13)\nwhile not game.pledge_done():\n    print('Boss: {}\\tShape: {}\\tCount: {}'.format(*game.current_pledge()))\n    print('queue: {}'.format(game.pledge_queue))\n    player = game.turn_player()\n    print('Player {}: {}'.format(player, game.hand(player=player)))\n\n    pledge_until_valid(game)\n\nif game.boss is not None:\n    game = ExtraPhase(*game.pledge_result())\n    game.prepare_extra_hand()\n    boss = game.boss\n    hand = game.hand(player=boss)\n    print('Boss extra hand: {}'.format(hand))\n    discard = list(map(int, input('Discard: ').split()))\n    game.discard_extra(discard=discard)\n    friend_condition = input('Pick friend: ')\n    game.pick_friend(friend_condition)\n\n    game = PlayPhase(*game.extra_result())\n    for r in range(10):\n        print('Round {}'.format(r))\n        for _ in range(game.NUM_PLAYERS):\n            print(game.round_state())\n            player = game.turn_player()\n            hand = game.hand(player=player)\n            print(hand)\n            while True:\n                card = int(input('Card: '))\n                valid, actions = game.check_submit(card=card)\n                if not valid:\n                    continue\n                elif actions:\n                    print(actions)\n                    action = actions[int(input())]\n                    game.submit(card=card, action=action)\n                else:\n                    game.submit(card=card, action=None)\n                break\n            print(game.submitted_cards())\n        print(game.round_summary())\n    print(game.final_summary())\n```\n",
    'author': 'DongJin Shin',
    'author_email': 'dongjin.shin.00@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dj-shin/mighty-engine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
