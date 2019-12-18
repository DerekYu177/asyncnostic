import unittest
import asyncio

import asyncnostic

class WithoutAsyncUnchanged:
    def setUp(self):
        self.a = "apples"

    def tearDown(self):
        self.a = "bananas"

    def test_basic(self):
        assert 1 + 1 == 2

    def test_with_self(self):
        assert self.a == "apples"


class WithAsyncTests:
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


class WithMixAsyncTests:
    def setUp(self, loop):
        self.loop = loop

    async def test_async_loop(self, loop):
        await asyncio.sleep(0, loop=loop)
        assert loop == self.loop

    async def test_loop(self, loop):
        assert loop == self.loop


class WithAsyncSpecials:
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

base_test_klasses = [
    WithoutAsyncUnchanged,
    WithAsyncTests,
    WithMixAsyncTests,
    WithAsyncSpecials,
]

decorated_test_klasses = []

for klass in base_test_klasses:
    # from the one class dynamically create 2 similar test classes
    # and decorate them with asyncnostic.asyncnostic and asyncnostic.v1
    # make sure the names change based on the name of the existing class

    klass_name = klass.__name__
    
    # klass_tested_with_legacy_decorator = type(
    #     f"Test{klass_name}Legacy",
    #     (unittest.TestCase, ),
    #     dict(klass.__dict__),
    # )
    #
    # klass_tested_with_legacy_decorator = \
    #     asyncnostic.asyncnostic(klass_tested_with_legacy_decorator)
    #
    # klass_tested_with_new_v1_decorator = type(
    #     f"Test{klass_name}V1",
    #     (unittest.TestCase, ),
    #     dict(klass.__dict__),
    # )
    #
    # klass_tested_with_new_v1_decorator = \
    #     asyncnostic.v1(klass_tested_with_new_v1_decorator)
    #
    # locals().update({
    #     klass_tested_with_legacy_decorator.__name__: klass_tested_with_legacy_decorator,
    #     klass_tested_with_new_v1_decorator.__name__: klass_tested_with_new_v1_decorator,
    # })

    locals().update({
        f"Test{klass_name}Legacy": asyncnostic.asyncnostic(
            type(
                f"Test{klass_name}Legacy",
                (unittest.TestCase, ),
                dict(klass.__dict__),
            )
        ),
        f"Test{klass_name}V1": asyncnostic.v1(
            type(
                f"Test{klass_name}V1",
                (unittest.TestCase, ),
                dict(klass.__dict__),
            )
        ),
    })
