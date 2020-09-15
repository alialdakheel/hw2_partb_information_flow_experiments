import news
import numpy as np

def freq_news_vectors(news_vec_list):
    # returns a frequency vector of news, when input a list of newsVecs
    news_union = news.NewsVector()
    for newsv in news_vec_list:
        news_union = news_union.union(newsv)
    av_list = []
    labels = []
    for newsv in news_vec_list:
        av_list.append(news_union.gen_news_vec(newsv))
        labels.append(newsv.label)
    return av_list, labels, news_union

def get_feature_vectors(news_measurements, num_agents):
    # returns observation vector from a list of rounds
    # sys.stdout.write("Creating feature vectors")
    # sys.stdout.write("-->>")
    # sys.stdout.flush()
    news_vecs = [vec for block in news_measurements for vec in block]

    X, labels, feat = freq_news_vectors(news_vecs)

    y = [int(i) for i in labels]
    X = [X[i:i+num_agents] for i in range(0,len(X),num_agents)]
    y = [y[i:i+num_agents] for i in range(0,len(y),num_agents)]

    return np.array(X), np.array(y), feat
