
import asyncio
from goslideapi import GoSlideLocal

loop = asyncio.get_event_loop()
goslide = GoSlideLocal()

x = loop.run_until_complete(goslide.slide_add('192.168.30.13','KjdtZ7yL'))
x = loop.run_until_complete(goslide.slide_info('192.168.30.13'))
print(x)

