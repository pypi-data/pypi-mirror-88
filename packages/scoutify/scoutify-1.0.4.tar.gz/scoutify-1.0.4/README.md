# Scoutify

![PyPI](https://img.shields.io/pypi/v/scoutify)
![PyPI - Downloads](https://img.shields.io/pypi/dm/scoutify)
![GitHub](https://img.shields.io/github/license/samsan-tech/scoutify)



## Installation

```bash
pip install scoutify
```

or upgrade

```bash
pip install scoutify --upgrade
```

## Quick Start

To get started, first create an app on https://developers.spotify.com/ to get you ID and SECRET.

### Usage example

```python
from scoutify import Scoutify
sp = Scoutify(client_id="YOUR_CLIENT_ID",
              client_secret="YOUR_CLIENT_SECRET",
              redirect_url="YOUR_REDIRECT_URI")
sp.set_access_token("YOUR_ACCESS_TOKEN")
result = sp.search(search_type="artist", q="blackpink")
print(result)
```


If you have suggestions, bugs or other issues specific to this library,
file them [here](https://github.com/samsan-tech/scoutify/issues).
Or just send a pull request.
