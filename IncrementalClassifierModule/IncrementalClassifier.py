'''
Created on Nov 11, 2016

@author: RahatIbnRafiq
'''
from collections import defaultdict
from csv import DictReader
from sklearn.feature_extraction import DictVectorizer
from numpy import array
from sklearn import linear_model
from sklearn.utils.extmath import safe_sparse_dot
from Utility.SentimentExtraction import SentimentExtraction as st




class IncrementalClassifier:
    def __init__(self):
        self.numberOfCommentsLimit = 20
        self.rootPath = "C:\\Users\\RahatIbnRafiq\\workspace\\CyberSafetySystem\\"
        self.testDataVideoUrls = []
        self.negativeWordDict = {}
        # load, train the classifier
        self.classifier = self.LoadIncrementalClassifier()
    
    
    def loadNegativeWordList(self):
        f = open(self.rootPath+"TextFiles\\negative_words_list.txt","r")
        for line in f:
            line = line.strip()
            self.negativeWordDict[line] = 1
        f.close()
    
    
    def FeatureExtraction(self,data):
        featureDictionary = defaultdict(int)
        featureDictionary["userDescriptionPolarity"] =float(1.0- float(data["userDescriptionPolarity"]))
        featureDictionary["postDescriptionPolarity"] = float(1.0- float(data["postDescriptionPolarity"]))
        featureDictionary["postDescriptionSubjectivity"] = float(1.0- float(data["postDescriptionSubjectivity"]))
        
        featureDictionary["allCommentPolarityTotal"] = float(100.0 + float(data["allCommentPolarityTotal"]))
        featureDictionary["allCommentSubjectivityTotal"] = float(100.0 + float(data["allCommentSubjectivityTotal"]))
        
        featureDictionary["negativeCommentCount"] = int(data["negativeCommentCount"])
        featureDictionary["negativeCommentPercentage"] = float(data["negativeCommentPercentage"])
        featureDictionary["negativeWordPerNegativeComment"] = float(data["negativeWordPerNegativeComment"])
        return featureDictionary
    
    def SplitIntoTestTrainingDataset(self,filename):
        total_data = DictReader(open(filename, 'Ur'))
        bullyingCount = 0
        notBullyngCount = 0
        
        trainingData = []
        trainingLabel = []
        testData = []
        testLabel = []
        count = 0
        for ii in total_data:
            count = count + 1
            if float(ii["question2:confidence"]) < 0.6:
                continue
            else:
                if ii["question2"] == "noneBll":
                    label = 0
                    notBullyngCount = notBullyngCount + 1
                    if notBullyngCount > 258: #258
                        continue
                    if notBullyngCount > 100:   #100
                        featureDictionary = self.FeatureExtraction(ii)
                        testData.append(featureDictionary)
                        testLabel.append(label)
                        self.testDataVideoUrls.append((str(ii["postShareUrl"]),"0"))
                    else:
                        featureDictionary = self.FeatureExtraction(ii)
                        trainingData.append(featureDictionary)
                        trainingLabel.append(label)
    
                else:
                    label = 1
                    bullyingCount = bullyingCount + 1
                    if bullyingCount > 179:   #179
                        continue
                    if bullyingCount > 100:  #100
                        featureDictionary = self.FeatureExtraction(ii)
                        testData.append(featureDictionary)
                        testLabel.append(label)
                        self.testDataVideoUrls.append((str(ii["postShareUrl"]),"1"))
                    else:
                        featureDictionary = self.FeatureExtraction(ii)
                        trainingData.append(featureDictionary)
                        trainingLabel.append(label)
                if bullyingCount > 179 and notBullyngCount > 258:
                    break
        totalData = []
        totalLabel = []
        
        for label in trainingLabel:
            totalLabel.append(label)
        for label in testLabel:
            totalLabel.append(label)
        
        for data in trainingData:
            totalData.append(data)
        for data in testData:
            totalData.append(data)
        return(totalData,totalLabel)


    def TransformIntoVectors(self,totalData,totalLabel):
        v = DictVectorizer(sparse=True)
        X =  v.fit_transform(totalData)   
        Y = array(totalLabel)
        return (X,Y)


    def buildClassifier(self,classifier,X,Y,X_test,Y_test):
        clf = classifier[0]
        clf.fit(X, Y)
        return clf
    
    
    def LoadIncrementalClassifier(self):
        totalData,totalLabel = self.SplitIntoTestTrainingDataset(self.rootPath+"vine_meta_data.csv")
        X,Y = self.TransformIntoVectors(totalData,totalLabel)
        
        classifierList = []
        classifierList.append((linear_model.LogisticRegression(),"LogisticRegression"))
        
        X_training = X[0:200]
        Y_training = Y[0:200]
        X_test = X[200:437]
        Y_test = Y[200:437]
        for classifier in classifierList:
            clf = self.buildClassifier(classifier,X_training,Y_training,X_test,Y_test)
        return clf
    
    
    
    
    # this is for extracting feature when the data is coming and the system is running. This
    # whole part is the incremental part code that is to be executed when the system is trying to
    # predict a media session on the fly
    def FeatureExtractionPrediction(self,mediaSession):
        featureDictionary = defaultdict(int)
        

        featureDictionary["postDescriptionPolarity"] = mediaSession.postDescriptionPolarity
        featureDictionary["postDescriptionSubjectivity"] = mediaSession.postDescriptionSubjectivity
        featureDictionary["userDescriptionPolarity"] = mediaSession.userDescriptionPolarity
        
        featureDictionary["allCommentPolarityTotal"] = float(mediaSession.allCommentPolarityTotal)
        featureDictionary["allCommentSubjectivityTotal"] = float(mediaSession.allCommentSubjectivityTotal)
        
        featureDictionary["negativeCommentCount"] = int(mediaSession.negativeCommentCountUntilNow)
        try:
            featureDictionary["negativeCommentPercentage"] = float(mediaSession.negativeCommentCountUntilNow/mediaSession.commentCountUntilNow)
            featureDictionary["negativeWordPerNegativeComment"] = float(mediaSession.negativeWordCountUntilNow/mediaSession.negativeCommentCountUntilNow)
        except Exception:
            featureDictionary["negativeCommentPercentage"] = 0.0
            featureDictionary["negativeWordPerNegativeComment"] = 0.0
        return featureDictionary
    
    def TransformIntoVectorsPrediction(self,totalData):
        v = DictVectorizer(sparse=True)
        X =  v.fit_transform(totalData)   
        return X
    
    def startIncrementalPrediction(self,mediaSession):
        featureDictionary = self.FeatureExtractionPrediction(mediaSession)
        X= self.TransformIntoVectorsPrediction([featureDictionary])
        scores = safe_sparse_dot(X, self.classifier.coef_.T,dense_output=True) + self.classifier.intercept_
        confidence= self.classifier._predict_proba_lr(X)[0]
        if scores > -0.5:
            return (1,scores[0][0],confidence)
        else:
            return (0,scores[0][0],confidence)
        
    def updateFeatureValues(self,mediaSession,commentsToBeProcessed):
        for comment in commentsToBeProcessed:
            commentText = str(comment["commentText"])
            sentiment = st(commentText)
            mediaSession.allCommentPolarityTotal = mediaSession.allCommentPolarityTotal + sentiment.getSentimentPolarity()
            mediaSession.allCommentSubjectivityTotal = mediaSession.allCommentSubjectivityTotal + sentiment.getSentimentSubjectivity()
            
            words = commentText.split(" ")
            found = 0
            for word in words:
                try:
                    if self.negativeWordDict[word] == 1:
                        mediaSession.negativeWordCountUntilNow +=1.0
                        found = 1
                except Exception:
                    continue
            if found == 1:
                mediaSession.negativeCommentCountUntilNow +=1.0
            mediaSession.commentCountUntilNow += 1.0

