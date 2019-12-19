# Usage

Using pytest to run unit-tests that now need to run async?
This package serves as a catch-all for mixing regular and asynchronous tests.

## asyncnostic 0.1.1 (v2)
This is a more modern implementation that takes into account the direction that python's `asyncio` package is moving - usage of the event loop specifically is slated for deprecation for python 3.8+. We set the loop specifically at the `asyncio` level so that any calls such as `asyncio.get_running_loop()` or `asyncio.get_event_loop()` or even `asyncio.run()` all use the same loop. This helps so that calls to the same `asyncio` object (such as pipes or queues) don't suffer when the loop that was used to generate the object is the same one that interacts with the object. 

```py
import unittest
import asyncio
import asyncnostic

@asyncnostic.v2
class TestAThing(unittest.TestCase):
  async def setUp(self):
    self.loop = asyncio.get_event_loop()
    
  async def test_loop(self):
    assert asyncio.get_event_loop() == self.loop
    await asyncio.sleep(2)
```

## asyncnostic 0.1.1 (v1)
You decorate the test class with `@asyncnostic.v1`. If any methods require the event loop, they can request it by adding the argument 'loop' in the method definition. We will automatically pass in the same loop every time. There will be no deprecation warning associated with using `asyncnostic` like this.

```py
import unittest
import asyncio
import asyncnostic

# if your test class has no async components to it at all
# asyncnostic will stay out of your way
@asyncnostic.v1
class TestAThing(unittest.TestCase):

  # the kwarg "loop" as an method argument is optional
  # If you don't want it, leave it out.
  # The event loop will be the same for all tests
  # we keep the same setUp and tearDown naming conventions from unittest
  async def setUp(self, loop):
    self.device = Device()
    self.loop = loop
    self.device.loop = loop
    await self.device.start(loop)

  # as long as your tests start with convention - starting in "test"
  # asyncnostic will pick them up
  # event loops passed in are the same
  async def test_async_simple(self, loop):
    assert await self.device.property
    asssert self.loop = loop

  # we even handle regular tests thrown into the mix
  # you can even ask for the loop if you want
  def test_regular_simple(self, loop):
    assert self.device.loop == loop

```

## asyncnostic (legacy)
This will raise an `DeprecationWarning` if called in this way. 
Decorate your class with `@asyncnostic`:

```py
import unittest
import asyncio
from asyncnostic import asyncnostic

@asyncnostic
class TestAThing(unittest.TestCase):

  async def setUp(self, loop):
    self.device = Device()
    await self.device.start(loop)
    
  async def test_async_simple(self, loop):
    result = await self.device.property
    assert result

  def test_regular_simple(self, loop):
    assert self.device.loop == loop

```

### How it works under the hood
We find all coroutines that start with "test", as is convention. These tests are then transformed into regular methods, and the asynchronous test is overwritten by the regular test method with the same name. Tests that are not asynchronous are left unchanged. If any of the tests request a loop, the event loop (unique per class) will be passed as a keyword argument.

### Contributing
Feel free to open a PR or and issue if there's any problem with `Asyncnostic`! If you do open a PR, make sure to have run `nox` before review :)
