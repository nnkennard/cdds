import glob
import json
import openreview
import tqdm

INVITATION_MAP = {
"ICLR2019":"ICLR.cc/2019/Conference/-/Blind_Submission",
"ICLR2020":"ICLR.cc/2020/Conference/-/Blind_Submission",
}

def write_pdf_to_file(guest_client, forum_id, forum_dir, note):
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
    with open(f'{forum_dir}/{forum_id}.pdf', 'wb') as file_handle:
        file_handle.write(pdf_binary)

def main():

  guest_client = openreview.Client(baseurl='https://api.openreview.net')

  done_forums = []
  for subset in "train dev test".split():
    print(subset)
    for filename in tqdm.tqdm(glob.glob(f"data/DISAPERE/final_dataset/{subset}/*.json")):
      with open(filename, 'r') as f:
        forum_id = json.load(f)['metadata']['forum_id']
        if forum_id not in done_forums:
          k = guest_client.get_references(
              referent=forum_id, original=True)  
          write_pdf_to_file(guest_client, forum_id, "pdfs/", k[-1])
          done_forums.append(forum_id)



if __name__ == "__main__":
  main()

