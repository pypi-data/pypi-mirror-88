"""Utility functions for creating an interpreter."""

from io import StringIO
import os
import re
from tempfile import TemporaryDirectory
from typing import List

from robot.api import get_model
from robot.errors import DataError
from robot.reporting import ResultWriter
from robot.running.model import TestSuite
from robot.running.builder.testsettings import TestDefaults
from robot.running.builder.parsers import ErrorReporter
from robot.running.builder.transformers import SettingsBuilder, SuiteBuilder
from robot.model.itemlist import ItemList

from .utils import (
    detect_robot_context, line_at_cursor, scored_results,
    complete_libraries, get_lunr_completions, remove_prefix,
    display_log, process_screenshots
)
from .selectors import (
    BrokenOpenConnection, clear_selector_highlights, get_autoit_selector_completions, get_selector_completions,
    get_white_selector_completions, get_win32_selector_completions, is_autoit_selector,
    is_selector, is_white_selector, is_win32_selector, close_current_connection, yield_current_connection
)
from .constants import VARIABLE_REGEXP, BUILTIN_VARIABLES
from .listeners import RobotKeywordsIndexerListener


class TestSuiteError(Exception):
    pass


class ErrorStream():
    def __init__(self):
        self.message = ''

    def write(self, message, flush=False):
        self.message = self.message + message

        if flush:
            self.flush()

    def flush(self):
        message_copy = str(self.message)

        self.message = ''

        raise TestSuiteError(message_copy)


class NoOpStream():
    def write(self, message, flush=False):
        # This is a no-op
        pass

    def flush(self):
        # This is a no-op
        pass


def init_suite(name: str, source: str = os.getcwd()):
    """Create a new test suite."""
    return TestSuite(name=name, source=source)


def generate_report(suite: TestSuite, outputdir: str):
    process_screenshots(outputdir)

    writer = ResultWriter(os.path.join(outputdir, "output.xml"))
    writer.write_results(
        log=os.path.join(outputdir, "log.html"),
        report=None,
        rpa=getattr(suite, "rpa", False),
    )

    with open(os.path.join(outputdir, "log.html"), "rb") as fp:
        log = fp.read()
        log = log.replace(b'"reportURL":"report.html"', b'"reportURL":null')

    html = """
        <button
          class="jp-mod-styled jp-mod-accept"
          onClick="{};event.preventDefault();event.stopPropagation();"
        >
            <i class="fa fa-file" aria-hidden="true"></i>
            Log
        </button>
        """.format(display_log(log, "log.html"))

    return {"text/html": html}


def _execute_impl(code: str, suite: TestSuite, defaults: TestDefaults = TestDefaults(),
                  stdout=None, stderr=None, listeners=[], drivers=[], outputdir=None):
    # Clear selector completion highlights
    for driver in yield_current_connection(drivers, ["RPA.Browser", "selenium", "jupyter"]):
        try:
            clear_selector_highlights(driver)
        except BrokenOpenConnection:
            close_current_connection(drivers, driver)

    # Copy keywords/variables/libraries in case of failure
    imports = get_items_copy(suite.resource.imports)
    variables = get_items_copy(suite.resource.variables)
    keywords = get_items_copy(suite.resource.keywords)

    # Compile AST
    model = get_model(
        StringIO(code),
        data_only=False,
        curdir=os.getcwd().replace("\\", "\\\\"),
    )
    ErrorReporter(code).visit(model)
    SettingsBuilder(suite, defaults).visit(model)
    SuiteBuilder(suite, defaults).visit(model)

    # Strip variables/keyword duplicates
    strip_duplicate_items(suite.resource.variables)
    strip_duplicate_items(suite.resource.keywords)

    # Set default streams
    # By default stdout is no-op
    # By default stderr raises an exception when flushing (workaround robotframework which does not raise)
    if stdout is None:
        stdout = NoOpStream()
    if stderr is None:
        stderr = ErrorStream()

    # Execute suite
    try:
        result = suite.run(outputdir=outputdir, stdout=stdout, stderr=stderr, listener=listeners)
    except TestSuiteError as e:
        # Reset keywords/variables/libraries
        set_items(suite.resource.imports, imports)
        set_items(suite.resource.variables, variables)
        set_items(suite.resource.keywords, keywords)

        clean_items(suite.tests)

        raise e

    for listener in listeners:
        if isinstance(listener, RobotKeywordsIndexerListener):
            listener.import_from_suite_data(suite)

    # Detect RPA
    suite.rpa = get_rpa_mode(model)

    report = None
    if suite.tests:
        report = generate_report(suite, outputdir)

    # Remove tests run so far,
    # this is needed so that we don't run them again in the next execution
    clean_items(suite.tests)

    return result, report


