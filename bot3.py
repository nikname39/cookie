import asyncio, discord, gspread, os
from selenium import webdriver
from oauth2client.service_account import ServiceAccountCredentials

client = discord.Client()

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('cookierunkingdom-319800-a62259183b71.json', scope)
gc = gspread.authorize(credentials)

@client.event
async def on_ready():
    await bt(['"!도움말"을 이용해보세요!', '구리 제작'])

@client.event
async def on_message(message):
    if message.content.startswith("!도움말"):
        embed = discord.Embed(title="명령어 모음",
                              description="계정과 쿠폰을 추가하여 사용합니다. \n추가한 신규 쿠폰은 계정에 자동 등록됩니다.\n(서버 상태에 따라 안될 수 있음.)",
                              color=0x00ff56)
        embed.set_author(name="쿠키런 쿠폰등록", url="https://game.devplay.com/coupon/ck/ko",
                         icon_url="https://raw.githubusercontent.com/nikname39/cookie/main/goorie.PNG")
        embed.set_thumbnail(url="https://raw.githubusercontent.com/nikname39/cookie/main/cookie.jpg")
        embed.add_field(name="!도움말", value="명령어들을 볼 수 있습니다.", inline=False)
        embed.add_field(name="!가입 + 이메일", value="쿠폰을 등록할 계정을 추가합니다.", inline=False)
        embed.add_field(name="!쿠폰 + 쿠폰번호", value="신규 쿠폰을 추가합니다.", inline=False)
        embed.set_image(url="https://raw.githubusercontent.com/nikname39/cookie/main/divide.gif")
        embed.set_footer(text="\n Powered by 재훈")
        await message.channel.send(embed=embed)

    if message.content.startswith("!쿠폰"):
        word = message.content.split(" ")
        word_ = message.content.replace("!쿠폰 ", "")

        gc1 = gc.open("Cookiedata").worksheet('Couponlist')
        C_data = gc1.col_values(1)

        for i in range(0, len(C_data)):
            if C_data[i] == word[1]:
                await message.channel.send("❌이미 추가된 쿠폰입니다.")
                break
            elif 16 != len(word[1]):
                await message.channel.send("❌쿠폰 번호는 16자리입니다.")
                break
            elif i == (len(C_data)-1):
                gc1.append_row([word[1], str(message.author)])
                await message.channel.send(":white_check_mark:쿠폰이 추가 되었습니다.")
                await refresh()
                break

    if message.content.startswith("!가입"):
        word = message.content.split(" ")
        word_ = message.content.replace("!가입 ", "")

        gc2 = gc.open("Cookiedata").worksheet('Memberlist')
        M_data = gc2.col_values(1)

        for i in range(0, len(M_data)):
            if M_data[i] == word[1]:
                await message.channel.send("❌이미 추가된 계정입니다.")
                break

            elif i == (len(M_data)-1):
                gc2.append_row([word[1], str(message.author)])
                await message.channel.send(":white_check_mark:계정이 추가 되었습니다.")
                await refresh()
                break

    if message.content == "!새로고침":
        await message.channel.send(":white_check_mark:새로고침 완료.")
        await refresh()


async def bt(games):
    await client.wait_until_ready()
    while not client.is_closed():
        await client.change_presence(status=discord.Status.online, activity=discord.Game('동기화'))
        await refresh()
        for i in range(360):
            for g in games:
                await client.change_presence(status=discord.Status.online, activity=discord.Game(g))
                await asyncio.sleep(5)


async def refresh():

    gc2 = gc.open("Cookiedata").worksheet('Memberlist')
    emaillist = gc2.col_values(1)

    gc1 = gc.open("Cookiedata").worksheet('Couponlist')
    codelist = gc1.col_values(1)

    Url = 'https://game.devplay.com/coupon/ck/ko'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    browser.get(Url)

    driver.get(page_url)
    for i in range(len(emaillist)):
        driver.find_element_by_id('email-box').click()
        driver.find_element_by_id('email-box').clear()
        driver.find_element_by_id('email-box').send_keys(emaillist[i])
        for i in range(len(codelist)):
            driver.find_element_by_id('code-box').click()
            driver.find_element_by_id('code-box').clear()
            driver.find_element_by_id('code-box').send_keys(codelist[i])
            driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/form/div[4]/div').click()
            await asyncio.sleep(1)
            try:
                driver.switch_to.alert.accept()
            except:
                print("에러없음")
    driver.quit()

client.run(token)
