import json

from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    Doc
)

analyze_done = False

def toponyme_search(text):
	segmenter = Segmenter()
	emb = NewsEmbedding()
	ner_tagger = NewsNERTagger(emb)
	morph_tagger = NewsMorphTagger(emb)
	syntax_parser = NewsSyntaxParser(emb)
	morph_vocab = MorphVocab()
	doc = Doc(text)
	doc.segment(segmenter)
	doc.tag_morph(morph_tagger)
	doc.parse_syntax(syntax_parser)
	doc.tag_ner(ner_tagger)
	for span in doc.spans:
		span.normalize(morph_vocab)
	my_dict = {_.text: _.normal for _ in doc.spans if _.type == "LOC"}
	return list(my_dict.values())

if __name__ == "__main__":
    dfdata = []
    with open("data_file.json", "r") as read_file:
        dfdata = json.load(read_file)
    if dfdata is not None:
        while not analyze_done:
            try:
                print("Waining for toponyme analyse")
                for post in dfdata:
                    post["toponymes"] = toponyme_search(post["text"])
                analyze_done = True
            except Exception:
                print("Something went wrong!")
        print("Analysed")
    else:
        print("Something went wrong!")
    with open("data_file.json", "w") as write_file:
        json.dump(dfdata, write_file)