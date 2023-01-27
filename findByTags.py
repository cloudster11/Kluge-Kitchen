import asyncio
import json

from pyodide.http import pyfetch, FetchResponse
from typing import Optional, Any
from js import document
from pyodide import create_proxy



async def search(self):
    currentIds = []
    currentDoms = []
    allCheckboxes = document.getElementsByClassName("checkTag")
    tagList = "?tags="
    for x in allCheckboxes:
        if x.checked:
            tagList += x.value
            tagList += "_"
    if tagList[-1] == "_":
        tagList = tagList[:-1]
    else:
        y = document.getElementById("recipePreview")
        if y:
            y.remove()

        element = document.createElement("div")
        element.setAttribute("align", "center")
        element.setAttribute("id", "recipePreview")
        document.getElementsByClassName("background")[0].append(element)

        y = document.getElementById("warning")
        if y:
            y.remove()

        element = document.createElement("h1")
        element.setAttribute("class", "headingSmall")
        element.setAttribute("id", "warning")
        element.innerText = "Bitte min. 1 Tag auswählen!"
        document.getElementById(f"recipePreview").append(element)


        return


    recipes = await request(f"https://c33894a.online-server.cloud/byTags{tagList}")

    currentJson = await recipes.json()

    if len(currentJson) == 0:
        y = document.getElementById("recipePreview")
        if y:
            y.remove()

        element = document.createElement("div")
        element.setAttribute("align", "center")
        element.setAttribute("id", "recipePreview")
        document.getElementsByClassName("background")[0].append(element)

        y = document.getElementById("warning")
        if y:
            y.remove()

        element = document.createElement("h1")
        element.setAttribute("class", "headingSmall")
        element.setAttribute("id", "warning")
        element.innerText = "Keine Rezepte gefunden!"
        document.getElementById(f"recipePreview").append(element)


        return



    else:
        y = document.getElementById("recipePreview")
        if y:
            y.remove()

        element = document.createElement("div")
        element.setAttribute("align", "center")
        element.setAttribute("id", "recipePreview")
        document.getElementsByClassName("background")[0].append(element)

        y = document.getElementById("warning")
        if y:
            y.remove()

        element = document.createElement("h1")
        element.setAttribute("class", "headingSmall")
        element.setAttribute("id", "warning")
        element.innerText = "Gefundene Rezepte:"
        document.getElementById(f"recipePreview").append(element)



        for recipe in currentJson:
            currentIds.append(recipe)
            recipeFull = await request(f"https://c33894a.online-server.cloud/byId?id={recipe}")
            recipeFull = await recipeFull.json()

            recipeImg = f"<img src=\"img/{recipe}.png\">"
            recDiv = document.createElement("div")
            recDiv.innerHTML = f"""
                <table width="70%">
                    <tr>
                        <td id="{recipe}_1_1" rowspan="2" class="recipePic">{recipeImg}</td>
                        <td id="{recipe}_1_2" colspan="2" width="75%" class="title">{recipeFull["name"]}</td>
                    </tr>
                    <tr>
                        <td id="{recipe}_2_2" width="50%"><p class="title">Dauer: {recipeFull["time"]} min</p></td>
                        <td id="{recipe}_2_3" width="20%" class="title">Schwierigkeit: {recipeFull["difficulty"]}/3</td>
                    </tr>
                </table>
            """

            document.getElementById("recipePreview").append(recDiv)


    for x in currentIds:
        y = document.getElementById(f"{x}_1_1")
        y.addEventListener("click", create_proxy(showRec))
        currentDoms.append(y)



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





e = document.getElementById("search")
e.addEventListener("click", create_proxy(search))
