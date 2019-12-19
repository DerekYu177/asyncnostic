import unittest
import asyncio

import asyncnostic


@asyncnostic.v2
class TestWithoutAsyncUnchangedV2(unittest.TestCase):
    def setUp(self):
        self.a = "apples"

    def tearDown(self):
        self.a = "bananas"

    def test_basic(self):
        assert 1 + 1 == 2

    def test_with_self(self):
        assert self.a == "apples"


@asyncnostic.v2
class TestWithAsyncTestsV2(unittest.TestCase):
    async def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.a = "pears"

    async def test_basic(self):
        await asyncio.sleep(0)
        assert 2 + 2 == 4

    async def test_with_self(self):
        await asyncio.sleep(0)
        assert self.a == "pears"

    async def test_running_loop_is_same_as_setup(self):
        assert asyncio.get_running_loop() == self.loop


@asyncnostic.v2
class TestWithAsyncSpecialsV2(unittest.TestCase):
    class DependsOnLoop:
        def __init__(self):
            self.depends = True

        async def start(self):
            loop = asyncio.get_running_loop()
            await asyncio.sleep(0)
            self.loop = loop

        async def add(self, a, b):
            await asyncio.sleep(0, loop=self.loop)
            return a + b

        def sub(self, a, b):
            return a - b

    async def setUp(self):
        self.loop = asyncio.get_running_loop()
        self.depends = self.DependsOnLoop()
        await self.depends.start()

    async def test_depends(self):
        result = await self.depends.add(1, 1)
        assert result == 2

    async def test_rely_on_supporting_method(self):
        assert await self.supporting_method()

    async def test_rely_on_supporting_method_tricky(self):
        loop = await self.tricky_supporting_test_method()
        assert loop == self.loop

    async def supporting_method(self):
        return self.depends.depends

    async def tricky_supporting_test_method(self):
        return self.depends.loop

    def test_simple_depends(self):
        assert self.depends.sub(2, 1) == 1
