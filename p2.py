from nltk.tag import pos_tag

sentence = "Akshita works at CG . She is a hardworking girl."
tagged_sent = pos_tag(sentence.split())
# [('Michael', 'NNP'), ('Jackson', 'NNP'), ('likes', 'VBZ'), ('to', 'TO'), ('eat', 'VB'), ('at', 'IN'), ('McDonalds', 'NNP')]

propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
print(propernouns)
# ['Michael','Jackson', 'McDonalds']