# A copy 'n paste of parts of IPython TestCompleter unit tests that will run with our monkey patched version to ensure
# we preserve the original behavior and keep up to date with new IPython versions.
# RIP-318 tracks the current backwards compatibility failures
# See the original here: https://github.com/ipython/ipython/blob/master/IPython/core/tests/test_completer.py
import sys
import os
import pytest
import textwrap
import unittest

from IPython import get_ipython
from IPython.core import completer
from IPython.utils.tempdir import TemporaryDirectory, TemporaryWorkingDirectory
from IPython.utils.generics import complete_object
from IPython.core.completer import (
    Completion,
    provisionalcompleter,
    match_dict_keys,
    _deduplicate_completions,
)
from riptable.Utils.ipython_utils import enable_custom_attribute_completion
from riptable.test_tooling_integration.ipython_integration_test import greedy_completion
from riptable.Utils.teamcity_helper import is_running_in_teamcity


class NoseTestMock:
    """IPython tests require the nose module, a deprecated module for testing.
    NoseTestMock will replace the nose functions with corresponding unittest functions.
    """

    def __init__(self):
        t = unittest.TestCase()
        self.assert_true = t.assertTrue
        self.assert_true = t.assertTrue
        self.assert_false = t.assertFalse
        self.assert_equal = t.assertEqual
        self.assert_in = t.assertIn
        self.assert_not_in = t.assertNotIn
        self.assert_list_equal = t.assertListEqual


nt = NoseTestMock()
assert_in = nt.assert_in
assert_not_in = nt.assert_not_in


# Todo add IPython baseline version and ensure ipython_utils._monkey_patched__complete stays up to date
# Below is a copy of IPython/core/tests/test_completer.py TestComleter that enables our custom completer
# and enables it in the TestCompleter.setUp.
# RIP-318 tracks the current backwards compatibility failures and they are marked below with an
# @pytest.mark.xfail decorator.


# region IPython/core/tests/test_completer.py
def check_line_split(splitter, test_specs):
    for part1, part2, split in test_specs:
        cursor_pos = len(part1)
        line = part1 + part2
        out = splitter.split_line(line, cursor_pos)
        nt.assert_equal(out, split)


class NamedInstanceMetaclass(type):
    def __getitem__(cls, item):
        return cls.get_instance(item)


class NamedInstanceClass(metaclass=NamedInstanceMetaclass):
    def __init__(self, name):
        if not hasattr(self.__class__, "instances"):
            self.__class__.instances = {}
        self.__class__.instances[name] = self

    @classmethod
    def _ipython_key_completions_(cls):
        return cls.instances.keys()

    @classmethod
    def get_instance(cls, name):
        return cls.instances[name]


class KeyCompletable:
    def __init__(self, things=()):
        self.things = things

    def _ipython_key_completions_(self):
        return list(self.things)


