import click
import os
import random
from db.db import get_all_channel_ids, save_channel_id, have_watched, save_to_watched
from youtube.youtube import get_videos

@click.group()
def cli():
    pass

@click.command()
@click.argument('id', nargs=-1)
def save(id):
    count = 0
    for channel_id in id:
        save_channel_id(id)
        count += 1
    click.echo(f"Saved {count} channels")

@click.command()
def channels():
    click.echo(get_all_channel_ids())

@click.command()
@click.option('--count', default=5, help="Number of videos to watch")
def gumbo(count):

    channels = get_all_channel_ids()
    gumbo = random.sample(channels, count if len(channels) > 5 else len(channels) )
    path = '/Applications/IINA.app/Contents/MacOS/iina-cli'
    videos = []
    for c_id in gumbo:
        videos = videos + get_videos(c_id)
    for vid in videos:
        click.echo(vid["title"])
        if not have_watched(vid):
            path = f'{path} "https://www.youtube.com/watch?v={vid["videoId"]}"'
    if click.confirm('These cool?', abort=True):
        os.system(f"{path}")
        save_to_watched(videos)

cli.add_command(save)
cli.add_command(gumbo)
cli.add_command(channels)

if __name__ == "__main__":
    cli()