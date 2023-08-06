import aiohttp
from blam3sdk.runconfig import RunConfig
from blam3sdk.blam.extensions import deserialise

class BlamClient(object):
    def __init__(self, run_config: RunConfig) -> None:
        self.base_url = run_config.api_endpoint
        self.headers = { "Authorization": "Bearer " + run_config.bearer_token }

    async def search_assets(self, query: str, limit: int=None):
        return await self._get_async(f'assets', { query: query, limit: limit })    

    async def get_asset_by_id(self, id: int):
        return await self._get_async(f'assets/{id}')

    async def create_asset(self, obj):
        return await self._post_async(f'assets', obj)

    async def get_asset_version_by_id(self, id: int):
        return await self._get_async(f'assets/versions/{id}')

    async def create_asset_version(self, obj):
        return await self._post_async(f'assets/versions', obj)

    async def get_asset_file_by_id(self, id: int):
        return await self._get_async(f'assets/versions/files/{id}')

    async def create_asset_file(self, obj):
        return await self._post_async(f'assets/versions/files', obj)

    async def create_file_location(self, obj):
        return await self._post_async(f'assets/versions/files/locations', obj)

    async def get_file_stores(self, id: int=None):
        if not id:
            return await self._get_async(f'filestores')
        else:
            return await self._get_async(f'filestores?fileStoreSchemaId={id}')

    async def get_file_store_schemas(self):
        return await self._get_async(f'filestores/schemas')
    
    async def _get_async(self, path: str, params=None):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            if params is None:
                async with session.get(self.base_url + '/' + path.strip(' /')) as response:
                    response.raise_for_status()
                    output = await response.json()
            else:
                async with session.get(self.base_url + '/' + path.strip(' /'), params=params) as response:
                    response.raise_for_status()
                    output = await response.json()
        return deserialise(output)

    async def _post_async(self, path: str, obj):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(self.base_url + '/' + path.strip(' /'), json=obj) as response:
                response.raise_for_status()
                output = await response.json()
        return deserialise(output)
