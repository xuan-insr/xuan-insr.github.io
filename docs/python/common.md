# 常用代码备忘

## loguru logger -> stderr

```Python
from loguru import logger
logger.remove()
logger.add(sys.stderr)
```
