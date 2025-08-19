import os
import shlex
from invoke import task

@task
def get_playlist(c, playlist_id="https://open.spotify.com/playlist/5ABMzUESx7K7EyowE5kFCl?si=8849debdda414011", config_path="./freyr-config/conf.json"):
    c.run(f"yarn freyr get {playlist_id} --config {config_path}")

@task
def remux_m4a(c, src, fixed):
    src_quoted = shlex.quote(src)
    fixed_quoted = shlex.quote(fixed)
    c.run(f"ffmpeg -err_detect ignore_err -i {src_quoted} -c copy {fixed_quoted}", warn=True)

@task
def m4a_to_mp3(c, src, dest=None):
    if not dest:
        dest = os.path.splitext(src)[0] + ".mp3"
    if os.path.exists(dest):
        print(f"Skipping conversion, mp3 already exists: {dest}")
        return
    src_quoted = shlex.quote(src)
    dest_quoted = shlex.quote(dest)
    result = c.run(f"ffmpeg -i {src_quoted} -codec:a libmp3lame -qscale:a 2 {dest_quoted}", warn=True)
    if result.exited != 0:
        print(f"Conversion failed for {src}")

@task
def convert_all_m4a(c, directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".m4a"):
                src_path = os.path.join(root, file)
                src_quoted = shlex.quote(src_path)
                check = c.run(f"ffmpeg -v error -i {src_quoted} -f null -", hide=True, warn=True)
                if check.exited == 0:
                    m4a_to_mp3(c, src_path)
                else:
                    print(f"File {src_path} flagged as corrupted, trying remux and convert...")
                    fixed_path = src_path + ".fixed.m4a"
                    remux_m4a(c, src_path, fixed_path)
                    m4a_to_mp3(c, fixed_path)
    print("Conversion attempts complete.")


@task
def copy_all_mp3(c, dest_dir="/media/mc18g13/SWIM PRO/"):
    dest_quoted = shlex.quote(dest_dir)
    for root, _, files in os.walk("."):
        for file in files:
            if file.lower().endswith(".mp3"):
                src_path = os.path.join(root, file)
                src_quoted = shlex.quote(src_path)
                c.run(f"cp {src_quoted} {dest_quoted}")
