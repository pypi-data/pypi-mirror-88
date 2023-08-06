import aiohttp

class Client:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.base_url = 'https://www.kal-byte.co.uk/api/'

    async def password(self, length: int = None) -> str:
        if length is None:
            raise AttributeError('You must provide a length argument.')

        extension = "password_generator"
        argument = "?length={}".format(length)
        async with self.session.get(self.base_url + extension + argument) as response:
            if response.status != 200:
                raise Exception("That request raised a {} status.".format(response.status))

            data = await response.json()
            password = data['password']

        return password

    async def close(self):
        await self.session.close()