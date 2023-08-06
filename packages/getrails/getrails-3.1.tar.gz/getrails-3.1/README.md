![Getrails](img/banner.png)

# GETRAILS

![Upload Python Package](https://github.com/Jul10l1r4/getrails/workflows/Upload%20Python%20Package/badge.svg) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/fc02078872134bbc93b9e79a777dc14e)](https://app.codacy.com/manual/Jul10l1r4/getrails?utm_source=github.com&utm_medium=referral&utm_content=Jul10l1r4/getrails&utm_campaign=Badge_Grade_Dashboard)

Lib of OSINT and Dork hacking that work with Google, Duckduckgo and Torch

## Run

```python
import getrails
getrails.search('site:scanme.nmap.org')) # Try Google search if return error use Duckduckgo
# ["http://scanme.nmap.org",...]

getrails.go_gle("term") # Searching Google
getrails.go_duck("term") # Searching Duckduckgo
getrails.go_onion("term") # Searching torch (Onion)
```

## Install

```pypi
pip3 install getrails
```
