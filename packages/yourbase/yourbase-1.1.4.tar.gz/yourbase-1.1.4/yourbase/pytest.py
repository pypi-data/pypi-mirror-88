# This file sets up YourBase pytest integration.
#
# For projects using pytest, the project only needs to add yourbase to its
# requirements file. This file will be run as an entry point (via setup.py) and
# will attach to pytest hooks so that tests do not need to be decorated.
#
# For projects not using pytest, or when running outside of the YourBase CI,
# this file does nothing.

import atexit
import inspect
import os
import yourbase

from typing import List, Optional

if yourbase.ENABLED:
    try:
        import pytest

        print("[YB] pytest found, attaching")
        from . import skip_when_possible

        def pytest_collection_modifyitems(items: List[pytest.Item]) -> None:
            """
            Called by pytest after tests are collected but before they start
            to run. `items` is mutable.

            Modern pytest's signature for this function is
            `pytest_collection_modifyitems(session, config, items)`, but
            pytest will check argument names before calling it and call with
            exactly the right arguments so that plugins gain forward
            compaitibility for free.

            For this reason, we shouldn't update this function signature to
            the modern version until we need something from it, as it would
            potentially break compatibility with older pytest versions. We
            also should not rename the arguments as this would prevent pytest
            from identifying them and cause it to error.

            For more information, see: https://github.com/pytest-dev/pytest/blob/991bc7bd50772b0ae1f40b5f821f7e67745d1b2e/doc/en/writing_plugins.rst#hook-function-validation-and-execution
            """
            if not yourbase.PLUGIN:
                return

            for item in items:
                fname = "%s" % (item.function.__qualname__)
                fpath = os.getcwd() + os.sep + inspect.getfile(item.function)

                if yourbase.PLUGIN.can_skip(fpath, fname):
                    item.add_marker(
                        pytest.mark.skip(reason="[YB] No dependencies changed ✨")
                    )

        def pytest_runtest_setup(item: pytest.Item) -> None:
            """
            Called by pytest before a single test is about to be run. This
            function is NOT called if the test is marked for skipping.
            """
            if not yourbase.PLUGIN:
                return

            fname = "%s" % (item.function.__qualname__)
            fpath = os.getcwd() + os.sep + inspect.getfile(item.function)

            yourbase.PLUGIN.start_test(fpath, fname)

        # TODO: This is called even when the test is skipped. Maybe check pytest to see if this is intended.
        def pytest_runtest_teardown(
            item: pytest.Item, nextitem: Optional[pytest.Item]
        ) -> None:
            """
            Called by pytest after a single test has been run. This function
            IS called even if the test was skipped.
            """
            if not yourbase.PLUGIN:
                return

            fname = "%s" % (item.function.__qualname__)
            fpath = os.getcwd() + os.sep + inspect.getfile(item.function)

            yourbase.PLUGIN.end_test(fpath, fname)

    except ModuleNotFoundError:
        print(
            "[YB] YourBase pytest code was initiated, but pytest wasn't found. Is pytest installed oddly?"
        )