class TestCompleter(unittest.TestCase):
    def setUp(self):
        """
        We want to silence all PendingDeprecationWarning when testing the completer
        """
        self._assertwarns = self.assertWarns(PendingDeprecationWarning)
        self._assertwarns.__enter__()

        enable_custom_attribute_completion()

    def tearDown(self):
        try:
            self._assertwarns.__exit__(None, None, None)
        except AssertionError:
            pass

    def test_custom_completion_error(self):
        """Test that errors from custom attribute completers are silenced."""
        ip = get_ipython()

        class A:
            pass

        ip.user_ns["x"] = A()

        @complete_object.register(A)
        def complete_A(a, existing_completions):
            raise TypeError("this should be silenced")

        ip.complete("x.")

    def test_custom_completion_ordering(self):
        """Test that errors from custom attribute completers are silenced."""
        ip = get_ipython()

        _, matches = ip.complete('in')
        assert matches.index('input') < matches.index('int')

        def complete_example(a):
            return ['example2', 'example1']

        ip.Completer.custom_completers.add_re('ex*', complete_example)
        _, matches = ip.complete('ex')
        assert matches.index('example2') < matches.index('example1')

    def test_unicode_completions(self):
        ip = get_ipython()
        # Some strings that trigger different types of completion.  Check them both
        # in str and unicode forms
        s = ["ru", "%ru", "cd /", "floa", "float(x)/"]
        for t in s + list(map(str, s)):
            # We don't need to check exact completion values (they may change
            # depending on the state of the namespace, but at least no exceptions
            # should be thrown and the return value should be a pair of text, list
            # values.
            text, matches = ip.complete(t)
            nt.assert_true(isinstance(text, str))
            nt.assert_true(isinstance(matches, list))

    def test_latex_completions(self):
        from IPython.core.latex_symbols import latex_symbols
        import random

        ip = get_ipython()
        # Test some random unicode symbols
        keys = random.sample(latex_symbols.keys(), 10)
        for k in keys:
            text, matches = ip.complete(k)
            nt.assert_equal(len(matches), 1)
            nt.assert_equal(text, k)
            nt.assert_equal(matches[0], latex_symbols[k])
        # Test a more complex line
        text, matches = ip.complete("print(\\alpha")
        nt.assert_equal(text, "\\alpha")
        nt.assert_equal(matches[0], latex_symbols["\\alpha"])
        # Test multiple matching latex symbols
        text, matches = ip.complete("\\al")
        nt.assert_in("\\alpha", matches)
        nt.assert_in("\\aleph", matches)

    @pytest.mark.xfail(reason="RIP-318 - AssertionError: 0 != 1")
    @pytest.mark.skipif(
        is_running_in_teamcity(), reason="Please remove alongside xfail removal."
    )
    def test_back_latex_completion(self):
        ip = get_ipython()

        # do not return more than 1 matches fro \beta, only the latex one.
        name, matches = ip.complete("\\β")
        nt.assert_equal(len(matches), 1)
        nt.assert_equal(matches[0], "\\beta")

    @pytest.mark.xfail(reason="RIP-318 - AssertionError: 0 != 1")
    @pytest.mark.skipif(
        is_running_in_teamcity(), reason="Please remove alongside xfail removal."
    )
    def test_back_unicode_completion(self):
        ip = get_ipython()

        name, matches = ip.complete("\\Ⅴ")
        nt.assert_equal(len(matches), 1)
        nt.assert_equal(matches[0], "\\ROMAN NUMERAL FIVE")

    @pytest.mark.xfail(reason="RIP-318 - AssertionError: 0 != 1")
    @pytest.mark.skipif(
        is_running_in_teamcity(), reason="Please remove alongside xfail removal."
    )
    def test_forward_unicode_completion(self):
        ip = get_ipython()

        name, matches = ip.complete("\\ROMAN NUMERAL FIVE")
        nt.assert_equal(len(matches), 1)
        nt.assert_equal(matches[0], "Ⅴ")

    @pytest.mark.xfail(
        reason="RIP-318 - AssertionError: Lists differ: ['\\jmath'] != []"
    )
    @pytest.mark.skipif(
        is_running_in_teamcity(), reason="Please remove alongside xfail removal."
    )
    def test_no_ascii_back_completion(self):
        ip = get_ipython()
        with TemporaryWorkingDirectory():  # Avoid any filename completions
            # single ascii letter that don't have yet completions
            for letter in "jJ":
                name, matches = ip.complete("\\" + letter)
                nt.assert_equal(matches, [])

    class CompletionSplitterTestCase(unittest.TestCase):
        def setUp(self):
            self.sp = completer.CompletionSplitter()

        def test_delim_setting(self):
            self.sp.delims = " "
            nt.assert_equal(self.sp.delims, " ")
            nt.assert_equal(self.sp._delim_expr, r"[\ ]")

        def test_spaces(self):
            """Test with only spaces as split chars."""
            self.sp.delims = " "
            t = [("foo", "", "foo"), ("run foo", "", "foo"), ("run foo", "bar", "foo")]
            check_line_split(self.sp, t)

    def test_has_open_quotes1(self):
        for s in ["'", "'''", "'hi' '"]:
            nt.assert_equal(completer.has_open_quotes(s), "'")

    def test_has_open_quotes2(self):
        for s in ['"', '"""', '"hi" "']:
            nt.assert_equal(completer.has_open_quotes(s), '"')

    def test_has_open_quotes3(self):
        for s in ["''", "''' '''", "'hi' 'ipython'"]:
            nt.assert_false(completer.has_open_quotes(s))

    def test_has_open_quotes4(self):
        for s in ['""', '""" """', '"hi" "ipython"']:
            nt.assert_false(completer.has_open_quotes(s))

    @pytest.mark.xfail(
        sys.platform == "win32", reason="RIP-318 - abspath completions fail on Windows"
    )
    @pytest.mark.skipif(
        is_running_in_teamcity(), reason="Please remove alongside xfail removal."
    )
    def test_abspath_file_completions(self):
        ip = get_ipython()
        with TemporaryDirectory() as tmpdir:
            prefix = os.path.join(tmpdir, "foo")
            suffixes = ["1", "2"]
            names = [prefix + s for s in suffixes]
            for n in names:
                open(n, "w").close()

            # Check simple completion
            c = ip.complete(prefix)[1]
            nt.assert_equal(c, names)

            # Now check with a function call
            cmd = 'a = f("%s' % prefix
            c = ip.complete(prefix, cmd)[1]
            comp = [prefix + s for s in suffixes]
            nt.assert_equal(c, comp)

    def test_local_file_completions(self):
        ip = get_ipython()
        with TemporaryWorkingDirectory():
            prefix = "./foo"
            suffixes = ["1", "2"]
            names = [prefix + s for s in suffixes]
            for n in names:
                open(n, "w").close()

            # Check simple completion
            c = ip.complete(prefix)[1]
            nt.assert_equal(c, names)

            # Now check with a function call
            cmd = 'a = f("%s' % prefix
            c = ip.complete(prefix, cmd)[1]
            comp = {prefix + s for s in suffixes}
            nt.assert_true(comp.issubset(set(c)))

    def test_quoted_file_completions(self):
        ip = get_ipython()
        with TemporaryWorkingDirectory():
            name = "foo'bar"
            open(name, "w").close()

            # Don't escape Windows
            escaped = name if sys.platform == "win32" else "foo\\'bar"

            # Single quote matches embedded single quote
            text = "open('foo"
            c = ip.Completer._complete(
                cursor_line=0, cursor_pos=len(text), full_text=text
            )[1]
            nt.assert_equal(c, [escaped])

            # Double quote requires no escape
            text = 'open("foo'
            c = ip.Completer._complete(
                cursor_line=0, cursor_pos=len(text), full_text=text
            )[1]
            nt.assert_equal(c, [name])

            # No quote requires an escape
            text = "%ls foo"
            c = ip.Completer._complete(
                cursor_line=0, cursor_pos=len(text), full_text=text
            )[1]
            nt.assert_equal(c, [escaped])

    @pytest.mark.xfail(
        reason="RIP-318 - assert ['TestClass.T...TestClass.a1'] == ['TestClass.a', 'TestClass.a1']"
    )
    @pytest.mark.skipif(
        is_running_in_teamcity(), reason="Please remove alongside xfail removal."
    )
    def test_all_completions_dups(self):
        """
        Make sure the output of `IPCompleter.all_completions` does not have
        duplicated prefixes.
        """
        ip = get_ipython()
        c = ip.Completer
        ip.ex("class TestClass():\n\ta=1\n\ta1=2")
        for jedi_status in [True, False]:
            with provisionalcompleter():
                ip.Completer.use_jedi = jedi_status
                matches = c.all_completions("TestCl")
                assert matches == ['TestClass'], jedi_status
                matches = c.all_completions("TestClass.")
                assert len(matches) > 2, jedi_status
                matches = c.all_completions("TestClass.a")
                assert matches == ['TestClass.a', 'TestClass.a1'], jedi_status

    def test_jedi(self):
        """
        A couple of issue we had with Jedi
        """
        ip = get_ipython()

        def _test_complete(reason, s, comp, start=None, end=None):
            l = len(s)
            start = start if start is not None else l
            end = end if end is not None else l
            with provisionalcompleter():
                ip.Completer.use_jedi = True
                completions = set(ip.Completer.completions(s, l))
                ip.Completer.use_jedi = False
                assert_in(Completion(start, end, comp), completions, reason)

        def _test_not_complete(reason, s, comp):
            l = len(s)
            with provisionalcompleter():
                ip.Completer.use_jedi = True
                completions = set(ip.Completer.completions(s, l))
                ip.Completer.use_jedi = False
                assert_not_in(Completion(l, l, comp), completions, reason)

        import jedi

        jedi_version = tuple(int(i) for i in jedi.__version__.split(".")[:3])
        if jedi_version > (0, 10):
            yield _test_complete, "jedi >0.9 should complete and not crash", "a=1;a.", "real"
        yield _test_complete, "can infer first argument", 'a=(1,"foo");a[0].', "real"
        yield _test_complete, "can infer second argument", 'a=(1,"foo");a[1].', "capitalize"
        yield _test_complete, "cover duplicate completions", "im", "import", 0, 2

        yield _test_not_complete, "does not mix types", 'a=(1,"foo");a[0].', "capitalize"

    def test_completion_have_signature(self):
        """
        Lets make sure jedi is capable of pulling out the signature of the function we are completing.
        """
        ip = get_ipython()
        with provisionalcompleter():
            ip.Completer.use_jedi = True
            completions = ip.Completer.completions("ope", 3)
            c = next(completions)  # should be `open`
            ip.Completer.use_jedi = False
        assert "file" in c.signature, "Signature of function was not found by completer"
        assert (
            "encoding" in c.signature
        ), "Signature of function was not found by completer"

    def test_deduplicate_completions(self):
        """
        Test that completions are correctly deduplicated (even if ranges are not the same)
        """
        ip = get_ipython()
        ip.ex(
            textwrap.dedent(
                """
        class Z:
            zoo = 1
        """
            )
        )
        with provisionalcompleter():
            ip.Completer.use_jedi = True
            l = list(
                _deduplicate_completions("Z.z", ip.Completer.completions("Z.z", 3))
            )
            ip.Completer.use_jedi = False

        assert len(l) == 1, "Completions (Z.z<tab>) correctly deduplicate: %s " % l
        assert l[0].text == "zoo"  # and not `it.accumulate`

    def test_greedy_completions(self):
        """
        Test the capability of the Greedy completer.

        Most of the test here does not really show off the greedy completer, for proof
        each of the text below now pass with Jedi. The greedy completer is capable of more.

        See the :any:`test_dict_key_completion_contexts`

        """
        ip = get_ipython()
        ip.ex("a=list(range(5))")
        _, c = ip.complete(".", line="a[0].")
        nt.assert_false(".real" in c, "Shouldn't have completed on a[0]: %s" % c)

        def _(line, cursor_pos, expect, message, completion):
            with greedy_completion(), provisionalcompleter():
                ip.Completer.use_jedi = False
                _, c = ip.complete(".", line=line, cursor_pos=cursor_pos)
                nt.assert_in(expect, c, message % c)

                ip.Completer.use_jedi = True
                with provisionalcompleter():
                    completions = ip.Completer.completions(line, cursor_pos)
                nt.assert_in(completion, completions)

        with provisionalcompleter():
            yield _, "a[0].", 5, "a[0].real", "Should have completed on a[0].: %s", Completion(
                5, 5, "real"
            )
            yield _, "a[0].r", 6, "a[0].real", "Should have completed on a[0].r: %s", Completion(
                5, 6, "real"
            )

            yield _, "a[0].from_", 10, "a[0].from_bytes", "Should have completed on a[0].from_: %s", Completion(
                5, 10, "from_bytes"
            )

