import asyncio
from typing import Any

from playwright.async_api import (
    Page,
    async_playwright,
    Response
)

GPT_FILL = '//*[@id="textareaAutosize"]'
GPT_BUTTON = '//button[contains(@class, "group absolute right-3 bottom-2 rounded-xl transition-colors")]'
GPT_NEW_CHAT = '//*[contains(text(), "New chat")]'


class PlayWrightCrawler:

    @staticmethod
    async def base_action(
        page: Page,
        xpath,
        timeout,
        action,
        **kwargs
    ) -> Any:
        try:
            result: str = await getattr(page.locator(xpath), action)(timeout=timeout, **kwargs)
            return result

        except Exception as error:
            raise error from None

    async def click_xpath(
        self,
        page: Page,
        xpath,
        timeout: int = 5_000
    ):
        return await self.base_action(
            page, xpath, timeout, action="click",
        )

    async def read_from_xpath(
        self,
        page: Page,
        xpath,
        timeout: int = 2_000
    ):
        return await self.base_action(
            page, xpath, timeout, action="text_content",
        )

    async def get_all_elements(
        self,
        page: Page,
        xpath,
        timeout: int = 5_000
    ):
        return await self.base_action(
            page, xpath, timeout, action="all",
        )

    async def fill_form(
        self,
        page: Page,
        xpath,
        timeout: int = 5_000,
        text: str | None = None
    ):
        return await self.base_action(
            page, xpath, timeout, action="fill",
            value=text
        )


async def interact_with_chatgpt(input: str):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            pwc = PlayWrightCrawler()

            await page.goto("https://chatbot.theb.ai/#/chat/")

            await pwc.fill_form(
                page=page,
                xpath='//input[@placeholder="Email"]',
                text='sepehrshafiee1379@gmail.com',
            )
            await pwc.fill_form(
                page = page,
                xpath = '//input[@placeholder="Password"]',
                text = 'MR.admin1379',
            )
            await pwc.click_xpath(
                page = page,
                xpath = '//button[contains(@class,"btn-blue")]'
            )

            await page.locator('//header[@id="driver-popover-title"]').wait_for(timeout=10000)
            element_count = await page.locator('//button[contains(@class,"driver-popover-close-btn")]').count()
            while element_count:
                if element_count > 0:
                    await pwc.click_xpath(
                        page=page,
                        xpath='//button[contains(@class,"driver-popover-close-btn")]'
                        )
                await asyncio.sleep(0.3)
                element_count = await page.locator('//button[contains(@class,"driver-popover-close-btn")]').count()

            await page.locator('//div[contains(@class, "hover:bg-[#138DFF]'
                                     ' group/item hover:text-n-1 cursor-pointer rounded-xl'
                                     ' items-center flex px-3 gap-4 py-2 w-full")]').nth(5).click()
            await pwc.fill_form(
                page=page,
                xpath=GPT_FILL,
                text=input,
            )
            await pwc.click_xpath(page, GPT_BUTTON)

            response: Response | None = None
            while response is None:
                _temp = await page.wait_for_event("response", timeout=120000)
                if "gen_title" in _temp.url:
                    response = _temp
            await page.locator('//div[contains(@class, "print-actions")]//button').nth(3).wait_for(timeout=120000)
            await page.locator('//div[contains(@class, "print-actions")]//button').nth(3).click()
            await asyncio.sleep(0.2)
            selector = '//div[contains(@class, "flex items-start overflow-x-auto whitespace-pre-wrap break-words flex-col mt-5")]'
            data = await page.locator(selector).evaluate("element => element.innerHTML")

            await asyncio.sleep(0.2)
            await browser.close()
            return data
    except Exception as e:
        print(str(e))
        return None