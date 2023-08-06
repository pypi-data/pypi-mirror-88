import logging
import web_minify.processor
import datetime
import time
import os

logger = logging.getLogger(__name__)


def test_true():
    logger.info("Dummy unit test")
    return True


def get_mtime(filename):
    return os.path.getmtime(filename)


def set_mtime(filename, t):
    os.utime(filename, (t, t))


def create_dummy_file(filename, content, time=None):
    with open(filename, "w", encoding="utf-8") as file:
        written = file.write(content)
        assert written == len(content)
    if time:
        set_mtime(filename, time)
    actual_time = get_mtime(filename)
    logger.info(f"Created dummy file '{filename}' with content '{content}' and time {time} (actual {actual_time})")
    return actual_time


def test_processor():
    now = datetime.datetime.now().timestamp()

    existant_input_fn = "existant_input.js"
    existant_input_content = "existant_content"
    existant_input_mtime = create_dummy_file(existant_input_fn, existant_input_content)

    existant_input_empty_fn = "existant_input_empty.js"
    existant_input_empty_content = ""
    existant_input_empty_mtime = create_dummy_file(existant_input_empty_fn, existant_input_empty_content)

    existant_output_older_fn = "existant_output_older.js"
    existant_output_older_content = ""
    existant_output_older_mtime = existant_input_mtime - 100
    assert existant_output_older_mtime == create_dummy_file(existant_output_older_fn, existant_output_older_content, existant_output_older_mtime)

    existant_output_same_fn = "existant_input_same.js"
    existant_output_same_content = ""
    existant_output_same_mtime = existant_input_mtime
    assert existant_output_same_mtime == create_dummy_file(existant_output_same_fn, existant_output_same_content, existant_output_same_mtime)

    existant_output_newer_fn = "existant_input_newer.js"
    existant_output_newer_content = ""
    existant_output_newer_mtime = existant_input_mtime + 100
    assert existant_output_newer_mtime == create_dummy_file(existant_output_newer_fn, existant_output_newer_content, existant_output_newer_mtime)

    defaults = {"format": "", "overwrite": True, "on_change": True, "verbose": False, "zipy": False, "sort": False, "comments": False, "timestamp": False, "wrap": False, "input": "", "output": ""}

    args = {"input": "inexistant_input.js"}
    settings = {**defaults, **args}
    p = web_minify.processor.Processor(settings)
    sane, message = p.sanity_checks()
    assert not sane, message

    args = {"input": existant_input_fn}
    settings = {**defaults, **args}
    p = web_minify.processor.Processor(settings)
    sane, message = p.sanity_checks()
    assert sane, message

    success, copied, skipped, message = p.process_file(input_path=existant_input_fn, output_path=existant_output_same_fn)
    assert success, message
    assert not copied, message
    assert skipped, message

    success, copied, skipped, message = p.process_file(input_path=existant_input_fn, output_path=existant_output_older_fn)
    assert success, message
    assert not copied, message
    assert not skipped, message

    success, copied, skipped, message = p.process_file(input_path=existant_input_fn, output_path=existant_output_newer_fn)
    assert success, message
    assert not copied, message
    assert skipped, message
