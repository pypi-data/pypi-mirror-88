import os
import aiohttp
from aiohttp import ClientSession, TCPConnector, TraceConfig
import asyncio
import logging


# @all_methods(method_logger)
class Requester:
    def __init__(self, asyncio_loop, client_access_token=None):

        self.API_ROOT = 'https://api.genius.com/'
        self.PUBLIC_API_ROOT = 'https://genius.com/api/'
        self.WEB_ROOT = 'https://genius.com/'

        # https://stackoverflow.com/questions/55273927/how-can-i-optimize-this-asyncio-slice-of-code-to-make-more-requests-per-second-i
        connector = TCPConnector(limit=5000)
        trace_config = TraceConfig()
        trace_config.on_request_start.append(self.on_request_start)
        trace_config.on_request_end.append(self.on_request_end)
        self.session = ClientSession(connector=connector, trace_configs=[trace_config])

        self.loop = asyncio_loop

        if client_access_token is None:
            client_access_token = os.environ.get("GENIUS_ACCESS_TOKEN")

        self.client_access_token = client_access_token

        self.access_token = (
            "Bearer " + client_access_token if client_access_token else None
        )
        self.authorization_header = {"authorization": self.access_token}

        self.retries = 5
        self.sleep_time = 10

    async def on_request_start(self, _session, trace_config_ctx, _params):
        trace_config_ctx.start = self.loop.time()

    async def on_request_end(self, _session, trace_config_ctx, params):
        elapsed = self.loop.time() - trace_config_ctx.start
        logging.info(f"Request took {elapsed} for {params.url}")

    async def make_request(
        self,
        path: str,
        params: dict = None,
        public_api: bool = False,
        web: bool = False,
        method: str = "GET",
        **kwargs,
    ) -> object:

        if public_api:
            uri = self.PUBLIC_API_ROOT
            header = None
        elif web:
            uri = self.WEB_ROOT
            header = None
        else:
            uri = self.API_ROOT
            header = self.authorization_header

        uri += path

        # Make the request
        response = None
        tries = 0
        wait_retries = 0

        if isinstance(params, dict):  # Some params will be list, eg. PublicAPI.referents
            params = {k: v for k, v in params.items() if v is not None} if params else None

        while response is None and tries <= self.retries:
            tries += 1
            try:
                async with self.session.request(
                    method=method,
                    url=uri,
                    params=params,
                    headers=header,
                    raise_for_status=True,
                    **kwargs,
                ) as response:
                    if web:
                        text_response = await response.text()
                        return text_response
                    elif response.status == 200:
                        res = await response.json()
                        return res.get("response", res)
                    elif response.status == 204:  # No content error
                        return "" if web else {}
                    else:
                        pass

            # Exceptions for which we should wait before retrying
            except (aiohttp.ClientConnectionError, aiohttp.ClientResponseError):
                wait_retries += 1
                # We don't exactly know how long to wait so we make sure we wait more at each try
                await asyncio.sleep(self.sleep_time * wait_retries)
                pass

            # Let's retry right away for those
            except aiohttp.ClientPayloadError:
                pass

            except asyncio.TimeoutError:
                pass

        return "" if web else {}
