def binarizeUserRating(user_rating) :
    for i in range(1,len(user_rating)) :
        for j in range(1,len(user_rating[0])) :
            if user_rating[i][j]>=3.0:
                user_rating[i][j]=1
            else :
                user_rating[i][j]=0
    return user_rating
