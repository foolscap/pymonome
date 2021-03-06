#! /usr/bin/env python3

import asyncio
import monome

from life import Life

class PagesSerialOsc(monome.SerialOsc):
    def __init__(self, app1, app2, loop=None, autoconnect_app=None):
        super().__init__(loop, autoconnect_app)
        self.app1 = app1
        self.app2 = app2

    async def pages_connect(self, port):
        transport, grid = await self.loop.create_datagram_endpoint(monome.Grid, local_addr=('127.0.0.1', 0), remote_addr=('127.0.0.1', port))

        page1 = monome.Page()
        page2 = monome.Page()
        page_manager = monome.SeqPageManager(grid=grid, pages=[page1, page2])

        self.app1.attach(page1)
        self.app2.attach(page2)

        page_manager.connect()

    def on_device_added(self, id, type, port):
        asyncio.async(self.pages_connect(port))

if __name__ == "__main__":
    life1 = Life()
    life2 = Life()

    loop = asyncio.get_event_loop()
    asyncio.async(PagesSerialOsc.create(loop=loop, app1=life1, app2=life2))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        life1.quit()
        life2.quit()
