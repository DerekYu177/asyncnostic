# asyncnostic
Using pytest to run unit-tests that now need to run async?
This package serves as a catch-all for mixing regular and asynchronous tests.

```py
import unittest
import asyncio
from asyncnostic import asyncnostic

@asyncnostic
class TestAThing(unittest.TestCase):

  # the kwarg "loop" as an method argument is optional
  # If you don't want it, leave it out.
  # The event loop will be the same for all tests
  # we keep the same setUp and tearDown naming conventions from unittest
  async def setUp(self, loop):
    # await statements can go here too!
    self.device = Device()
    await self.device.start(loop)

  # as long as your tests start with convention - starting in "test"
  # asyncnostic will pick them up
  async def test_async_simple(self, loop):
    result = await self.device.property
    assert result

  # we even handle regular tests thrown into the mix
  # you can even ask for the loop if you want
  def test_regular_simple(self, loop):
    assert self.device.loop == loop

```

### How it works under the hood
We find all coroutines that start with "test", as is convention. These tests are then transformed into regular methods, and the asynchronous test is overwritten by the regular test method with the same name. Tests that are not asynchronous are left unchanged. If any of the tests request a loop, the event loop (unique per class) will be passed as a keyword argument.
