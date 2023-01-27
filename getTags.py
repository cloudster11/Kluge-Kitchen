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

allTags = await request("https://c33894a.online-server.cloud/tags")

currentJson = await allTags.json()

row = 0
col = 5
for x in currentJson:
    if col == 5:
        row += 1
        newRow = document.createElement("tr")
        newRow.setAttribute("id", f"r_{row}")
        document.getElementById("tagTable").append(newRow)
        col = 0


    newCol = document.createElement("td")
    newCol.setAttribute("id", f"r_{row}_c_{col}")

    document.getElementById(f"r_{row}").append(newCol)

    element = document.createElement("input")
    element.setAttribute("type", "checkbox")
    element.setAttribute("id", f"{x}")
    element.setAttribute("value", f"{x}")
    document.getElementById(f"r_{row}_c_{col}").append(element)

    label = document.createElement("label")
    label.setAttribute("for", f"{x}")
    label.innerText = f"  {currentJson[x]}"
    document.getElementById(f"r_{row}_c_{col}").append(label)
    col += 1

#    element = document.createElement("input")
#    element.setAttribute("type", "checkbox")
#    element.setAttribute("value", f"{x}")
#    document.getElementById("tags").append(element)

