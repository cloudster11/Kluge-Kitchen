import asyncio
from pyodide.http import pyfetch, FetchResponse
from typing import Optional, Any
from js import document


async def request(url: str, method: str = "GET", body: Optional[str] = None,
                  headers: Optional[dict[str, str]] = None, **fetch_kwargs: Any) -> FetchResponse:
    """
    Async request function. Pass in Method and make sure to await!
    Parameters:
        url: str = URL to make request to
        method: str = {"GET", "POST", "PUT", "DELETE"} from `JavaScript` global fetch())
        body: str = body as json string. Example, body=json.dumps(my_dict)
        headers: dict[str, str] = header as dict, will be converted to string...
            Example, headers=json.dumps({"Content-Type": "application/json"})
        fetch_kwargs: Any = any other keyword arguments to pass to `pyfetch` (will be passed to `fetch`)
    Return:
        response: pyodide.http.FetchResponse = use with .status or await.json(), etc.
    """
    kwargs = {"method": method, "mode": "cors"}  # CORS: https://en.wikipedia.org/wiki/Cross-origin_resource_sharing
    if body and method not in ["GET", "HEAD"]:
        kwargs["body"] = body
    if headers:
        kwargs["headers"] = headers
    kwargs.update(fetch_kwargs)

    response = await pyfetch(url, **kwargs)
    return response

currentRec = await request("https://c33894a.online-server.cloud/hourlyRecipes")

currentJson = await currentRec.json()

for x in currentJson:
    document.getElementById(f"hourly{x}src").innerText = f"{currentJson[x][4]}"
    document.getElementById(f"hourly{x}Title").innerText = f"{currentJson[x][1]}"
    document.getElementById(f"hourly{x}").setAttribute("src", f"img/{currentJson[x][0]}.png")
    document.getElementById(f"hourly{x}Dif").innerText = f"{currentJson[x][3]}/3"
    document.getElementById(f"hourly{x}Time").innerText = f"{currentJson[x][2]} min"
