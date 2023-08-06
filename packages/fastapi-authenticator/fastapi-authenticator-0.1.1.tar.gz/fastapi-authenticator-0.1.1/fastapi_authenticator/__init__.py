import asyncio
import time
from typing import Iterable, Optional, Union

import httpx
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt  # type: ignore
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request

__version__ = "0.1.1"

# https://developers.google.com/identity/protocols/oauth2/openid-connect#discovery
DEFAULT_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"


class GoogleCloudAuth:
    def __init__(
        self,
        audience: str = None,
        issuer: Union[str, Iterable[str], None] = "https://accounts.google.com",
        discovery_url: str = DEFAULT_DISCOVERY_URL,
    ):
        self.audience = audience
        self.issuer = issuer
        self.discovery_url = discovery_url
        self._jwks_uri = None
        self._public_keys: Optional[list] = None
        self._public_keys_timestamp: float = 0.0
        self._lock = asyncio.Lock()

    async def _get_jwk_uri(self, client):
        if self._jwks_uri is None:
            resp = await client.get(self.discovery_url)
            self._jwks_uri = resp.json()["jwks_uri"]
        return self._jwks_uri

    async def _fetch_public_keys(self) -> None:
        async with self._lock:
            if self._public_keys is not None and (
                time.time() - self._public_keys_timestamp <= 300
            ):
                return
            async with httpx.AsyncClient() as client:
                jwks_uri = await self._get_jwk_uri(client)
                resp = await client.get(jwks_uri)
                self._public_keys = resp.json()["keys"]
                self._public_keys_timestamp = time.time()

    async def __call__(
        self,
        request: Request,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ) -> dict:
        jwt_header = jwt.get_unverified_header(token.credentials)
        await self._fetch_public_keys()
        for public_key in self._public_keys or []:
            if public_key["kid"] == jwt_header["kid"]:
                try:
                    claims = jwt.decode(
                        token.credentials,
                        public_key,
                        audience=self.audience or str(request.url),
                        issuer=self.issuer,
                    )
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Invalid Token {e}",
                    )
                return claims
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown Token"
            )


google_cloud_auth = GoogleCloudAuth()


def google_cloud_task(request: Request):
    if request.headers.get("user-agent") != "Google-Cloud-Tasks":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid user agent")
    hs = request.headers
    return GoogleCloudTask(
        queue_name=hs["x-cloudtasks-queuename"],
        name=hs["x-cloudtasks-taskname"],
        retry_count=int(hs["x-cloudtasks-taskretrycount"]),
        execution_count=int(hs["x-cloudtasks-taskexecutioncount"]),
        eta=float(hs["x-cloudtasks-tasketa"]),
    )


def google_cloud_scheduler(request: Request):
    if request.headers.get("user-agent") != "Google-Cloud-Scheduler":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid user agent")
    return request.headers.get("x-cloudscheduler") == "true"


class GoogleCloudTask(BaseModel):
    queue_name: str
    name: str
    retry_count: int
    execution_count: int
    eta: float
