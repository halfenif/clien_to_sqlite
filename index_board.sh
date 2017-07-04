if [ "$1" == "" ]; then
  echo "Plaease Enter Start Page No..."
else
 nohup python3 batch_collect_article_index.py -p 7999 -t board -s $1 > nohup.out.7999 &
fi
