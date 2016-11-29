import re
negative_words = []
positive_words = []
def violence_rating(tweets):
    global negative_words, positive_words
    negs=0
    poses=0
    total=0
    with open("negative_words.txt") as negative_file:
        for l in negative_file:
            negative_words.append(l.strip())

    with open("positive_words.txt") as positive_file:
        for l in positive_file:
            positive_words.append(l.strip())

    negative_count, total_count = count_words(tweets, negative_words)
    positive_count, total_count = count_words(tweets, positive_words)
    negs += negative_count
    poses += positive_count
    total += total_count
    out_val = (poses - negs)*100.0/total if total > 0 else 'None'
    return out_val
    # return str(calculate_riot_prob(out_val))

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
