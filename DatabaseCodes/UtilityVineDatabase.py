'''
Created on Feb 5, 2015

@author: RahatIbnRafiq
'''

'''
Created on Feb 5, 2015

@author: RahatIbnRafiq
'''
import mongoOperations
import warnings
warnings.filterwarnings("ignore")


def addFieldToPostCollection(postId,mentionCount,negativePercentage,negativeCount,positivePercentage,positiveCount):
    databaseName = "VineDatabase"
    collectionName = "CollectedUserPosts"
    mongoOperations.addFieldToPoctCollection(databaseName, collectionName, postId, mentionCount, negativePercentage, negativeCount
                                             ,positivePercentage,positiveCount)



def getDistinctUserFromPostsCollection():
    databaseName = "VineDatabase"
    collectionName = "CollectedUserPosts"
    documents = mongoOperations.getDistinctUserFromPostCollection(databaseName, collectionName)
    useridList = []
    for document in documents:
        useridList.append(str(document))
        
    return useridList

def getUserIdsFromBioCollection():
    databaseName = "VineDatabase"
    collectionName = "CollectedUserBio"
    documents = mongoOperations.findAllDataFromCollection(databaseName, collectionName)
    useridList = []
    for document in documents:
        useridList.append(str(document['userId']))
        
    return useridList

def getPostIdsFromPostCollection():
    databaseName = "VineDatabase"
    collectionName = "CollectedUserPosts"
    documents = mongoOperations.findAllDataFromCollection(databaseName, collectionName)
    postidList = []
    for document in documents:
        postidList.append(str(document['postId']))
        
    return postidList

def getCommentsForPost(postId):
    databaseName = "VineDatabase"
    collectionName = "CollectedUserComments"
    documents = mongoOperations.findAllCommentsFromCollection(databaseName, collectionName,postId)
    commentList = []
    for document in documents:
        commentList.append(document)
        
    return commentList

def getInstagramBio():
    databaseName = "VineDatabase"
    collectionName = "CollectedUserBio"
    documents = mongoOperations.findAllDataFromCollection(databaseName, collectionName)
    f = open("NathanInstagramFile.txt","w")
    count = 0
    for document in documents:
        if "instagram" in str(document["description"]).lower():
            vineUsername = "Vine username:"+str(document["username"])
            vineUserID = "Vine UserID:"+str(document["userId"])
            vineDescription = "Description:"+str(document["description"])
            f.write(vineUsername+"\n")
            f.write(vineUserID+"\n")
            f.write(vineDescription+"\n")
            count = count + 1
            print str(count)+" users done"
    f.close()

def writeAllPostIdsToFile():
    databaseName = "VineDatabase"
    collectionName = "CollectedUserPosts"
    documents = mongoOperations.findAllDataFromCollection(databaseName, collectionName)
    count = 0
    fileCount = 1
    totalCount = 0
    g = open("vinePostIdFileNumber"+str(fileCount)+".txt","a")
    for document in documents:
        g.write(str(document['postId'])+"\n")
        count = count + 1
        totalCount = totalCount + 1
        print "total:"+str(totalCount)
        if count == 100000:
            count = 0
            g.close()
            fileCount = fileCount + 1
            g = open("vinePostIdFileNumber"+str(fileCount)+".txt","a")
            print "newfile!yay!!!!!!!!!!!!!!!!!!!!!!!"
            
    g.close()
    

