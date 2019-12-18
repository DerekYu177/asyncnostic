import asyncio
import inspect

specials = ["setUp", "tearDown"]


def to_method_with_loop(corm, loop):
    def inner(self):
        req_args = inspect.getfullargspec(corm).args
        # for now we only support inserting the loop directly into the method
        # for python >3.10, using the loop explicitly is considered bad
        # practice, so we will have to set the loop some other way
        _corm = corm(self, loop=loop) if "loop" in req_args else corm(self)
        return (
            loop.run_until_complete(_corm)
            if inspect.iscoroutinefunction(corm)
            else _corm
        )

    return inner


def is_a_coro_test(name, coro):
    is_test = name.startswith("test")
    is_coro = inspect.iscoroutinefunction(coro)
    return is_coro and is_test


def asyncnostic(klass):
    loop = asyncio.new_event_loop()
    klass_methods_and_coroutines = klass.__dict__

    # copy over all test async methods
    # leave the ones that do not start with test
    # because they are supporting methods

    coroutines = {
        name: coro
        for name, coro in klass_methods_and_coroutines.items()
        if is_a_coro_test(name, coro)
    }

    for name, coro in coroutines.items():

        # transform the coroutine into a method
        # provide the loop if necessary
        # the name cannot change because we want to override the earlier method
        method = to_method_with_loop(coro, loop)
        setattr(klass, name, method)

    # copy over the setup and teardown
    special_methods = {
        name: method
        for name, method in klass_methods_and_coroutines.items()
        if name in specials
    }

    for name, method in special_methods.items():

        # does not transform, since these are already methods
        # provides loop if necessary
        method = to_method_with_loop(method, loop)
        setattr(klass, name, method)

    return klass
