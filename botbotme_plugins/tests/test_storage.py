from botbotme_plugins.base import BasePlugin, DummyApp


bp = BasePlugin()
bp.app = DummyApp()


def test_retrieve_nonexistent_key():
    assert(bp.retrieve('nobody_home') is None)


def test_store_and_retrieve():
    bp.store('michael_jacksons_pet_monkey', 'banana')
    assert(bp.retrieve('michael_jacksons_pet_monkey') == 'banana')


def test_incr():
    #key doesn't exist yet
    assert(bp.incr('lindsey_lohan') == 1)
    #incr key with current value of 1
    assert(bp.incr('lindsey_lohan') == 2)
