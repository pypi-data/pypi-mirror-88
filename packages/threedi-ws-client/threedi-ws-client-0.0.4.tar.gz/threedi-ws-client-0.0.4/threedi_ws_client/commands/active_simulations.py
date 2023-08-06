import asyncio
from urllib.parse import urlparse
import signal

import click
from threedi_api_client.threedi_api_client import ThreediApiClient

from threedi_ws_client.ws_client import WebsocketClient
from threedi_ws_client.settings import get_settings
from threedi_ws_client.models.monitor import ActiveSimulations


async def shutdown(signal_inst: signal):
    """
    try to shut down gracefully
    """
    click.secho(f"Received exit signal {signal_inst.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    click.secho("Canceling outstanding tasks")
    await asyncio.gather(*tasks)


async def startup(env):
    env_file = f"{env}.env"
    active_sims = ActiveSimulations(env_file)
    await asyncio.gather(
        active_sims.run_monitor(),
    )


@click.command()
@click.option(
    "--env",
    required=True,
    type=click.Choice(["prod", "stag", "local"], case_sensitive=False),
    help="The destination environment",
)
@click.pass_context
def run(ctx: click.Context, env: str):
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown(s))
        )
    asyncio.run(startup(env))


if __name__ == "__main__":
    run()
