import collections
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


Result = collections.namedtuple("Result",
  "review_id index review_sentence scores")

Review = collections.namedtuple("Review",
  "forum_id review_id review_sentences section_titles permalink")

def top_sections(score_pairs):
  return [x[0] for x in sorted(score_pairs, key=lambda y:y[1],
  reverse=True)[:3]]


def score_sections(metadata, xml_dir, review_sentences):

  review_id, forum_id, permalink = [metadata[key]
      for key in "review_id forum_id permalink".split()]
  section_titles, section_texts = get_docs(xml_dir, forum_id)
  corpus = [preprocess_text(section) for section in section_texts]
  queries = [preprocess_text(sentence) for sentence in review_sentences]
  model = rank_bm25.BM25Okapi(corpus)
  results = []
  for i, (original_sentence, query) in enumerate(zip(review_sentences,
  queries)):
    results.append(Result(
    review_id, i, original_sentence, model.get_scores(query).tolist()))
  return Review(forum_id, review_id, results, section_titles, permalink)

def recursive_json_dumps(review):
  temp = review._asdict()
  temp['review_sentences'] = [x._asdict() for x in temp['review_sentences']]
  return json.dumps(temp)

def write_scores(data_dir, metadata, xml_dir, review_sentences):
  with open(f'{data_dir}/{metadata["review_id"]}.json', 'w') as f:
    f.write(recursive_json_dumps(
      score_sections(metadata, xml_dir, review_sentences)))

def main():
  for filename in tqdm.tqdm(glob.glob(f"data/DISAPERE/final_dataset/train/*.json")):
    with open(filename, 'r') as f:
      obj = json.load(f)
      review_sentences = [x["text"] for x in obj["review_sentences"]]
      try:
        write_scores('data/score_jsons/', obj['metadata'], 'data/xmls/', review_sentences)
      except ValueError:
        print(f"Error with XML parsing (probably) of review {obj['metadata']['review_id']}")
      except FileNotFoundError:
        print(f"File not found error with review {obj['metadata']['review_id']}")


if __name__ == "__main__":
  main()

