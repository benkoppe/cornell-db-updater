import httpx
from pydantic import BaseModel

from typing import Type, TypeVar

from cornell_db_updater.config import settings
import cornell_db_updater.api.types as Cornell


# definitions to relate api routes to their corresponding pydantic types
class CornellAPIRoute(BaseModel):
    route: str
    response_data_key: str


# map of pydantic types to their corresponding api routes
API_ROUTES: dict[Type[BaseModel], CornellAPIRoute] = {
    Cornell.Roster: CornellAPIRoute(
        route="config/rosters", response_data_key="rosters"
    ),
    Cornell.AcademicCareer: CornellAPIRoute(
        route="config/acadCareers", response_data_key="classes"
    ),
    Cornell.AcademicGroup: CornellAPIRoute(
        route="config/acadGroups", response_data_key="classes"
    ),
    Cornell.ClassLevel: CornellAPIRoute(
        route="config/classLevels", response_data_key="classes"
    ),
    Cornell.Subject: CornellAPIRoute(
        route="config/subjects", response_data_key="subjects"
    ),
    Cornell.Class: CornellAPIRoute(route="search/classes", response_data_key="classes"),
}


# generic type for the desired return type of fetch_cornell_data
TReturnType = TypeVar("TReturnType", bound=BaseModel)


async def fetch_cornell_data(
    type: Type[TReturnType], roster: str | None = None, subject: str | None = None
) -> list[TReturnType]:
    api_route = API_ROUTES[type]

    if not api_route:
        raise ValueError(f"Invalid type {type}")

    search_params = {}

    if roster:
        search_params["roster"] = roster
    if subject:
        search_params["subject"] = subject

    path = create_cornell_path(api_route.route)

    async with httpx.AsyncClient() as client:
        r = await client.get(path, params=search_params)
        data = response_to_data(r, api_route.response_data_key)
        instances = parse_data(data, type)

    return instances


def create_cornell_path(route: str) -> str:
    return f"https://{settings.CORNELL_API_HOST}/api/{settings.CORNELL_API_VERSION}/{route}.json"


def response_to_data(
    response: httpx.Response,
    data_key: str,
) -> list[str]:
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch data from {response.url}")

    data = response.json()

    if "data" not in data:
        raise ValueError(f"Invalid data returned from {response.url}")

    data = data["data"]

    if data_key not in data:
        raise ValueError(f"Invalid data returned from {response.url}")

    return data[data_key]


def parse_data(data: list[str], type: Type[TReturnType]) -> list[TReturnType]:
    instances = []

    for datum in data:
        typed_datum = type(**datum)
        instances.append(typed_datum)

    return instances


if __name__ == "__main__":
    import asyncio

    data = asyncio.run(fetch_cornell_data(Cornell.Class, roster="SU24", subject="WRIT"))

    print(data)
