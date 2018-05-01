python2 src/main.py --method deepWalk --input ../hierarchy.edgelist --graph-format edgelist --epochs 500 --output deepwalk_vec.txt --clf-ratio 1
python2 src/main.py --method line --input ../hierarchy.edgelist --graph-format edgelist --epochs 500 --output LINE_vec.txt --clf-ratio 1
python2 src/main.py --method node2vec --input ../hierarchy.edgelist --graph-format edgelist --epochs 500 --output node2vec_vec.txt --clf-ratio 1
