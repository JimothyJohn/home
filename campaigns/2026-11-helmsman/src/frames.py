import asyncio, sys, os
from playwright.async_api import async_playwright
page, out, dur, fps = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
async def main():
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width':960,'height':468}, device_scale_factor=1)
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://'+page); await pg.wait_for_timeout(600)
        n=int(dur*fps)
        for i in range(n):
            await pg.evaluate(f'render({i/fps})')
            await pg.screenshot(path=f'{out}/f{i:04d}.png')
        print('frames',n,'errors',errs); await b.close()
asyncio.run(main())
