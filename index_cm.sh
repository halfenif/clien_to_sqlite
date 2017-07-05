if [ "$1" == "" ]; then
  echo "Plaease Enter Start Page No..."
else
 nohup python3 batch_collect_article_index.py -p 7998 -t cm -s $1 > nohup.out.7998 &
fi
