for i in {1..20}; do distortions.py -o "alt_cover_$i.jpg" -s $(awk "BEGIN {print 0.3 + (rand() * 1.2)}"); done
