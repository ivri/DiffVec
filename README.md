# DiffVec

The dataset for evaluating of vector differences.

## Take and Took, Gaggle and Goose, Book and Read: Evaluating the Utility of Vector Differences for Lexical Relation Learning
Ekaterina Vylomova, Laura Rimell, Trevor Cohn, and Timothy Baldwin 

Recent work has shown that simple vector subtraction over word embeddings is surprisingly effective at capturing different lexical
relations, despite lacking explicit supervision.
Prior work has evaluated this intriguing result using a word analogy prediction formulation and hand-selected relations, but the generality
of the finding over a broader range of lexical relation types and different learning settings has not been evaluated. In this paper, we carry
out such an evaluation in two learning settings: (1) spectral clustering to induce word relations, and (2) supervised learning to classify
vector differences into relation types. We find that word embeddings capture a surprising amount of information, and that, under suitable supervised training, vector subtraction generalises well to a broad range of relations,
including over unseen lexical items.

There are asymmetric relations consisting of either verbs or nouns. 

The final dataset consists of 12,458 triples {relation, word_1 , word_2), comprising 15 relation types, extracted from SemEval’12 (Jurgens et al., 2012), BLESS (Baroni and Lenci, 2011), the MSR analogy dataset (Mikolov et al., 2013c), the light verb dataset of Tan et al. (2006a), Princeton WordNet (Fellbaum, 1998), Wiktionary, 5 and a web lexicon of collective nouns
