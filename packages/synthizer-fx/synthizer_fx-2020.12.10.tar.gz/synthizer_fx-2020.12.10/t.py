from atexit import register

from synthizer import *

initialize()
register(shutdown)
c = Context()
s = DirectSource(c)
g = BufferGenerator(c)
g.buffer = Buffer.from_stream('file', 'sound.wav')
r = GlobalFdnReverb(c)
c.config_route(s, r)
s.add_generator(g)


def f(thing):
    return sorted(x for x in dir(thing) if not x.startswith('_'))
