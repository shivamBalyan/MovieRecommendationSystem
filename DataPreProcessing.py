import csv

def binarySearch(a,x,lo=0,hi=None) :
    if hi is None:
        hi=len(a)-1
    while lo<=hi:
        mid=(lo+hi)//2
        if a[mid]>x:
            hi=mid-1
        elif a[mid]<x:
            lo=mid+1
        else :
            return mid
    return -1

def createSearchMovieMatrix() :
    movies = open('InputData/movies.csv', 'r')
    # creating a search matrix that has all genres listed for a movie
    # List of all genres for index referencing with help of dictionary
    list_genre = ["Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                  "Film-Noir", "Horror", "IMAX", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War",
                  "Western"]
    index_genre = {}
    for i in range(len(list_genre)):
        index_genre[list_genre[i]] = i
    csv_reader = csv.reader(movies, delimiter=',')
    line_count = 0
    search_movies = []
    for row in csv_reader:
        if line_count == 0:
            search_movies.append([row[0], row[1], list_genre])
        else:
            genreList = [0] * len(list_genre)
            genres = row[2].split('|')
            if (genres[0] != '(no genres listed)'):
                for i in genres:
                    genreList[index_genre[i]] = 1
            search_movies.append([row[0], row[1], genreList])
        line_count += 1
    movies.close()
    return search_movies

def createRankingMatrix(search_movies) :
    # creating a ranking list for each user's all ratings as column and user Id as row
    ratings = open('InputData/ratings.csv','r')
    csv_reader = csv.reader(ratings, delimiter=',')
    user_rating = []
    movieIds = []
    for i in range(1, len(search_movies)):
        movieIds.append(search_movies[i][0])
    user_rating.append(['userId'])
    user_rating[0].extend(movieIds)
    #CONVERTING MOVIE ID INTO INT SO THAT SEARCHING COULD BE DONE
    for i in range(len(movieIds)) :
        movieIds[i]=int(movieIds[i])
    line_count = 0
    currUserId=-1
    for row in csv_reader:
        if line_count != 0:
            #-1 means not rated
            if currUserId!=row[0] :
                # 0 means not rated
                x=0
                user_rating.append([row[0]])
                user_rating[-1].extend([0]*len(movieIds))
                currUserId=row[0]
            x=binarySearch(movieIds,int(row[1]),lo=x)
            user_rating[-1][x+1]=float(row[2])
        line_count += 1
    return user_rating