def explicitUserAverageStats():
    databaseName = "VineDatabase"
    collectionName = "CollectedUserBio"
    documents = mongoOperations.findAllDataFromCollection(databaseName, collectionName)
    verifiedcount = 0
    nonVerifiedcount = 0
    
    verifiedFollowerCount = 0
    nonVerifiedFollowerCount = 0
    
    verifiedFollowingCount = 0
    nonVerifiedFollowingCount = 0
    
    verifiedLoopCount = 0
    nonVerifiedLoopCount = 0
    
    verifiedPostCount = 0
    nonVerifiedPostCount = 0
    
    verifiedAuthorCount = 0
    nonVerifiedAuthorCount = 0
    
    verifiedLocationCount = 0
    nonVerifiedLocationCount = 0
    
    verifiedTwitterCount = 0
    nonVerifiedTwitterCount = 0
    
    verifiedInstagramCount = 0
    nonVerifiedInstagramCount = 0
    
    verifiedYoutubeCount = 0
    nonVerifiedYoutubeCount = 0
    
    
    for document in documents:
        if str(document["explicitContent"]) == "1":
            verifiedcount = verifiedcount + 1
            verifiedAuthorCount = verifiedAuthorCount + int(str(document["authoredPostCount"]))
            verifiedPostCount = verifiedPostCount + int(str(document["postCount"]))
            verifiedLoopCount = verifiedLoopCount + int(str(document["loopCount"]))
            verifiedFollowingCount = verifiedFollowingCount + int(str(document["followingCount"]))
            verifiedFollowerCount = verifiedFollowerCount + int(str(document["followerCount"]))
            if len(str(document["location"])) > 0:
                verifiedLocationCount = verifiedLocationCount + 1
            if "twitter" in str(document["description"]).lower():
                verifiedTwitterCount = verifiedTwitterCount + 1
            
            if "instagram" in str(document["description"]).lower():
                verifiedInstagramCount = verifiedInstagramCount + 1
            
            if "youtube" in str(document["description"]).lower():
                verifiedYoutubeCount = verifiedYoutubeCount + 1
                
                
        else:
            nonVerifiedcount = nonVerifiedcount + 1
            nonVerifiedAuthorCount = nonVerifiedAuthorCount + int(str(document["authoredPostCount"]))
            nonVerifiedPostCount = nonVerifiedPostCount + int(str(document["postCount"]))
            nonVerifiedLoopCount = nonVerifiedLoopCount + int(str(document["loopCount"]))
            nonVerifiedFollowingCount = nonVerifiedFollowingCount + int(str(document["followingCount"]))
            nonVerifiedFollowerCount = nonVerifiedFollowerCount + int(str(document["followerCount"]))
            
            if len(str(document["location"])) > 0:
                nonVerifiedLocationCount = nonVerifiedLocationCount + 1
            
            if "twitter" in str(document["description"]).lower():
                nonVerifiedTwitterCount = nonVerifiedTwitterCount + 1
            
            if "instagram" in str(document["description"]).lower():
                nonVerifiedInstagramCount = nonVerifiedInstagramCount + 1
            
            if "youtube" in str(document["description"]).lower():
                nonVerifiedYoutubeCount = nonVerifiedYoutubeCount + 1
    
    print "explicit content users:"
    
    print "total authored post: "+str(verifiedAuthorCount)
    print "average authored post: "+str(verifiedAuthorCount/verifiedcount)
    
    print "total  number of post: "+str(verifiedPostCount)
    print "average  number of post: "+str(verifiedPostCount/verifiedcount)
    
    print "total  number of loop: "+str(verifiedLoopCount)
    print "average  number of loop: "+str(verifiedLoopCount/verifiedcount)
    
    print "total  number of following: "+str(verifiedFollowingCount)
    print "average  number of following: "+str(verifiedFollowingCount/verifiedcount)
    
    print "total  number of follower: "+str(verifiedFollowerCount)
    print "average  number of follower: "+str(verifiedFollowerCount/verifiedcount)
    
    print "total  number of location: "+str(verifiedLocationCount)
    print "percentage of location: "+str(float(verifiedLocationCount)/float(verifiedcount))
    
    print "total  number of twitter: "+str(verifiedTwitterCount)
    print "percentage of twitter: "+str(float(verifiedTwitterCount)/float(verifiedcount))
    
    print "total  number of instagram: "+str(verifiedInstagramCount)
    print "percentage of instagram: "+str(float(verifiedInstagramCount)/float(verifiedcount))
    
    print "total  number of youtube: "+str(verifiedYoutubeCount)
    print "percentage of youtube: "+str(float(verifiedYoutubeCount)/float(verifiedcount))
    
    
    
    
    
    
    print "non explicit content users:"
    
    print "total authored post: "+str(nonVerifiedAuthorCount)
    print "average authored post: "+str(nonVerifiedAuthorCount/nonVerifiedcount)
    
    print "total  number of post: "+str(nonVerifiedPostCount)
    print "average  number of post: "+str(nonVerifiedPostCount/nonVerifiedcount)
    
    print "total  number of loop: "+str(nonVerifiedLoopCount)
    print "average  number of loop: "+str(nonVerifiedLoopCount/nonVerifiedcount)
    
    print "total  number of following: "+str(nonVerifiedFollowingCount)
    print "average  number of following: "+str(nonVerifiedFollowingCount/nonVerifiedcount)
    
    print "total  number of follower: "+str(nonVerifiedFollowerCount)
    print "average  number of follower: "+str(nonVerifiedFollowerCount/nonVerifiedcount)
    
    print "total  number of location: "+str(nonVerifiedLocationCount)
    print "percentage of location: "+str(float(nonVerifiedLocationCount)/float(nonVerifiedcount))
    
    print "total  number of twitter: "+str(nonVerifiedTwitterCount)
    print "percentage of twitter: "+str(float(nonVerifiedTwitterCount)/float(nonVerifiedcount))
    
    print "total  number of instagram: "+str(nonVerifiedInstagramCount)
    print "percentage of instagram: "+str(float(nonVerifiedInstagramCount)/float(nonVerifiedcount))
    
    print "total  number of youtube: "+str(nonVerifiedYoutubeCount)
    print "percentage of youtube: "+str(float(nonVerifiedYoutubeCount)/float(nonVerifiedcount))


