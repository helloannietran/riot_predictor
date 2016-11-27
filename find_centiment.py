from parse_file import get_all_files_in_dir
from os.path import join
import re
negative_words = []
positive_words = []

def count_words(text, ref_words):
    all_words = text.split()
    regex = re.compile('[^a-zA-Z]')
    all_words = [regex.sub('',  w).strip() for w in all_words if len(w)<20]
    
    count = 0
    for word in all_words:
        # print word
        if word.strip().lower() in ref_words:
            # print word
            count += 1
    total_count = len(all_words)
    return count, total_count



with open("negative_words.txt") as negative_file:
    for l in negative_file:
        negative_words.append(l.strip())

with open("positive_words.txt") as positive_file:
    for l in positive_file:
        positive_words.append(l.strip())

# PATH = "centiment_files"
PATH = "Data"
# Data/structured_riots_data/
unstructured_data = "riots_bing_html"
structured_data = "structured_riots_data"

unstructured_dir = join(PATH, unstructured_data)
structured_dir = join(PATH, structured_data)
with open("structured_centiment_1905-58.csv", 'w') as out_file:
    # out_file.write("centiment_percents\n")
    for i in xrange(2086, 2113):
        try:
            print "checking riot %d" % i
            data_dir = join(structured_dir, "riot%04d" %i)
            files = get_all_files_in_dir(data_dir)
            negs = 0
            poses = 0
            total = 0
            for file_name in files:
                with open(join(data_dir, file_name)) as file:
                    text = file.read()
                    # print 'test: ', text

                    negative_count, total_count = count_words(text, negative_words)
                    positive_count, total_count = count_words(text, positive_words)
                    negs += negative_count
                    poses += positive_count
                    total += total_count
            # print 'negative: %d, positive: %d, total: %d' %(negs, poses, total)
            out_val = (poses - negs)*100.0/total if total > 0 else 'None'
            out_file.write("%s\n" % str(out_val))
        except:
            out_file.write("-None\n")
            continue