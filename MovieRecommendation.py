"""THIS MOVIE RECOMMENDATION SYSTEM WORKS ON ITEM BASED COLLABORATIVE FILTERING.
A MOVIE IS RECOMMENDED ON THE BASIS OF SIMILARITY OF USER RATINGS OF THE GIVEN MOVIE
WITH OTHER MOVIES. """
import math
import DataPreProcessing
import DataSelection
import DataBinarization
from collections import Counter
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def createMovieName(search_movies):
    # CREATING A DICTIONARY WHICH HAS KEY AS MOVIE ID AND VALUE AS MOVIE NAME
    movie_name = {}
    for i in range(1,len(search_movies)) :
        movie_name[search_movies[i][0].strip()]=search_movies[i][1]
    return movie_name

def findMatch(names,theName) :
    """

    :param names: list of names
    :param theName: the name you find the most similar name in names
    :return: the most similar name in names
    """
    #FINDING THE MOST SIMILAR MOVIE NAME TO movieName
    highest=process.extractOne(theName,names)
    if highest[1]>50 :
        return highest[0]
    else :
        return None

def getMovieId(movie_name,movieName) :
    """

    :param movie_name: dictionary of movieIDs and their names
    :param movieName: the name of the movie
    :return: the movie id

    """
    for i in movie_name:
        if movieName==movie_name[i] :
            return i

def createPropertyMatrixForMovie(movId,goodUsers,user_rating) :
    movieMat=[]
    for i in range(1,len(user_rating[0])) :
        if movId==user_rating[0][i] :
            j=1
            for x in goodUsers :
                while user_rating[j][0]!=x :
                    j+=1
                if float(user_rating[j][i])>=3.0 :
                    movieMat.append(1)
                else :
                    movieMat.append(0)
    return movieMat

def cosineDistance(a,b):
    """

    :param a: list containing properties of a
    :param b: list containing properties of b
    NOTE :properties of a and b must be in same order
    :return: SIMILARITY BASED ON PROPERTIES of a and b
        if similarity cant be found returns -1

    """
    if len(a)!=len(b) :
        print("Similarity cant be found")
        return -1
    else :
        d=0
        for i in range(len(a)) :
            d+=a[i]*b[i]
        modA=0
        for i in range(len(a)) :
            modA+=a[i]**2
        modA=math.sqrt(modA)
        modB = 0
        for i in range(len(b)):
            modB +=b[i]**2
        modB = math.sqrt(modB)
        if modA!=0 and modB!=0 :
            d/=modA*modB
        return d

def createSimilarityDict(movieMat,user_rating) :
    """
    THIS FUNCTION CREATED A DICTIONARY WHERE KEY IS MOVIE ID AND
     VALUE IS SIMILARITY BETWEEN INPUT MOVIE AND KEY
     """
    similarityDict={}
    for i in range(1,len(user_rating[0])) :
        b=[]
        for j in range(1,len(user_rating)) :
            b.append(user_rating[j][i])
        similarityDict[user_rating[0][i]]=cosineDistance(movieMat,b)
    return similarityDict

def main():
    movieName=input("ENTER MOVIE NAME : ")

    search_movies=DataPreProcessing.createSearchMovieMatrix()
    user_rating=DataPreProcessing.createRankingMatrix(search_movies)

    movies=createMovieName(search_movies)

    similarMovieName=findMatch(movies.values(),movieName)
    if similarMovieName == None :
        print("No such movie exist in database")
        return None
    print("Showing recommended movies based on",similarMovieName," :")

    movID=getMovieId(movies,similarMovieName)

    goodUsers=DataSelection.selectGoodUsers(user_rating)
    goodMovies=DataSelection.selectGoodMovies(user_rating)

    final_user_rating=DataBinarization.binarizeUserRating(DataSelection.trimmingData(user_rating,goodUsers,goodMovies))

    movieMat=createPropertyMatrixForMovie(movID,goodUsers,user_rating)
    similarityDict=createSimilarityDict(movieMat,final_user_rating)

    #The most similar movie will be the movie itself
    recommendedMovies=dict(Counter(similarityDict).most_common(11))

    count=0
    for i in recommendedMovies :
        if str(i) in movies and count!=0:
            print('\t',movies[str(i)])
        count+=1
    return None

main()