def getSelectedPostsFromCollection():
    databaseName = "VineDatabase"
    collectionName = "CollectedUserPosts"
    documents = mongoOperations.getSelectedPostsFromCollection(databaseName, collectionName)
    postidList = []
    for document in documents:
        postidList.append(str(document['postId']))
    return postidList

def getPostIDsForUser(userid):
    databaseName = "VineDatabase"
    collectionName = "CollectedUserPosts"
    documents = mongoOperations.findPostsFromCollection(databaseName, collectionName, userid)
    postidList = []
    for document in documents:
        postidList.append(str(document['postId']))
    return postidList


def verifiedUserAverageStats():
    databaseName = "VineDatabase"
    collectionName = "CollectedUserBio"
    documents = mongoOperations.findAllDataFromCollection(databaseName, collectionName)
    verifiedcount = 0
    nonVerifiedcount = 0
    
    verifiedFollowerCount = 0
    nonVerifiedFollowerCount = 0
    
    verifiedFollowingCount = 0
    nonVerifiedFollowingCount = 0
    
    verifiedLoopCount = 0
    nonVerifiedLoopCount = 0
    
    verifiedPostCount = 0
    nonVerifiedPostCount = 0
    
    verifiedAuthorCount = 0
    nonVerifiedAuthorCount = 0
    
    verifiedExplicitCount = 0
    nonVerifiedExplicitCount = 0
    
    verifiedLocationCount = 0
    nonVerifiedLocationCount = 0
    
    verifiedTwitterCount = 0
    nonVerifiedTwitterCount = 0
    
    verifiedInstagramCount = 0
    nonVerifiedInstagramCount = 0
    
    verifiedYoutubeCount = 0
    nonVerifiedYoutubeCount = 0
    
    
    for document in documents:
        if str(document["verified"]) == "1":
            verifiedcount = verifiedcount + 1
            verifiedAuthorCount = verifiedAuthorCount + int(str(document["authoredPostCount"]))
            verifiedExplicitCount = verifiedExplicitCount + int(str(document["explicitContent"]))
            verifiedPostCount = verifiedPostCount + int(str(document["postCount"]))
            verifiedLoopCount = verifiedLoopCount + int(str(document["loopCount"]))
            verifiedFollowingCount = verifiedFollowingCount + int(str(document["followingCount"]))
            verifiedFollowerCount = verifiedFollowerCount + int(str(document["followerCount"]))
            if len(str(document["location"])) > 0:
                verifiedLocationCount = verifiedLocationCount + 1
            if "twitter" in str(document["description"]).lower():
                verifiedTwitterCount = verifiedTwitterCount + 1
            
            if "instagram" in str(document["description"]).lower():
                verifiedInstagramCount = verifiedInstagramCount + 1
            
            if "youtube" in str(document["description"]).lower():
                verifiedYoutubeCount = verifiedYoutubeCount + 1
                
                
        else:
            nonVerifiedcount = nonVerifiedcount + 1
            nonVerifiedAuthorCount = nonVerifiedAuthorCount + int(str(document["authoredPostCount"]))
            nonVerifiedExplicitCount = nonVerifiedExplicitCount + int(str(document["explicitContent"]))
            nonVerifiedPostCount = nonVerifiedPostCount + int(str(document["postCount"]))
            nonVerifiedLoopCount = nonVerifiedLoopCount + int(str(document["loopCount"]))
            nonVerifiedFollowingCount = nonVerifiedFollowingCount + int(str(document["followingCount"]))
            nonVerifiedFollowerCount = nonVerifiedFollowerCount + int(str(document["followerCount"]))
            
            if len(str(document["location"])) > 0:
                nonVerifiedLocationCount = nonVerifiedLocationCount + 1
            
            if "twitter" in str(document["description"]).lower():
                nonVerifiedTwitterCount = nonVerifiedTwitterCount + 1
            
            if "instagram" in str(document["description"]).lower():
                nonVerifiedInstagramCount = nonVerifiedInstagramCount + 1
            
            if "youtube" in str(document["description"]).lower():
                nonVerifiedYoutubeCount = nonVerifiedYoutubeCount + 1
    
    print "verified users:"
    print "total explicit content: "+str(verifiedExplicitCount)
    print "total explicit content percentage: "+str(float(verifiedExplicitCount)/float(verifiedcount))
    
    print "total authored post: "+str(verifiedAuthorCount)
    print "average authored post: "+str(verifiedAuthorCount/verifiedcount)
    
    print "total  number of post: "+str(verifiedPostCount)
    print "average  number of post: "+str(verifiedPostCount/verifiedcount)
    
    print "total  number of loop: "+str(verifiedLoopCount)
    print "average  number of loop: "+str(verifiedLoopCount/verifiedcount)
    
    print "total  number of following: "+str(verifiedFollowingCount)
    print "average  number of following: "+str(verifiedFollowingCount/verifiedcount)
    
    print "total  number of follower: "+str(verifiedFollowerCount)
    print "average  number of follower: "+str(verifiedFollowerCount/verifiedcount)
    
    print "total  number of location: "+str(verifiedLocationCount)
    print "percentage of location: "+str(float(verifiedLocationCount)/float(verifiedcount))
    
    print "total  number of twitter: "+str(verifiedTwitterCount)
    print "percentage of twitter: "+str(float(verifiedTwitterCount)/float(verifiedcount))
    
    print "total  number of instagram: "+str(verifiedInstagramCount)
    print "percentage of instagram: "+str(float(verifiedInstagramCount)/float(verifiedcount))
    
    print "total  number of youtube: "+str(verifiedYoutubeCount)
    print "percentage of youtube: "+str(float(verifiedYoutubeCount)/float(verifiedcount))
    
    
    
    
    
    
    print "non verified users:"
    print "total explicit content: "+str(nonVerifiedExplicitCount)
    print "total explicit content percentage: "+str(float(nonVerifiedExplicitCount)/float(nonVerifiedcount))
    
    print "total authored post: "+str(nonVerifiedAuthorCount)
    print "average authored post: "+str(nonVerifiedAuthorCount/nonVerifiedcount)
    
    print "total  number of post: "+str(nonVerifiedPostCount)
    print "average  number of post: "+str(nonVerifiedPostCount/nonVerifiedcount)
    
    print "total  number of loop: "+str(nonVerifiedLoopCount)
    print "average  number of loop: "+str(nonVerifiedLoopCount/nonVerifiedcount)
    
    print "total  number of following: "+str(nonVerifiedFollowingCount)
    print "average  number of following: "+str(nonVerifiedFollowingCount/nonVerifiedcount)
    
    print "total  number of follower: "+str(nonVerifiedFollowerCount)
    print "average  number of follower: "+str(nonVerifiedFollowerCount/nonVerifiedcount)
    
    print "total  number of location: "+str(nonVerifiedLocationCount)
    print "percentage of location: "+str(float(nonVerifiedLocationCount)/float(nonVerifiedcount))
    
    print "total  number of twitter: "+str(nonVerifiedTwitterCount)
    print "percentage of twitter: "+str(float(nonVerifiedTwitterCount)/float(nonVerifiedcount))
    
    print "total  number of instagram: "+str(nonVerifiedInstagramCount)
    print "percentage of instagram: "+str(float(nonVerifiedInstagramCount)/float(nonVerifiedcount))
    
    print "total  number of youtube: "+str(nonVerifiedYoutubeCount)
    print "percentage of youtube: "+str(float(nonVerifiedYoutubeCount)/float(nonVerifiedcount))
    



