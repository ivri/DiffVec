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

The final dataset consists of 12,458 triples {relation, word_1 , word_2), comprising 15 relation types, extracted from SemEval’12 (Jurgens et al., 2012), BLESS (Baroni and Lenci, 2011), the MSR analogy dataset (Mikolov et al., 2013c), the light verb dataset of Tan et al. (2006a), Princeton WordNet (Fellbaum, 1998), Wiktionary, and a web lexicon of collective nouns

## Scripts

### preprocess.py
Generates the files with vectors difference  
Usage: preprocess.py -s <semanticrels> -v <vectors> -o <outputfile>  
<semanticrels> -- input file with relations  
<vectors> -- input file with word embeddings (use ' '(space) as delimiter)  
<outputfile>  -- output file

### generate_NS.py
Generate negative samples (opposite and shuffled pairs)  
Usage: generate_NS.py -s <semanticrels>  
<semanticrels> -- input file with relations  
Outputs <semanticrels>.oppos.csv and <semanticrels>.shuff.csv files with opposite and shiffled pairs   
Run preprocess.py to get WEs for their differences  

### cluster.py
Run Spectral Clustering over the vectors  
  USAGE: -f <file_vectors> -c <clust_type:affin, knn> -n <number_of_clusters> -d <distance:euclid, cosine> -p <parameter: gamma, k(NN)> [-s <std>]  
  Example: python cluster.py -f  google.300d.vec -c affin -n 80 -d euclid -p 0.1  
  Outputs:  
	prints V-Measure and Homogeneity  
	for each DiffVec it's cluster in the format using ' : ' as delimiter  
  Automaically gererates the file name like fname.affin."$clust_number".euclid.0.1.1  

### run_cluster.sh
Scripts that runs cluster.py  
Need to specify settings and the file inside  

### VM_average.sh
Script for clustering evaluation.   
Takes average V-Measure for various runs depending on numbers of clusters  
Need to set your file name inside  
Better to put each run over several clusters in a separate EX\d(EX1, EX2, ..) folder  
