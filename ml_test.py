from news import News, NewsVector
import helpers
import ml
import permutation_test
from statistics import correctly_classified

def test_news_classifier():
    n1 = News("asdf", 0)
    n2 = News("asdf_23", 0)
    n3 = News("asdf_", 1)
    n4 = News("asdf_23", 1)

    nv1 = NewsVector()
    nv1.add(n1)
    nv1.add(n2)
    nv1.label = n1.label
    nv2 = NewsVector()
    nv2.add(n3)
    nv2.add(n4)
    nv2.label = n3.label

    news_vecs = [[nv1, nv1] ,[nv2, nv2]] * 6 
    num_agents = 2

    X, y, union = helpers.get_feature_vectors(news_vecs, num_agents)
    classifier, y_pred, y_true = ml.train_and_test(X, y, verbose=True)

def test_news_perm():
    n1 = News("asdf", 0)
    n2 = News("asdf_23", 0)
    n3 = News("asdf_", 1)
    n4 = News("asdf_23", 1)

    nv1 = NewsVector()
    nv1.add(n1)
    nv1.add(n2)
    nv1.label = n1.label
    nv2 = NewsVector()
    nv2.add(n3)
    nv2.add(n4)
    nv2.label = n3.label

    news_vecs = [[nv1, nv1] ,[nv2, nv2]] * 6 
    num_agents = 2

    X, y, union = helpers.get_feature_vectors(news_vecs, num_agents)
    classifier, y_pred, y_true = ml.train_and_test(X, y, verbose=True)

    test_stat = correctly_classified
    p_value = permutation_test.blocked_sampled_test(
            y_pred,
            y_true,
            test_stat
            )
    return p_value



if __name__ == "__main__":
    # test_news_classifier()
    p_value = test_news_perm()
