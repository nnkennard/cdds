import argparse
import collections
import json
import openreview
import os
import time
import tqdm

import data_lib

from datetime import datetime

parser = argparse.ArgumentParser(
    description="Get all revisions from an conference.")
parser.add_argument("-i", "--idx", type=int, help="Invitation index")
parser.add_argument("-p", "--path", type=str, help="Path to data directory")
parser.add_argument(
    "-d",
    "--debug",
    action="store_true",
    help="truncate to small subset of data for debugging",
)


def get_discussion(client, forum_id, path):
  forum_notes = client.get_notes(forum=forum_id)
  with open(f"{path}/discussion.jsonl", "w") as f:
    for note in forum_notes:
      f.write(json.dumps(note.to_json()))


def get_pdf_filename(forum_dir, timestamp, is_reference):
  """Produce a filename for the pdf with a human readable timestamp.

    Args:
        forum_dir: Directory to write pdfs to
        timestamp: Unix timestamp from note.tcdate in OR Note object
        is_reference: follows is_reference value of OR API.

    Returns:
        pdf filename with timestamps in forum_dir
    """
  nice_timestamp = datetime.fromtimestamp(timestamp / 1000).strftime(
      "%Y-%m-%dT%H_%M_%S")  # Something human-readable for the file name
  if is_reference:
    main_or_revision = "revision"
  else:
    main_or_revision = "main"
  return forum_dir + "/{0}_{1}.pdf".format(main_or_revision, nice_timestamp)


def write_pdf_to_file(guest_client, forum_dir, note):
  """Get pdf of manuscript and write to an appropriately named file.
    Args:
        guest_client: OR API client
        forum_dir: Directory to write pdfs to
        note: OR API Note object
    Returns:
        None
    """
  is_reference = not (note.id == note.forum)
  pdf_binary = guest_client.get_pdf(note.id, is_reference=is_reference)
  with open(get_pdf_filename(forum_dir, note.tcdate, is_reference),
            "wb") as file_handle:
    file_handle.write(pdf_binary)


def get_revisions(client, forum_id, path):
  (forum_note,) = [
      note for note in client.get_notes(forum=forum_id) if note.id == forum_id
  ]
  write_pdf_to_file(client, path, forum_note)
  for revision in tqdm.tqdm(
      client.get_references(referent=forum_id, original=True),
      desc="Getting revisions for {0}".format(forum_id),
  ):
    try:
      write_pdf_to_file(client, path, revision)
    except openreview.OpenReviewException:
      continue


def main():

  args = parser.parse_args()
  conference_name, invitation, _ = data_lib.venues[args.idx]

  guest_client = openreview.Client(baseurl="https://api.openreview.net")

  for i, forum in enumerate(
      openreview.tools.iterget_notes(guest_client, invitation=invitation)):
    path = f"{args.path}/{conference_name}/{forum.id}/"
    os.makedirs(path, exist_ok=True)
    get_discussion(guest_client, forum.id, path)
    get_revisions(guest_client, forum.id, path)
    time.sleep(5)

    if args.debug and i == 9:
      break


if __name__ == "__main__":
  main()
