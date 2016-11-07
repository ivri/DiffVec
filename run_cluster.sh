## Run clustering for various clusters
## google.300d.vec -- file with embeddings

python cluster.py -f  google.300d.vec -c affin -n 80 -d euclid -p 0.1 &
python cluster.py -f  google.300d.vec -c affin -n 70 -d euclid -p 0.1 &

python cluster.py -f  google.300d.vec -c affin -n 60 -d euclid -p 0.1 &

python cluster.py -f  google.300d.vec -c affin -n 50 -d euclid -p 0.1 &

python cluster.py -f  google.300d.vec -c affin -n 40 -d euclid -p 0.1 &

python cluster.py -f  google.300d.vec -c affin -n 30 -d euclid -p 0.1 &

python cluster.py -f  google.300d.vec -c affin -n 20 -d euclid -p 0.1 &

python cluster.py -f  google.300d.vec -c affin -n 10 -d euclid -p 0.1 

