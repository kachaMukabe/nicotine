import click
import os
import random
import questionary
from db.db import get_all_channels, save_channel, have_watched, save_to_watched, pop_from_list
from youtube.youtube import get_videos, get_channel_details

@click.group()
def cli():
    pass

@click.command()
@click.argument('ids', nargs=-1)
def save(ids):
    count = 0
    for channel_id in ids:
        details = get_channel_details(channel_id)
        title = details["snippet"]["title"]
        channel_details = {
            "name": title,
            "channel_id": channel_id,
            "tag": "gen"
        }
        save_channel(channel_details)
        count += 1
    click.echo(f"Saved {count} channels")

@click.command()
def latest():
    channels = get_all_channels()
    choice = questionary.checkbox("select channels",channels).ask()
    click.echo(choice)

@click.command()
def channels():
    echo = get_all_channels()
    click.echo(len(echo))

@click.command()
@click.option('--count', default=5, help="Number of videos to watch")
def gumbo(count):

    channels = get_all_channels()
    gumbo = random.sample(channels, 18 if len(channels) > 5 else len(channels) )
    
    videos = []
    for channel in gumbo:
        # click.echo(channel["channel_id"])
        videos = videos + get_videos(channel["channel_id"])
    # click.echo(videos)
    vid_choices = questionary.checkbox("Select Videos", [video["title"] for video in videos]).ask()
    click.echo(vid_choices)
    to_watch = [video for video in videos if video["title"] in vid_choices]
    click.echo(to_watch)
    watch(to_watch)

def watch(videos):
    if len(videos) > 0:
        path = '/Applications/IINA.app/Contents/MacOS/iina-cli'
        for vid in videos:
            click.echo(vid["title"])
            if not have_watched(vid):
                path = f'{path} "https://www.youtube.com/watch?v={vid["videoId"]}"'
        if click.confirm('These cool?', abort=True):
            os.system(f"{path}")
            save_to_watched(videos)
    else:
        click.echo("No videos selected")

## DEV COMMANDS
@click.command()
def update_channels():
    channels = get_all_channels()
    mod_channels = []
    for i in range(len(channels)): 
        channel = pop_from_list("channels", i)
        details = get_channel_details(channel)
        title = details["snippet"]["title"]
        channel_details = {
            "name": title,
            "channel_id": channel,
            "tag": "gen"
        }
        mod_channels.append(channel_details)
    for channel_id in mod_channels:
        save_channel(channel_id)

cli.add_command(save)
cli.add_command(gumbo)
cli.add_command(channels)

cli.add_command(latest)

if __name__ == "__main__":
    cli()