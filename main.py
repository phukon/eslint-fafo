from child.child import childFunction
from logger import logger, log_context

print('running main')

with log_context('rikriki'):
    logger.info('Starting child function')
    childFunction()
    logger.info('Finished child function')

logger.flush()