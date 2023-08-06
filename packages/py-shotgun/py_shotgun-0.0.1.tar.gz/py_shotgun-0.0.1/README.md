# pyShotgun
A python wrapper for shotgun api

### usage
basic usage

```python
import logging
logger = logging.getLogger(__name__)
import shotgun_api3
from py_shotgun import SGSchema
sg = shotgun_api3.Shotgun(server, script_name=script_name, api_key=script_key)
# init a shotgun api

SGSchema.set_api(sg)
SGProject = SGSchema.sgClasses.Project
SGReply = SGSchema.sgClasses.Reply
# get shotgun class from "SGSchema.sgClasses"

project = SGProject(1, sg, logger)
reply = SGReply(2, sg, logger)

print(project.name)
```
