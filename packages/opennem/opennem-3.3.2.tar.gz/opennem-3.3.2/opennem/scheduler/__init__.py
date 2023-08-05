# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=no-member
from huey import RedisHuey, crontab

from opennem.api.export.map import PriorityType
from opennem.api.export.tasks import (
    export_energy,
    export_metadata,
    export_power,
)
from opennem.exporter.geojson import export_facility_geojson
from opennem.monitors.aemo_intervals import aemo_wem_live_interval
from opennem.monitors.opennem import check_opennem_interval_delays
from opennem.monitors.opennem_metadata import check_metadata_status
from opennem.settings import settings

redis_host = None

if settings.cache_url:
    redis_host = settings.cache_url.host

huey = RedisHuey("opennem.exporter", host=redis_host)
# export tasks


@huey.periodic_task(crontab(minute="*/2"))
@huey.lock_task("schedule_live_tasks")
def schedule_live_tasks() -> None:
    export_power(priority=PriorityType.live)


@huey.periodic_task(crontab(hour="*/2"))
@huey.lock_task("schedule_power_weeklies")
def schedule_power_weeklies() -> None:
    """
    Run weekly power outputs
    """
    export_power(priority=PriorityType.history, latest=True)


@huey.periodic_task(crontab(hour="*/3"))
@huey.lock_task("schedule_power_weeklies_archive")
def schedule_power_weeklies_archive() -> None:
    """
    Run weekly power outputs entire archive
    """
    export_power(priority=PriorityType.history)


@huey.periodic_task(crontab(hour="*/1"))
@huey.lock_task("schedule_hourly_tasks")
def schedule_hourly_tasks() -> None:
    export_energy(priority=PriorityType.daily, latest=True)


@huey.periodic_task(crontab(hour="*/2"))
@huey.lock_task("schedule_daily_tasks")
def schedule_daily_tasks() -> None:
    export_energy(priority=PriorityType.daily)


@huey.periodic_task(crontab(hour="*/12"))
@huey.lock_task("schedule_energy_monthlies")
def schedule_energy_monthlies() -> None:
    export_energy(priority=PriorityType.monthly)


# geojson maps
@huey.periodic_task(crontab(minute="*/30"))
@huey.lock_task("schedule_export_geojson")
def schedule_export_geojson() -> None:
    export_facility_geojson()


# metadata
@huey.periodic_task(crontab(minute="*/30"))
@huey.lock_task("schedule_export_metadata")
def schedule_export_metadata() -> None:
    export_metadata()


# monitoring tasks
@huey.periodic_task(crontab(minute="*/15"))
@huey.lock_task("monitor_opennem_intervals")
def monitor_opennem_intervals() -> None:
    for network_code in ["NEM", "WEM"]:
        check_opennem_interval_delays(network_code)


@huey.periodic_task(crontab(minute="*/15"))
@huey.lock_task("monitor_wem_interval")
def monitor_wem_interval() -> None:
    aemo_wem_live_interval()


@huey.periodic_task(crontab(hour="*/1"))
@huey.lock_task("monitor_metadata_status")
def monitor_metadata_status() -> None:
    check_metadata_status()
