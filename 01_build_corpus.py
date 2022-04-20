import glob
import json
import rank_bm25
import stanza
import tqdm
import xml.etree.ElementTree as ET

STANZA_PIPELINE = stanza.Pipeline("en", processors="tokenize,lemma")
with open("nltk_stopwords.json", "r") as f:
  STOPWORDS = json.load(f)


PREFIX = "{http://www.tei-c.org/ns/1.0}"
TEXT_ID = f"{PREFIX}text"
BODY_ID = f"{PREFIX}body"
DIV_ID = f"{PREFIX}div"
HEAD_ID = f"{PREFIX}head"
P_ID = f"{PREFIX}p"


def get_docs(xml_dir, forum_id):
  section_titles = []
  section_texts = []
  filename = f'{xml_dir}/{forum_id}.tei.xml'
  divs = ET.parse(filename).getroot().findall(
    TEXT_ID)[0].findall(BODY_ID)[0].findall(DIV_ID)
  for div in divs:
    header_node, = div.findall(HEAD_ID)
    section_titles.append(header_node.text)
    text = ""
    for p in div.findall(P_ID):
      text += " ".join(p.itertext())
    section_texts.append(text)
  return section_titles, section_texts


def preprocess_text(text):
  doc = STANZA_PIPELINE(text)
  lemmatized = []
  for sentence in doc.sentences:
    for token in sentence.tokens:
      (token_dict,) = token.to_dict()
      maybe_lemma = token_dict["lemma"].lower()
      if maybe_lemma not in STOPWORDS:
        lemmatized.append(maybe_lemma)
  return lemmatized


def score_sections(forum_id, xml_dir, review_sentences):
  section_titles, section_texts = get_docs(xml_dir, forum_id)
  corpus = [preprocess_text(section) for section in section_texts]
  queries = [preprocess_text(sentence) for sentence in review_sentences]
  model = rank_bm25.BM25Okapi(corpus)
  for original_sentence, query in zip(review_sentences, queries):
    print(original_sentence)
    print(query)
    scores = model.get_scores(query)
    assert len(section_titles) == len(scores)
    print({k:v for k, v in zip(section_titles, scores)})
  print()
   

def main():
  for subset in "train dev test".split():
    print(subset)
    for filename in tqdm.tqdm(glob.glob(f"data/DISAPERE/final_dataset/{subset}/*.json")):
      with open(filename, 'r') as f:
        obj = json.load(f)
        forum_id = obj['metadata']['forum_id']
        review_sentences = [x["text"] for x in obj["review_sentences"]]
        score_sections(forum_id, "xmls/", review_sentences)


   


if __name__ == "__main__":
  main()

