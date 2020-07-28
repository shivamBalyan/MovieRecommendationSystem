"""SELECTING USERS WHO HAVE RATED ATLEAST 50 MOVIES"""
def selectGoodUsers(user_rating) :
    goodUsers=[]
    for i in range(1,len(user_rating)) :
        count=0
        for j in range(1,len(user_rating[0])) :
            if user_rating[i][j]!=0 :
                count+=1
            if count>=50 :
                goodUsers.append(user_rating[i][0])
                break
    return goodUsers

"""SELECTING INDICES OF MOVIES WHO HAVE BEEN RATED ATLEAST 50 TIMES """
def selectGoodMovies(user_rating) :
    goodMovies=[]
    for i in range(1,len(user_rating[0])) :
        count =0
        for j in range(1,len(user_rating)) :
            if user_rating[j][i]!=0 :
                count+=1
            if count>=50 :
                goodMovies.append(i)
                break
    return goodMovies

def trimmingData(user_rating,goodUsers,goodMovies) :
    new_user_rating=[]
    features=['userId']
    for i in goodMovies :
        features.append(i)
    new_user_rating.append(features)
    j=1
    for i in goodUsers :
        while(i!=user_rating[j][0]) :
            j+=1
        newRow=[i]
        for x in goodMovies :
            newRow.append(float(user_rating[j][x]))
        new_user_rating.append(newRow)
    return new_user_rating

"""
TESTING THE MODULE

def test() :
    file = open('PreProcessedData/user_ratings.txt', 'r')
    user_rating = []
    for row in file:
        user_rating.append(row.split())
    file.close()
    goodMovies=selectGoodMovies(user_rating)
    goodUsers=selectGoodUsers(user_rating)
    newData=trimmingData(user_rating,goodUsers,goodMovies)
    return newData

"""