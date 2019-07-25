import unittest
import asyncio

from asyncnostic import asyncnostic


@asyncnostic
class TestWithoutAsyncUnchanged(unittest.TestCase):
    def setUp(self):
        self.a = "apples"

    def tearDown(self):
        self.a = "bananas"

    def test_basic(self):
        assert 1 + 1 == 2

    def test_with_self(self):
        assert self.a == "apples"


@asyncnostic
class TestWithAsyncTests(unittest.TestCase):
    def setUp(self):
        self.a = "pears"

    async def test_basic_without_loop(self):
        await asyncio.sleep(0)
        assert 1 + 1 == 2

    async def test_basic_with_loop(self, loop):
        await asyncio.sleep(0, loop=loop)
        assert 2 + 2 == 4

    async def test_with_self(self):
        await asyncio.sleep(0)
        assert self.a == "pears"

    async def test_with_self_with_loop(self, loop):
        await asyncio.sleep(0, loop=loop)
        assert self.a == "pears"


@asyncnostic
class TestWithMixAsyncTests(unittest.TestCase):
    def setUp(self, loop):
        self.loop = loop

    async def test_async_loop(self, loop):
        await asyncio.sleep(0, loop=loop)
        assert loop == self.loop

    async def test_loop(self, loop):
        assert loop == self.loop


@asyncnostic
class TestWithAsyncSpecials(unittest.TestCase):
    class DependsOnLoop:
        def __init__(self):
            self.depends = True

        async def start(self, loop):
            await asyncio.sleep(0, loop=loop)
            self.loop = loop

        async def add(self, a, b):
            await asyncio.sleep(0, loop=self.loop)
            return a + b

        def sub(self, a, b):
            return a - b

    async def setUp(self, loop):
        self.loop = loop
        self.depends = self.DependsOnLoop()
        await self.depends.start(loop)

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
