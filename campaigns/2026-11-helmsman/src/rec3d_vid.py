import asyncio, glob, os
from playwright.async_api import async_playwright
A=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=A)
        ctx = await b.new_context(viewport={'width':1280,'height':800}, record_video_dir='/home/claude/gifs/raw', record_video_size={'width':1280,'height':800})
        pg = await ctx.new_page()
        await pg.goto('http://localhost:8765/playground/'); await pg.wait_for_timeout(3500)
        await pg.mouse.click(1183,33); await pg.wait_for_timeout(2500)
        t0 = await pg.evaluate('performance.now()')
        await pg.mouse.move(354,427); await pg.wait_for_timeout(500)
        await pg.mouse.click(354,427); await pg.wait_for_timeout(3500)
        await pg.mouse.move(800,300,steps=12); await pg.wait_for_timeout(300)
        await pg.mouse.dblclick(800,257); await pg.wait_for_timeout(3800)
        await pg.screenshot(path='/tmp/dive.png')
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(3000)
        await pg.mouse.click(354,427); await pg.wait_for_timeout(1500)
        await ctx.close(); await b.close()
asyncio.run(main())
