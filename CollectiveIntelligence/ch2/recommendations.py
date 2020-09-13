


critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,'The Night Listener': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


import pandas as pd
from math import sqrt

def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    # 无相同
    if len(si)==0:
        return 0
    sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])
    return 1/(1+sqrt(sum_of_squares))


def sim_pearson(prefs, p1, p2):
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1
    n =len(si)
    if n==0:
        return 0
    # 评分总和
    sum1 = sum([prefs[p1][item] for item in si])
    sum2 = sum([prefs[p2][item] for item in si])
    # 评分平方和
    sum1Sq = sum([pow(prefs[p1][item], 2) for item in si])
    sum2Sq = sum([pow(prefs[p2][item], 2) for item in si])
    # 乘积之和
    pSum = sum(prefs[p1][item]*prefs[p2][item] for item in si)
    # 皮尔逊评价值
    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1Sq - pow(sum1, 2)/n)*(sum2Sq - pow(sum2, 2)/n))
    if den == 0:
        return 0
    return num/den


def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other!=person] 
    scores.sort()
    scores.reverse()
    return scores[:n]


def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        if other==person:
            continue
        sim = similarity(prefs, person, other)
        # print('sim:', sim)
        if sim<=0:
            continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item]==0:
                totals.setdefault(item, 0)
                totals[item]+=prefs[other][item]*sim
                simSums.setdefault(item, 0)
                simSums[item]+=sim
    rankings = [(total/simSums[item],item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            result[item][person] = prefs[person][item]
    return result


def calculateSimilarItems(prefs, n=10):
    result={}
    itemPrefs = transformPrefs(prefs)
    c=0
    for item in itemPrefs:
        # print('------{}-------'.format(item))
        c+=1
        if c%100==0:
            print("%d/%d"%(c,len(itemPrefs)))
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item]=scores
    return result


def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}

    for (item, rating) in userRatings.items():
        for (similarity, item2) in itemMatch[item]:
            # 看过就跳过
            if item2 in userRatings:
                continue
            scores.setdefault(item2, 0)
            scores[item2]=similarity*rating
            totalSim.setdefault(item2, 0)
            totalSim[item2]+=similarity*rating
    rankings = [(score/totalSim[item], item) for item, score in scores.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


def loadMovieLens(path='./ml-latest-samll'):
    movies = {}
    data1 = pd.read_csv('D:\ReadingLog\Collective intelligence programming\ch2\ml-latest-small\movies.csv')
    # print(data1.info())
    for i in range(0, len(data1)):
        id = int(data1.iloc[i]['movieId'])
        title = data1.iloc[i]['title']
        movies[id]=title
    prefs = {}
    data2 = pd.read_csv('D:\ReadingLog\Collective intelligence programming\ch2\ml-latest-small\\ratings.csv')
    # print(data2.info())  
    for i in range(0, len(data2)):
        user = data2.iloc[i]['userId']
        rating = data2.iloc[i]['rating']
        movieId = int(data2.iloc[i]['movieId'])
        prefs.setdefault(user, {})
        # print('user:',user)
        # print('movieId:', movieId)
        # print('rating:', rating)
        prefs[user][movies[movieId]]=float(rating)
    return prefs 


if __name__ == '__main__':
    # print(critics['Lisa Rose'])
    # print(critics['Gene Seymour'])
    # dis1 = sim_distance(critics, 'Lisa Rose','Gene Seymour')
    # print(dis1)
    # dis2 = sim_pearson(critics, 'Lisa Rose','Gene Seymour')
    # print(dis2)
    # res = topMatches(critics, 'Toby', n=3)
    # print(res)
    # res = getRecommendations(critics, 'Toby')
    # print(res)
    # movies = transformPrefs(critics)
    # res = topMatches(movies, 'Superman Returns')
    # print(res)
    # print(calculateSimilarItems(critics, n=10))
    # 计算电影相似度
    # res = calculateSimilarItems(critics)
    # print(res)
    # print(getRecommendedItems(critics, res, 'Toby'))
    prefs = loadMovieLens()
    # res = getRecommendations(prefs, '87')[0:30]
    # print(res)
    itemsim = calculateSimilarItems(prefs, n=50)
    res = getRecommendedItems(prefs, itemsim, '87')[0:30]
    print(res) 