def locationUserAverageStats():
    databaseName = "VineDatabase"
    collectionName = "CollectedUserBio"
    documents = mongoOperations.findAllDataFromCollection(databaseName, collectionName)
    locationcount = 0
    nonLocationcount = 0
    
    locationFollowerCount = 0
    nonLocationFollowerCount = 0
    
    locationFollowingCount = 0
    nonLocationFollowingCount = 0
    
    locationLoopCount = 0
    nonLocationLoopCount = 0
    
    locationPostCount = 0
    nonLocationPostCount = 0
    
    locationAuthorCount = 0
    nonLocationAuthorCount = 0
    
    locationExplicitCount = 0
    nonLocationExplicitCount = 0

    
    locationTwitterCount = 0
    nonLocationTwitterCount = 0
    
    locationInstagramCount = 0
    nonLocationInstagramCount = 0
    
    locationYoutubeCount = 0
    nonLocationYoutubeCount = 0
    
    
    for document in documents:
        if len(str(document["location"])) > 0:
            locationcount = locationcount + 1
            locationAuthorCount = locationAuthorCount + int(str(document["authoredPostCount"]))
            locationExplicitCount = locationExplicitCount + int(str(document["explicitContent"]))
            locationPostCount = locationPostCount + int(str(document["postCount"]))
            locationLoopCount = locationLoopCount + int(str(document["loopCount"]))
            locationFollowingCount = locationFollowingCount + int(str(document["followingCount"]))
            locationFollowerCount = locationFollowerCount + int(str(document["followerCount"]))
            if "twitter" in str(document["description"]).lower():
                locationTwitterCount = locationTwitterCount + 1
            
            if "instagram" in str(document["description"]).lower():
                locationInstagramCount = locationInstagramCount + 1
            
            if "youtube" in str(document["description"]).lower():
                locationYoutubeCount = locationYoutubeCount + 1
                
                
        else:
            nonLocationcount = nonLocationcount + 1
            nonLocationAuthorCount = nonLocationAuthorCount + int(str(document["authoredPostCount"]))
            nonLocationExplicitCount = nonLocationExplicitCount + int(str(document["explicitContent"]))
            nonLocationPostCount = nonLocationPostCount + int(str(document["postCount"]))
            nonLocationLoopCount = nonLocationLoopCount + int(str(document["loopCount"]))
            nonLocationFollowingCount = nonLocationFollowingCount + int(str(document["followingCount"]))
            nonLocationFollowerCount = nonLocationFollowerCount + int(str(document["followerCount"]))
            
            if "twitter" in str(document["description"]).lower():
                nonLocationTwitterCount = nonLocationTwitterCount + 1
            
            if "instagram" in str(document["description"]).lower():
                nonLocationInstagramCount = nonLocationInstagramCount + 1
            
            if "youtube" in str(document["description"]).lower():
                nonLocationYoutubeCount = nonLocationYoutubeCount + 1
    
    print "location set users:"
    print "total explicit content: "+str(locationExplicitCount)
    print "total explicit content percentage: "+str(float(locationExplicitCount)/float(locationcount))
    
    print "total authored post: "+str(locationAuthorCount)
    print "average authored post: "+str(locationAuthorCount/locationcount)
    
    print "total  number of post: "+str(locationPostCount)
    print "average  number of post: "+str(locationPostCount/locationcount)
    
    print "total  number of loop: "+str(locationLoopCount)
    print "average  number of loop: "+str(locationLoopCount/locationcount)
    
    print "total  number of following: "+str(locationFollowingCount)
    print "average  number of following: "+str(locationFollowingCount/locationcount)
    
    print "total  number of follower: "+str(locationFollowerCount)
    print "average  number of follower: "+str(locationFollowerCount/locationcount)

    
    print "total  number of twitter: "+str(locationTwitterCount)
    print "percentage of twitter: "+str(float(locationTwitterCount)/float(locationcount))
    
    print "total  number of instagram: "+str(locationInstagramCount)
    print "percentage of instagram: "+str(float(locationInstagramCount)/float(locationcount))
    
    print "total  number of youtube: "+str(locationYoutubeCount)
    print "percentage of youtube: "+str(float(locationYoutubeCount)/float(locationcount))
    
    
    
    
    
    
    print "non location users:"
    print "total explicit content: "+str(nonLocationExplicitCount)
    print "total explicit content percentage: "+str(float(nonLocationExplicitCount)/float(nonLocationcount))
    
    print "total authored post: "+str(nonLocationAuthorCount)
    print "average authored post: "+str(nonLocationAuthorCount/nonLocationcount)
    
    print "total  number of post: "+str(nonLocationPostCount)
    print "average  number of post: "+str(nonLocationPostCount/nonLocationcount)
    
    print "total  number of loop: "+str(nonLocationLoopCount)
    print "average  number of loop: "+str(nonLocationLoopCount/nonLocationcount)
    
    print "total  number of following: "+str(nonLocationFollowingCount)
    print "average  number of following: "+str(nonLocationFollowingCount/nonLocationcount)
    
    print "total  number of follower: "+str(nonLocationFollowerCount)
    print "average  number of follower: "+str(nonLocationFollowerCount/nonLocationcount)
    
    
    print "total  number of twitter: "+str(nonLocationTwitterCount)
    print "percentage of twitter: "+str(float(nonLocationTwitterCount)/float(nonLocationcount))
    
    print "total  number of instagram: "+str(nonLocationInstagramCount)
    print "percentage of instagram: "+str(float(nonLocationInstagramCount)/float(nonLocationcount))
    
    print "total  number of youtube: "+str(nonLocationYoutubeCount)
    print "percentage of youtube: "+str(float(nonLocationYoutubeCount)/float(nonLocationcount))
