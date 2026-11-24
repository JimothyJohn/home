import asyncio, sys, os
from playwright.async_api import async_playwright
page, out, t0, t1, fps, y0, h = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
async def main():
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width':960,'height':468})
        await pg.goto('file://'+page); await pg.wait_for_timeout(600)
        n=int((t1-t0)*fps)
        for i in range(n):
            await pg.evaluate(f'render({t0+i/fps})')
            await pg.screenshot(path=f'{out}/f{i:04d}.png', clip={'x':0,'y':y0,'width':960,'height':h})
        await b.close()
asyncio.run(main())
