import click
import os
import random
from db.db import get_all_channel_ids, save_channel_id, save_test
from youtube.youtube import get_videos

@click.group()
def cli():
    pass

@click.command()
@click.argument('id')
def save(id):
    save_channel_id(id)

@click.command()
def test():
    save_test("id")

@click.command()
def gumbo():

    channels = get_all_channel_ids()
    gumbo = random.sample(channels, 5 if len(channels) >5 else len(channels) )
    path = '/Applications/IINA.app/Contents/MacOS/iina-cli'
    videos = []
    for c_id in gumbo:
        videos = videos + get_videos(c_id)
    for vid in videos:
        click.echo(vid["title"])
        path = f'{path} "https://www.youtube.com/watch?v={vid["videoId"]}"'
    if click.confirm('These cool?', abort=True):
        os.system(f"{path}")

cli.add_command(save)
cli.add_command(gumbo)
cli.add_command(test)

if __name__ == "__main__":
    cli()