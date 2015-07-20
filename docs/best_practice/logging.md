The logging best practice is inspired by [chapter 11](http://12factor.net/logs) of [The Twelve-Factor App](http://12factor.net/). In short, the idea is that all packages and modules log to ```stdout``` so that during development, this stream is available to the developer and in testing and production environments, an application (or applications) can be in place to route ```stdout``` as appropriate.

In the case of this application, all packages and modules should have logging implemented by default (using the standard library). However, the specifics of this implementation will depend on the package and module in question. Where it is known, it will be detailed here.

In the case of the ```utils``` library, the ```Logger``` object should be the first definition made inside of the public function (noting that a ```utils``` module should only ever have one public function) and instantiated with the ```__name__``` variable. A "START" and "END" message should wrap the body of the function as follows:
```python
import logging


def foo():
    logger = logging.getLogger(__name__)
    logger.info('START {0}.'.format(__name__))

    ...

    logger.info('END {0}.'.format(__name__))
```
Logging may then be executed throughout the public function as necessary. Note that if logging is required in any of the private functions, the ```Logger``` object will have to be passed as a parameter. If usage in this way turns out to be extensive, I may change the best practice to define the Logger at a module level rather than inside the public function.

The specifics of how to deal with logging in "top-level" applications is yet to be defined but the general idea is to configure a logger with ```Handler``` such that all logging goes to ```stdout``` and then, using a logging application, route everything from ```stdout``` to a logfile (or multiple logfiles). This will become clearer in time though.
