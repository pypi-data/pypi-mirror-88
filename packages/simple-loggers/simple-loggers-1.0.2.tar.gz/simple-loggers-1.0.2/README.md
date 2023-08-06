# A Simple Logger Package

## Installation
```bash
pip install simple-loggers
```

## Usage
```python

from simple_loggers import SimpleLogger

logger = SimpleLogger(colored=True)
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')

logger2 = SimpleLogger(name='TEST2', colored=False, logfile='out.log')
logger2.debug('debug message')
logger2.info('info message')
logger2.warning('warn message')
logger2.error('error message')

logger3 = SimpleLogger(name='TEST3', level='info', fmt='%(asctime)s %(levelname)s: %(message)s')
logger3.debug('debug message')
logger3.info('info message')
logger3.warning('warn message')
logger3.error('error message')
```