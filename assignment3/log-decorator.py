import logging

# one time setup
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    def wrapper(*args, **kwargs):
        logger.info(f"function: {func.__name__}")
        if args:
            logger.info(f"positional parameters: {list(args)}")
        else:
            logger.info("positional parameters: none")
        if kwargs:
            logger.info(f"keyword parameters: {kwargs}")
        else:
            logger.info("keyword parameters: none")
        result = func(*args, **kwargs)
        logger.info(f"return: {result}")
        return result
    return wrapper

@logger_decorator
def func1():
    print("Hello, World!")

@logger_decorator
def func2(*args):
    return True

@logger_decorator
def func3(**kwargs):
    return logger_decorator

if __name__ == "__main__":
    func1()
    func2(1, 2, 3)
    func3(a=1, b=2)
