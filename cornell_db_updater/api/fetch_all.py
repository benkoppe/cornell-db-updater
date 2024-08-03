import asyncio
from typing import Dict, List

import cornell_db_updater.api.types as Cornell
from cornell_db_updater.api.fetch import fetch_cornell_data


CornellAPIData = Dict[Cornell.Roster, Dict[Cornell.Subject, List[Cornell.Class]]]

DOWNLOAD_LIMIT = 20


async def gather_with_concurrency(n, *coros):
    semaphore = asyncio.Semaphore(n)

    async def sem_coro(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(*(sem_coro(coro) for coro in coros))


async def fetch_all_data() -> CornellAPIData:
    all_rosters = await fetch_all_rosters()
    all_data = {}

    for roster in all_rosters:
        if not roster:
            return
        all_data[roster] = {}
        subjects = await fetch_roster_subjects(roster)

        async def fetch_subject_data(subject: Cornell.Subject):
            if not subject:
                return
            classes = await fetch_roster_subject_classes(roster, subject)
            all_data[roster][subject] = classes

        subjects_coros = [fetch_subject_data(subject) for subject in subjects]
        await gather_with_concurrency(DOWNLOAD_LIMIT, *subjects_coros)

    return all_data


async def fetch_all_rosters() -> list[Cornell.Roster]:
    return await fetch_cornell_data(Cornell.Roster)


async def fetch_roster_subjects(roster: Cornell.Roster) -> list[Cornell.Subject]:
    return await fetch_cornell_data(Cornell.Subject, roster=roster.slug)


async def fetch_roster_subject_classes(
    roster: Cornell.Roster, subject: Cornell.Subject
) -> list[Cornell.Class]:
    print("fetching classes for", roster.slug, subject.value)
    return await fetch_cornell_data(
        Cornell.Class, roster=roster.slug, subject=subject.value
    )


async def main() -> None:
    sem = asyncio.Semaphore(10)
    async with sem:
        data = await fetch_all_data()
        print(data)


if __name__ == "__main__":
    asyncio.run(main())
