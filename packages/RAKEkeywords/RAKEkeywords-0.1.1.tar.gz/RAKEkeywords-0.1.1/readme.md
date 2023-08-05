# RAKEkeywords

Implementation of RAKE - Rapid Automatic Keyword Exraction algorithm as described in:
 
     Rose, S., D. Engel, N. Cramer, and W. Cowley (2010).
     Automatic keyword extraction from indi-vidual documents.
     In M. W. Berry and J. Kogan (Eds.), Text Mining: Applications and Theory.unknown: John Wiley and Sons, Ltd.

  
## Install

Available on pip

```bash
pip install RAKEkeywords
```

## Usage

```python
from RAKEkeywords import Rake

rake = Rake()

keywords = rake.extract_keywords("Mycroft is a free and open-source voice assistant for Linux-based operating systems that uses a natural language user interface")

"""
[('natural language user interface', 16.0),
 ('open-source voice assistant', 9.0),
 ('linux-based operating systems', 9.0),
 ('mycroft', 1.0),
 ('free', 1.0)]
"""

```
