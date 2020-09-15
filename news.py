import re, sys                                      # regular expressions
from datetime import datetime, timedelta            # to read timestamps reloadtimes

# Choices for assigning weight to the vector
NUM = 1
LOG_NUM = 2
SCALED_NUM = 3 # not implemented
W_CHOICE = NUM

class News:

    def __init__(self, heading, treatment_id, separator = '@|'):
        # chunks = re.split(separator, value)
        # self.time = datetime.strptime(chunks[0], "%Y-%m-%d %H:%M:%S.%f")
        self.heading = heading
        # self.title = chunks[2]
        # self.agency = chunks[3]
        # self.ago = chunks[4]
        #self.body = chunks[5]
        self.label = treatment_id

    def identical_news(self, news):
        return news.heading == self.heading

    def contains(self, nonces):
        for nonce in nonces:
            if (nonce in self.title.lower() or nonce in self.agency.lower()):
                return True
        return False

    def news_to_words(self):
        # returns a list of words from an news
        line = self.title+ " "# + self.body
        l = re.split(r'[.(), !<>\/:=?;\-\n]+|', line)
        for i in range(0,len(l)):
            l[i] = l[i].replace('\xe2\x80\x8e', '')
            l[i] = l[i].replace('\xc2\xae', '') 
            l[i] = l[i].replace('\xe2\x84\xa2', '') 
            l[i] = l[i].replace('\xc3\xa9', '') 
            l[i] = l[i].replace('\xc3\xa1', '') 
        l = [x for x in l if len(x)>1]
        return l

    # def fit_to_feat(self, word_v, wchoice):
        # # fits an news to a feature vector, returns a weight vector
        # vec = []
        # words = self.news_to_words()
        # stemmed_words = common.stem_low_wvec(words)
        # words = common.strip_vec(words)
        # # print words
        # for word in word_v:
            # if(wchoice == NUM):
                # vec.append(float(words.count(word)))
            # elif(wchoice == LOG_NUM):
                # vec.append(math.log(float(words.count(word))))
        # return vec

class NewsVector:
    def __init__(self):
        self.data = []
        self.label = -1

    def setLabel(self, lbl):
        self.label = lbl

    def index(self, news):
        return self.data.index(news)

    def size(self):
        return len(self.data)

    def add_vec(self, newsv):
        for news in newsv.data:
            self.add(news)

    def add(self, news):
        self.data.append(news)

    def remove(self, news):
        self.data.remove(news)

    def get_indices(self, keyword):
        # special purpose use
        indices = []
        for news in self.data:
            if(news.agency == keyword):
                indices.append(self.index(news))
        return indices

    def choose_by_index(self, index):
        return self.data[index]

    def countLabels(self, lbl):
        c1=0
        for news in self.data:
            if(news.label == lbl):
                c1 += 1
        return c1

    def freq_contains(self, nonces):
        count = 0
        for news in self.data:
            if(news.contains(nonces)):
                count +=1
        return count

    def unique(self):
        uniq = NewsVector()
        for news in self.data:
            present = False
            for un_news in uniq.data:
                if(news.identical_news(un_news)):
                    present = True
                    break
            if(not present):
                uniq.add(news)
        return uniq

    def union(self, newsv1):
        temp = NewsVector()
        for news in self.data:
            temp.add(news)
        for news in newsv1.data:
            temp.add(news)
        return temp.unique()

    def intersect(self, newsvp1):                   # without duplicates
        temp_int = NewsVector()
        newsv1 = NewsVector()
        newsv2 = NewsVector()
        newsv1.add_vec(self)                        # making copies 
        newsv2.add_vec(newsvp1)                     # making copies 
        for news1 in newsv1.data:
            present = False
            for news2 in newsv2.data:
                if(news1.identical_news(news2)):
                    present = True
                    break
            if(present):
                temp_int.add(news1)
                newsv1.remove(news1)
                newsv2.remove(news2)
        return temp_int.unique()

    def tot_intersect(self, newsvp1):
        # with duplicates
        newsv1 = NewsVector()
        newsv2 = NewsVector()
        newsv1.add_vec(self)
        newsv2.add_vec(newsvp1)
        for news1 in newsv1.data:
            present = False
            for news2 in newsv2.data:
                if(news1.identical_news(news2)):
                    present = True
                    break
            if(present):
                self.add(news1)
                newsv2.remove(news2)
        return self

    def news_weight(self, news, wchoice):
        count = 0
        for a in self.data:
            if(a.identical_news(news)):
                count = count+1
        if(wchoice == NUM):
            return count
        elif(wchoice == LOG_NUM):
            if(count == 0):
                return 0
            else:
                return math.log(count)
        else:
            print("Illegal W_CHOICE")
            raw_input("Press Enter to exit")
            sys.exit(0)

    # def gen_word_vec(self, word_v, wchoice=1):
        # # check generates a vector of words from NewsVector, fits it to word_v
        # vec = []
        # words = self.newsvec_to_words()
        # stemmed_words = common.stem_low_wvec(words)
        # words = common.strip_vec(words)
        # for word in word_v:
            # if(wchoice == NUM):
                # vec.append(float(words.count(word)))
            # elif(wchoice == LOG_NUM):
                # vec.append(math.log(float(words.count(word))))
        # return vec

    def gen_news_vec(self, newsv, choice=None):
        # check self is news_union  # generates a vector of newss from NewsVector
        vec = [0]*self.size()
        for news in self.data:
            for lnews in newsv.data:
                if(news.identical_news(lnews)):
                    vec[self.index(news)] += 1.
        return vec

    def gen_temp_news_vec(self, newsv, choice=None):
        # self is news_union
        vec = [0]*newsv.size()
        i = 0
        j = 0
        for news in newsv.data:
            for lnews in self.data:
                if(news.identical_news(lnews)):
                    vec[i] = self.index(lnews)
            i += 1
        return vec

    def newsvec_to_words(self):
        line = ""
        for news in self.data:
            line = line + " " + news.title+ " "# + news.body
        l = re.split(r'[.(), !<>\/:=?;\-\n]+|', line)
        for i in range(0,len(l)):
            l[i] = l[i].replace('\xe2\x80\x8e', '')
            l[i] = l[i].replace('\xc2\xae', '') 
            l[i] = l[i].replace('\xe2\x84\xa2', '') 
            l[i] = l[i].replace('\xc3\xa9', '') 
            l[i] = l[i].replace('\xc3\xa1', '') 
        l = [x for x in l if len(x)>1]
        return l

    def gen_news_words_vec(self, feat):
        # Creates a vector of word frequencies for each news in NewsVector
        vec = []
        for news in self.data:
            vec.append(news.fit_to_feat(feat))
        return vec

# if __name__ == "__main__":
