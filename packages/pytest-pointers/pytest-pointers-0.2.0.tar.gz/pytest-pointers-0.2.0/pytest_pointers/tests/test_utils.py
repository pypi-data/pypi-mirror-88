import ast
from pathlib import Path
from textwrap import dedent

import pytest

from pytest_pointers.tests.mock_structure import for_func_finder
from pytest_pointers.utils import FuncFinder


@pytest.mark.pointer(target=FuncFinder.get_methods)
class TestFuncFinderGetFunctions:
    def test__func_called__result_returned(self, testdir):
        with open(Path(for_func_finder.__file__), 'r') as f:
            tree = ast.parse(f.read())

        methods = list(FuncFinder.get_methods(tree))

        assert len(methods) == 5
        assert methods[0].name == 'for_test'

        assert methods[1].name == '__init__'
        assert methods[1].parent.name == 'Some'
        assert methods[2].name == 'for_test'
        assert methods[2].parent.name == 'Some'

        assert methods[3].name == '__init__'
        assert methods[3].parent.name == 'Another'
        assert methods[4].name == 'for_test'
        assert methods[4].parent.name == 'Another'


@pytest.mark.pointer(target=FuncFinder.get_node_qual_name)
class TestFuncFinderGetNodeQualName:
    @pytest.mark.parametrize(
        ('module', 'expect'),
        [
            pytest.param(
                dedent("""\
                    def for_test():
                        pass
                    """),
                ['for_test'],
                id="Simple function"
            ),
            pytest.param(
                dedent("""\
                    class Some:
                        def __init__(self):
                            pass

                        def for_test(self):
                            pass
                    """),
                ['Some.__init__', 'Some.for_test'],
                id="Multiple methods"
            ),
            pytest.param(
                dedent("""\
                        class Some:
                            async def for_test(self):
                                pass
                        """),
                ['Some.for_test'],
                id="Async methods"
            ),
            pytest.param(
                dedent("""\
                    class Some:
                        def __init__(self):
                            pass

                        def for_test(self):
                            pass


                    class Another:
                        def __init__(self):
                            pass

                        def for_test(self):
                            pass
                    """),
                ['Some.__init__', 'Some.for_test', 'Another.__init__', 'Another.for_test'],
                id="Multiple classes with same methods"
            )
        ]
    )
    def test__func_called__result_returned(self, module, expect):
        tree = ast.parse(module)
        methods = list(FuncFinder.get_methods(tree))

        result = list(FuncFinder.get_node_qual_name(m) for m in methods)

        assert result == expect


@pytest.mark.pointer(target=FuncFinder.__iter__)
class TestFuncFinderIter:
    def test__func_called__result_returned(self, ):
        funcs = FuncFinder(Path(for_func_finder.__file__).parent)

        assert set(funcs) == {'pytest_pointers.tests.mock_structure.for_func_finder.Some.__init__',
                              'pytest_pointers.tests.mock_structure.for_func_finder.Some.for_test',
                              'pytest_pointers.tests.mock_structure.for_func_finder.Another.__init__',
                              'pytest_pointers.tests.mock_structure.for_func_finder.for_test',
                              'pytest_pointers.tests.mock_structure.for_func_finder.Another.for_test'}


@pytest.mark.pointer(target=FuncFinder.get_py_files)
class TestFuncFinderGetPyFiles:
    @pytest.mark.parametrize(
        ('files', 'files_ignored'),
        [
            (
                    ["dir1/module.py", "dir1/module2.py", ],
                    [".venv/pack1/module.py", ".venv/pack2/module.py", ]
            ),
            (
                    ["dir1/module.py", "dir2/pack1/m.py", "dir2/pack1/m2.py", ],
                    [".venv/pack1/module.py", ]
            ),
            (
                    ["dir1/module.py", "dir2/pack1/m.py", "dir2/pack1/m2.py", ],
                    ["dir1/tests/test_module.py", ]
            ),
        ]
    )
    def test__func_called__result_returned(self, tmp_path, files, files_ignored):
        files_path = [tmp_path / Path(f) for f in files]
        files_ignored_path = [tmp_path / Path(f) for f in files_ignored]

        for f in files_path + files_ignored_path:
            f.parent.mkdir(parents=True, exist_ok=True)
            f.touch()

        result = FuncFinder(start_dir=tmp_path).get_py_files()
        assert len(result - set(files_path)) == 0
