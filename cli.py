import click
import os
import random
import questionary
from db.db import get_all_channels, save_channel, have_watched, save_to_watched, pop_from_list
from youtube.youtube import get_videos, get_channel_details, search_youtube

@click.group()
def cli():
    pass

@click.command()
@click.argument('query', nargs=-1)
def search(query):
    results = search_youtube(query)
    selected = questionary.select("Watch search result", [f"{video['snippet']['title']}\n  {video['snippet']['channelTitle']}" for video in results]).ask()
    title = selected.split('\n')[0]
    to_watch = [{"title": video["snippet"]["title"], "videoId": video["id"]["videoId"]} for video in results if video["snippet"]["title"] == title]
    watch(to_watch)
    click.echo(to_watch)

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
@click.option('--vids', default=1, help="Number of videos to display")
def channels(vids):
    channels = get_all_channels()
    channel_choices = questionary.checkbox("Select channels to watch", [channel["name"] for channel in channels]).ask()
    selected_channels = [channel for channel in channels if channel["name"] in channel_choices]
    videos = []
    videos = get_videos([channel["channel_id"] for channel in selected_channels], vids)
    videos = [video for video in videos if not have_watched(video)]
    watch(videos)


@click.command()
@click.option('--count', default=5, help="Number of videos to watch")
@click.option('--vids', default=1, help="Number of videos to display")
def patch(count, vids):

    channels = get_all_channels()
    gumbo = random.sample(channels, count if count <= len(channels) else len(channels)  )
    
    videos = []
    videos = get_videos([channel["channel_id"] for channel in gumbo], vids)
    videos = [video for video in videos if not have_watched(video)]
    if len(videos) > 0:
        vid_choices = questionary.checkbox("Select Videos", [video["title"] for video in videos]).ask()
        to_watch = [video for video in videos if video["title"] in vid_choices]
        watch(to_watch)
    else:
        click.echo("All Videos watched")

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
def test():
    channels = get_all_channels()
    click.echo(channels)


cli.add_command(save)
cli.add_command(patch)
cli.add_command(channels)
cli.add_command(test)
cli.add_command(search)

if __name__ == "__main__":
    cli()