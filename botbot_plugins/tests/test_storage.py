from botbot_plugins.base import BasePlugin, DummyApp


bp = BasePlugin()
bp.app = DummyApp()


def test_retrieve_nonexistent_key():
    "test retrieve operation on nonexistent key"
    assert(bp.retrieve('nobody_home') is None)


def test_store_and_retrieve():
    "test storing and retrieving a string value"

    first_rule = """\
        A robot may not injure a human being or, through inaction,
        allow a human being to come to harm."""
    bp.store('first_rule', first_rule)
    assert(bp.retrieve('first_rule') == first_rule)


def test_incr():
    "test that counters can be created and incremented"
    #key doesn't exist yet
    assert(bp.incr('counter') == 1)
    #incr key with current value of 1
    assert(bp.incr('counter') == 2)