#    @pytest.mark.xfail(reason="RIP-318 - requires traitlets module")
#    @pytest.mark.skipif(
#        is_running_in_teamcity(), reason="Please remove alongside xfail removal."
#    )
#    def test_omit__names(self):
# deleted due to lint failure

#    @pytest.mark.xfail(reason="RIP-318 - requires traitlets module")
#    @pytest.mark.skipif(
#        is_running_in_teamcity(), reason="Please remove alongside xfail removal."
#    )
#    def test_limit_to__all__False_ok(self):
#        """
#        Limit to all is deprecated, once we remove it this test can go away.
#        """
#        ip = get_ipython()
#        c = ip.Completer
#        c.use_jedi = False
#        ip.ex("class D: x=24")
#        ip.ex("d=D()")
#        cfg = Config()
#        cfg.IPCompleter.limit_to__all__ = False
#        c.update_config(cfg)
#        s, matches = c.complete("d.")
#        nt.assert_in("d.x", matches)

    def test_get__all__entries_ok(self):
        class A:
            __all__ = ["x", 1]

        words = completer.get__all__entries(A())
        nt.assert_equal(words, ["x"])

    def test_get__all__entries_no__all__ok(self):
        class A:
            pass

        words = completer.get__all__entries(A())
        nt.assert_equal(words, [])

    def test_func_kw_completions(self):
        ip = get_ipython()
        c = ip.Completer
        c.use_jedi = False
        ip.ex("def myfunc(a=1,b=2): return a+b")
        s, matches = c.complete(None, "myfunc(1,b")
        nt.assert_in("b=", matches)
        # Simulate completing with cursor right after b (pos==10):
        s, matches = c.complete(None, "myfunc(1,b)", 10)
        nt.assert_in("b=", matches)
        s, matches = c.complete(None, 'myfunc(a="escaped\\")string",b')
        nt.assert_in("b=", matches)
        # builtin function
        s, matches = c.complete(None, "min(k, k")
        nt.assert_in("key=", matches)

    def test_default_arguments_from_docstring(self):
        ip = get_ipython()
        c = ip.Completer
        kwd = c._default_arguments_from_docstring("min(iterable[, key=func]) -> value")
        nt.assert_equal(kwd, ["key"])
        # with cython type etc
        kwd = c._default_arguments_from_docstring(
            "Minuit.migrad(self, int ncall=10000, resume=True, int nsplit=1)\n"
        )
        nt.assert_equal(kwd, ["ncall", "resume", "nsplit"])
        # white spaces
        kwd = c._default_arguments_from_docstring(
            "\n Minuit.migrad(self, int ncall=10000, resume=True, int nsplit=1)\n"
        )
        nt.assert_equal(kwd, ["ncall", "resume", "nsplit"])

    def test_line_magics(self):
        ip = get_ipython()
        c = ip.Completer
        s, matches = c.complete(None, "lsmag")
        nt.assert_in("%lsmagic", matches)
        s, matches = c.complete(None, "%lsmag")
        nt.assert_in("%lsmagic", matches)

    def test_cell_magics(self):
        from IPython.core.magic import register_cell_magic

        @register_cell_magic
        def _foo_cellm(line, cell):
            pass

        ip = get_ipython()
        c = ip.Completer

        s, matches = c.complete(None, "_foo_ce")
        nt.assert_in("%%_foo_cellm", matches)
        s, matches = c.complete(None, "%%_foo_ce")
        nt.assert_in("%%_foo_cellm", matches)

    def test_line_cell_magics(self):
        from IPython.core.magic import register_line_cell_magic

        @register_line_cell_magic
        def _bar_cellm(line, cell):
            pass

        ip = get_ipython()
        c = ip.Completer

        # The policy here is trickier, see comments in completion code.  The
        # returned values depend on whether the user passes %% or not explicitly,
        # and this will show a difference if the same name is both a line and cell
        # magic.
        s, matches = c.complete(None, "_bar_ce")
        nt.assert_in("%_bar_cellm", matches)
        nt.assert_in("%%_bar_cellm", matches)
        s, matches = c.complete(None, "%_bar_ce")
        nt.assert_in("%_bar_cellm", matches)
        nt.assert_in("%%_bar_cellm", matches)
        s, matches = c.complete(None, "%%_bar_ce")
        nt.assert_not_in("%_bar_cellm", matches)
        nt.assert_in("%%_bar_cellm", matches)

    def test_magic_completion_order(self):
        ip = get_ipython()
        c = ip.Completer

        # Test ordering of line and cell magics.
        text, matches = c.complete("timeit")
        nt.assert_equal(matches, ["%timeit", "%%timeit"])

    def test_magic_completion_shadowing(self):
        ip = get_ipython()
        c = ip.Completer
        c.use_jedi = False

        # Before importing matplotlib, %matplotlib magic should be the only option.
        text, matches = c.complete("mat")
        nt.assert_equal(matches, ["%matplotlib"])

        # The newly introduced name should shadow the magic.
        ip.run_cell("matplotlib = 1")
        text, matches = c.complete("mat")
        nt.assert_equal(matches, ["matplotlib"])

        # After removing matplotlib from namespace, the magic should again be
        # the only option.
        del ip.user_ns["matplotlib"]
        text, matches = c.complete("mat")
        nt.assert_equal(matches, ["%matplotlib"])

    def test_magic_completion_shadowing_explicit(self):
        """
        If the user try to complete a shadowed magic, and explicit % start should
        still return the completions.
        """
        ip = get_ipython()
        c = ip.Completer

        # Before importing matplotlib, %matplotlib magic should be the only option.
        text, matches = c.complete("%mat")
        nt.assert_equal(matches, ["%matplotlib"])

        ip.run_cell("matplotlib = 1")

        # After removing matplotlib from namespace, the magic should still be
        # the only option.
        text, matches = c.complete("%mat")
        nt.assert_equal(matches, ["%matplotlib"])

    def test_magic_config(self):
        ip = get_ipython()
        c = ip.Completer

        s, matches = c.complete(None, "conf")
        nt.assert_in("%config", matches)
        s, matches = c.complete(None, "conf")
        nt.assert_not_in("AliasManager", matches)
        s, matches = c.complete(None, "config ")
        nt.assert_in("AliasManager", matches)
        s, matches = c.complete(None, "%config ")
        nt.assert_in("AliasManager", matches)
        s, matches = c.complete(None, "config Ali")
        nt.assert_list_equal(["AliasManager"], matches)
        s, matches = c.complete(None, "%config Ali")
        nt.assert_list_equal(["AliasManager"], matches)
        s, matches = c.complete(None, "config AliasManager")
        nt.assert_list_equal(["AliasManager"], matches)
        s, matches = c.complete(None, "%config AliasManager")
        nt.assert_list_equal(["AliasManager"], matches)
        s, matches = c.complete(None, "config AliasManager.")
        nt.assert_in("AliasManager.default_aliases", matches)
        s, matches = c.complete(None, "%config AliasManager.")
        nt.assert_in("AliasManager.default_aliases", matches)
        s, matches = c.complete(None, "config AliasManager.de")
        nt.assert_list_equal(["AliasManager.default_aliases"], matches)
        s, matches = c.complete(None, "config AliasManager.de")
        nt.assert_list_equal(["AliasManager.default_aliases"], matches)

    def test_magic_color(self):
        ip = get_ipython()
        c = ip.Completer

        s, matches = c.complete(None, "colo")
        nt.assert_in("%colors", matches)
        s, matches = c.complete(None, "colo")
        nt.assert_not_in("NoColor", matches)
        s, matches = c.complete(None, "%colors")  # No trailing space
        nt.assert_not_in("NoColor", matches)
        s, matches = c.complete(None, "colors ")
        nt.assert_in("NoColor", matches)
        s, matches = c.complete(None, "%colors ")
        nt.assert_in("NoColor", matches)
        s, matches = c.complete(None, "colors NoCo")
        nt.assert_list_equal(["NoColor"], matches)
        s, matches = c.complete(None, "%colors NoCo")
        nt.assert_list_equal(["NoColor"], matches)

    def test_match_dict_keys(self):
        """
        Test that match_dict_keys works on a couple of use case does return what
        expected, and does not crash
        """
        delims = " \t\n`!@#$^&*()=+[{]}\\|;:'\",<>?"

        keys = ["foo", b"far"]
        assert match_dict_keys(keys, "b'", delims=delims) == ("'", 2, ["far"])
        assert match_dict_keys(keys, "b'f", delims=delims) == ("'", 2, ["far"])
        assert match_dict_keys(keys, 'b"', delims=delims) == ('"', 2, ["far"])
        assert match_dict_keys(keys, 'b"f', delims=delims) == ('"', 2, ["far"])

        assert match_dict_keys(keys, "'", delims=delims) == ("'", 1, ["foo"])
        assert match_dict_keys(keys, "'f", delims=delims) == ("'", 1, ["foo"])
        assert match_dict_keys(keys, '"', delims=delims) == ('"', 1, ["foo"])
        assert match_dict_keys(keys, '"f', delims=delims) == ('"', 1, ["foo"])

        match_dict_keys

    def test_dict_key_completion_string(self):
        """Test dictionary key completion for string keys"""
        ip = get_ipython()
        complete = ip.Completer.complete

        ip.user_ns["d"] = {"abc": None}

        # check completion at different stages
        _, matches = complete(line_buffer="d[")
        nt.assert_in("'abc'", matches)
        nt.assert_not_in("'abc']", matches)

        _, matches = complete(line_buffer="d['")
        nt.assert_in("abc", matches)
        nt.assert_not_in("abc']", matches)

        _, matches = complete(line_buffer="d['a")
        nt.assert_in("abc", matches)
        nt.assert_not_in("abc']", matches)

        # check use of different quoting
        _, matches = complete(line_buffer='d["')
        nt.assert_in("abc", matches)
        nt.assert_not_in('abc"]', matches)

        _, matches = complete(line_buffer='d["a')
        nt.assert_in("abc", matches)
        nt.assert_not_in('abc"]', matches)

        # check sensitivity to following context
        _, matches = complete(line_buffer="d[]", cursor_pos=2)
        nt.assert_in("'abc'", matches)

        _, matches = complete(line_buffer="d['']", cursor_pos=3)
        nt.assert_in("abc", matches)
        nt.assert_not_in("abc'", matches)
        nt.assert_not_in("abc']", matches)

        # check multiple solutions are correctly returned and that noise is not
        ip.user_ns["d"] = {
            "abc": None,
            "abd": None,
            "bad": None,
            object(): None,
            5: None,
        }

        _, matches = complete(line_buffer="d['a")
        nt.assert_in("abc", matches)
        nt.assert_in("abd", matches)
        nt.assert_not_in("bad", matches)
        assert not any(m.endswith(("]", '"', "'")) for m in matches), matches

        # check escaping and whitespace
        ip.user_ns["d"] = {"a\nb": None, "a'b": None, 'a"b': None, "a word": None}
        _, matches = complete(line_buffer="d['a")
        nt.assert_in("a\\nb", matches)
        nt.assert_in("a\\'b", matches)
        nt.assert_in('a"b', matches)
        nt.assert_in("a word", matches)
        assert not any(m.endswith(("]", '"', "'")) for m in matches), matches

        # - can complete on non-initial word of the string
        _, matches = complete(line_buffer="d['a w")
        nt.assert_in("word", matches)

        # - understands quote escaping
        _, matches = complete(line_buffer="d['a\\'")
        nt.assert_in("b", matches)

        # - default quoting should work like repr
        _, matches = complete(line_buffer="d[")
        nt.assert_in('"a\'b"', matches)

        # - when opening quote with ", possible to match with unescaped apostrophe
        _, matches = complete(line_buffer="d[\"a'")
        nt.assert_in("b", matches)

        # need to not split at delims that readline won't split at
        if "-" not in ip.Completer.splitter.delims:
            ip.user_ns["d"] = {"before-after": None}
            _, matches = complete(line_buffer="d['before-af")
            nt.assert_in("before-after", matches)

    def test_dict_key_completion_contexts(self):
        """Test expression contexts in which dict key completion occurs"""
        ip = get_ipython()
        complete = ip.Completer.complete
        d = {"abc": None}
        ip.user_ns["d"] = d

        class C:
            data = d

        ip.user_ns["C"] = C
        ip.user_ns["get"] = lambda: d

        def assert_no_completion(**kwargs):
            _, matches = complete(**kwargs)
            nt.assert_not_in("abc", matches)
            nt.assert_not_in("abc'", matches)
            nt.assert_not_in("abc']", matches)
            nt.assert_not_in("'abc'", matches)
            nt.assert_not_in("'abc']", matches)

        def assert_completion(**kwargs):
            _, matches = complete(**kwargs)
            nt.assert_in("'abc'", matches)
            nt.assert_not_in("'abc']", matches)

        # no completion after string closed, even if reopened
        assert_no_completion(line_buffer="d['a'")
        assert_no_completion(line_buffer='d["a"')
        assert_no_completion(line_buffer="d['a' + ")
        assert_no_completion(line_buffer="d['a' + '")

        # completion in non-trivial expressions
        assert_completion(line_buffer="+ d[")
        assert_completion(line_buffer="(d[")
        assert_completion(line_buffer="C.data[")

        # greedy flag
        def assert_completion(**kwargs):
            _, matches = complete(**kwargs)
            nt.assert_in("get()['abc']", matches)

        assert_no_completion(line_buffer="get()[")
        with greedy_completion():
            assert_completion(line_buffer="get()[")
            assert_completion(line_buffer="get()['")
            assert_completion(line_buffer="get()['a")
            assert_completion(line_buffer="get()['ab")
            assert_completion(line_buffer="get()['abc")

    def test_dict_key_completion_bytes(self):
        """Test handling of bytes in dict key completion"""
        ip = get_ipython()
        complete = ip.Completer.complete

        ip.user_ns["d"] = {"abc": None, b"abd": None}

        _, matches = complete(line_buffer="d[")
        nt.assert_in("'abc'", matches)
        nt.assert_in("b'abd'", matches)

        if False:  # not currently implemented
            _, matches = complete(line_buffer="d[b")
            nt.assert_in("b'abd'", matches)
            nt.assert_not_in("b'abc'", matches)

            _, matches = complete(line_buffer="d[b'")
            nt.assert_in("abd", matches)
            nt.assert_not_in("abc", matches)

            _, matches = complete(line_buffer="d[B'")
            nt.assert_in("abd", matches)
            nt.assert_not_in("abc", matches)

            _, matches = complete(line_buffer="d['")
            nt.assert_in("abc", matches)
            nt.assert_not_in("abd", matches)

    def test_dict_key_completion_unicode_py3(self):
        """Test handling of unicode in dict key completion"""
        ip = get_ipython()
        complete = ip.Completer.complete

        ip.user_ns["d"] = {"a\u05d0": None}

        # query using escape
        if sys.platform != "win32":
            # Known failure on Windows
            _, matches = complete(line_buffer="d['a\\u05d0")
            nt.assert_in("u05d0", matches)  # tokenized after \\

        # query using character
        _, matches = complete(line_buffer="d['a\u05d0")
        nt.assert_in("a\u05d0", matches)

        with greedy_completion():
            # query using escape
            _, matches = complete(line_buffer="d['a\\u05d0")
            nt.assert_in("d['a\\u05d0']", matches)  # tokenized after \\

            # query using character
            _, matches = complete(line_buffer="d['a\u05d0")
            nt.assert_in("d['a\u05d0']", matches)

    # @dec.skip_without("numpy")
    def test_struct_array_key_completion(self):
        """Test dict key completion applies to numpy struct arrays"""
        import numpy

        ip = get_ipython()
        complete = ip.Completer.complete
        ip.user_ns["d"] = numpy.array([], dtype=[("hello", "f"), ("world", "f")])
        _, matches = complete(line_buffer="d['")
        nt.assert_in("hello", matches)
        nt.assert_in("world", matches)
        # complete on the numpy struct itself
        dt = numpy.dtype(
            [("my_head", [("my_dt", ">u4"), ("my_df", ">u4")]), ("my_data", ">f4", 5)]
        )
        x = numpy.zeros(2, dtype=dt)
        ip.user_ns["d"] = x[1]
        _, matches = complete(line_buffer="d['")
        nt.assert_in("my_head", matches)
        nt.assert_in("my_data", matches)
        # complete on a nested level
        with greedy_completion():
            ip.user_ns["d"] = numpy.zeros(2, dtype=dt)
            _, matches = complete(line_buffer="d[1]['my_head']['")
            nt.assert_true(any(["my_dt" in m for m in matches]))
            nt.assert_true(any(["my_df" in m for m in matches]))

    # @dec.skip_without("pandas")
    def test_dataframe_key_completion(self):
        """Test dict key completion applies to pandas DataFrames"""
        import pandas

        ip = get_ipython()
        complete = ip.Completer.complete
        ip.user_ns["d"] = pandas.DataFrame({"hello": [1], "world": [2]})
        _, matches = complete(line_buffer="d['")
        nt.assert_in("hello", matches)
        nt.assert_in("world", matches)

    def test_dict_key_completion_invalids(self):
        """Smoke test cases dict key completion can't handle"""
        ip = get_ipython()
        complete = ip.Completer.complete

        ip.user_ns["no_getitem"] = None
        ip.user_ns["no_keys"] = []
        ip.user_ns["cant_call_keys"] = dict
        ip.user_ns["empty"] = {}
        ip.user_ns["d"] = {"abc": 5}

        _, matches = complete(line_buffer="no_getitem['")
        _, matches = complete(line_buffer="no_keys['")
        _, matches = complete(line_buffer="cant_call_keys['")
        _, matches = complete(line_buffer="empty['")
        _, matches = complete(line_buffer="name_error['")
        _, matches = complete(line_buffer="d['\\")  # incomplete escape

    def test_object_key_completion(self):
        ip = get_ipython()
        ip.user_ns["key_completable"] = KeyCompletable(["qwerty", "qwick"])

        _, matches = ip.Completer.complete(line_buffer="key_completable['qw")
        nt.assert_in("qwerty", matches)
        nt.assert_in("qwick", matches)

    def test_class_key_completion(self):
        ip = get_ipython()
        NamedInstanceClass("qwerty")
        NamedInstanceClass("qwick")
        ip.user_ns["named_instance_class"] = NamedInstanceClass

        _, matches = ip.Completer.complete(line_buffer="named_instance_class['qw")
        nt.assert_in("qwerty", matches)
        nt.assert_in("qwick", matches)

    def test_tryimport(self):
        """
        Test that try-import don't crash on trailing dot, and import modules before
        """
        from IPython.core.completerlib import try_import

        assert try_import("IPython.")

    def test_aimport_module_completer(self):
        ip = get_ipython()
        _, matches = ip.complete("i", "%aimport i")
        nt.assert_in("io", matches)
        nt.assert_not_in("int", matches)

    def test_nested_import_module_completer(self):
        ip = get_ipython()
        _, matches = ip.complete(None, "import IPython.co", 17)
        nt.assert_in("IPython.core", matches)
        nt.assert_not_in("import IPython.core", matches)
        nt.assert_not_in("IPython.display", matches)

    def test_import_module_completer(self):
        ip = get_ipython()
        _, matches = ip.complete("i", "import i")
        nt.assert_in("io", matches)
        nt.assert_not_in("int", matches)

    def test_from_module_completer(self):
        ip = get_ipython()
        _, matches = ip.complete("B", "from io import B", 16)
        nt.assert_in("BytesIO", matches)
        nt.assert_not_in("BaseException", matches)

    def test_snake_case_completion(self):
        ip = get_ipython()
        ip.Completer.use_jedi = False
        ip.user_ns["some_three"] = 3
        ip.user_ns["some_four"] = 4
        _, matches = ip.complete("s_", "print(s_f")
        nt.assert_in("some_three", matches)
        nt.assert_in("some_four", matches)

    def test_mix_terms(self):
        ip = get_ipython()
        from textwrap import dedent

        ip.Completer.use_jedi = False
        ip.ex(
            dedent(
                """
            class Test:
                def meth(self, meth_arg1):
                    print("meth")

                def meth_1(self, meth1_arg1, meth1_arg2):
                    print("meth1")

                def meth_2(self, meth2_arg1, meth2_arg2):
                    print("meth2")
            test = Test()
            """
            )
        )
        _, matches = ip.complete(None, "test.meth(")
        nt.assert_in("meth_arg1=", matches)
        nt.assert_not_in("meth2_arg1=", matches)


# endregion IPython/core/tests/test_completer.py


if __name__ == '__main__':
    tester = unittest.main()