def execute(code: str, suite: TestSuite, defaults: TestDefaults = TestDefaults(),
            stdout=None, stderr=None, listeners=[], drivers=[], outputdir=None):
    """Execute a snippet of code, given the current test suite."""
    if outputdir is None:
        with TemporaryDirectory() as path:
            result = _execute_impl(code, suite, defaults, stdout, stderr, listeners, drivers, path)
    else:
        result = _execute_impl(code, suite, defaults, stdout, stderr, listeners, drivers, outputdir)

    return result


def complete(code: str, cursor_pos: int, suite: TestSuite, keywords_listener: RobotKeywordsIndexerListener = None, extra_libraries: List[str] = [], drivers=[]):
    """Complete a snippet of code, given the current test suite."""
    context = detect_robot_context(code, cursor_pos)
    cursor_pos = cursor_pos is None and len(code) or cursor_pos
    line, offset = line_at_cursor(code, cursor_pos)
    line_cursor = cursor_pos - offset
    needle = re.split(r"\s{2,}|\t| \| ", line[:line_cursor])[-1].lstrip()

    library_completion = context == "__settings__" and any(
        [
            line.lower().startswith("library "),
            "import library " in line.lower(),
            "reload library " in line.lower(),
            "get library instance" in line.lower(),
        ]
    )

    matches = []

    # Try to complete a variable
    if needle and needle[0] in "$@&%":
        potential_vars = list(set(
            [var.name for var in suite.resource.variables] +
            VARIABLE_REGEXP.findall(code) +
            BUILTIN_VARIABLES
        ))

        matches = [
            m["ref"]
            for m in scored_results(needle, [dict(ref=v) for v in potential_vars])
            if needle.lower() in m["ref"].lower()
        ]

        if len(line) > line_cursor and line[line_cursor] == "}":
            cursor_pos += 1
            needle += "}"
    # Try to complete a library name
    elif library_completion:
        needle = needle.lower()
        needle = remove_prefix(needle, 'library ')
        needle = remove_prefix(needle, 'import library ')
        needle = remove_prefix(needle, 'reload library ')
        needle = remove_prefix(needle, 'get library instance ')

        matches = complete_libraries(needle, extra_libraries)
    # Try to complete a CSS selector
    elif is_selector(needle):
        matches = []
        for driver in yield_current_connection(drivers, ["RPA.Browser", "selenium", "jupyter", "appium"]):
            matches = [get_selector_completions(needle.rstrip(), driver)[0]]
    # Try to complete an AutoIt selector
    elif is_autoit_selector(needle):
        matches = [get_autoit_selector_completions(needle)[0]]
    # Try to complete a white selector
    elif is_white_selector(needle):
        matches = [get_white_selector_completions(needle)[0]]
    # Try to complete a Windows selector
    elif is_win32_selector(needle):
        matches = [get_win32_selector_completions(needle)[0]]
    # Try to complete a keyword
    elif keywords_listener is not None:
        matches = get_lunr_completions(
            needle,
            keywords_listener.index,
            keywords_listener.keywords,
            context
        )

    return {
        "matches": matches,
        "cursor_end": cursor_pos,
        "cursor_start": cursor_pos - len(needle)
    }


def shutdown_drivers(drivers=[]):
    for driver in drivers:
        if hasattr(driver["instance"], "quit"):
            driver["instance"].quit()


def strip_duplicate_items(items: ItemList):
    """Remove duplicates from an item list."""
    new_items = {}
    for item in items:
        new_items[item.name] = item
    items._items = list(new_items.values())


def clean_items(items: ItemList):
    """Remove elements from an item list."""
    items._items = []


def set_items(items: ItemList, value: List):
    """Remove elements from an item list."""
    items._items = value


def get_items_copy(items: ItemList):
    """Get copy of an itemlist."""
    return list(items._items)


def get_rpa_mode(model):
    """Get RPA mode for the test suite."""
    if not model:
        return None
    tasks = [s.tasks for s in model.sections if hasattr(s, 'tasks')]
    if all(tasks) or not any(tasks):
        return tasks[0] if tasks else None
    raise DataError('One file cannot have both tests and tasks.')
