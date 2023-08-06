# Trello API - Async Python SDK client (using aiohttp)

<p align="center">
<img src="https://img.shields.io/badge/tests-pytest-orange?style=for-the-badge" alt="pytest"/>
<img src="https://img.shields.io/badge/async-asyncio, aiohttp-green?style=for-the-badge" alt="asyncio, aiohttp"/>
<a href="https://t.me/herr_horror"><img src="https://img.shields.io/badge/Telegram Chat-@herr_horror-2CA5E0.svg?logo=telegram&style=for-the-badge" alt="Chat on Telegram"/></a>
<img src="https://img.shields.io/badge/version-v.0.0.1-green?style=for-the-badge" alt="Last Release"/>
</p>


Simple and fast client to call rest-api endpoints `"https://trello.com/1/` using aiohttp package.  

View at:
https://pypi.org/project/python-trello-api/


## How to install
```bash
pip3 install python-trello-api
```


## Usage

Main example:
```python
import asyncio
from api_trello import TrelloClient


TOKEN = "12345:YOUR_TOKEN"
APP_HOSTNAME = "https://YOUR_HOSTNAME.ngrok.io"


trello = TrelloClient(token=TGBOT_TOKEN)


async def main_async():
    pass


if __name__ == "__main__":
    asyncio.run_until_complete(main_async())

```




### Docs
1. How to publish pypi package [Medium article in Russian](https://medium.com/nuances-of-programming/python-%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F-%D0%B2%D0%B0%D1%88%D0%B8%D1%85-%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2-%D0%B2-pypi-11dd3216581c)


## Dependencies
TODO


## Disclaimer
This project and its author is neither associated, nor affiliated with [Atlassian](https://atlassian.com/) or [Trello](https://trello.com/) in anyway.
See License section for more details.


## License

This project is released under the [GNU LESSER GENERAL PUBLIC LICENSE][link-license] License.

[link-author]: https://github.com/DmitriyKalekin
[link-repo]: https://github.com/DmitriyKalekin/python-trello-api
[link-pygramtic]: https://github.com/devtud/pygramtic
[link-issues]: https://github.com/DmitriyKalekin/python-trello-api/issues
[link-contributors]: https://github.com/DmitriyKalekin/python-trello-api/contributors
[link-docs]: https://telegram-bot-api.readme.io/docs
[link-license]: https://github.com/DmitriyKalekin/python-trello-api/blob/main/LICENSE
[link-trello-api]: https://developer.atlassian.com/cloud/trello/rest/api-group-actions/

