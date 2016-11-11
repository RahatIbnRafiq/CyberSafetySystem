'''
Created on Nov 11, 2016

@author: RahatIbnRafiq
'''

from collections import defaultdict
from csv import DictReader
from sklearn.feature_extraction import DictVectorizer
from numpy import array
from sklearn import linear_model
from sklearn import cross_validation
from Utility.SentimentExtraction import SentimentExtraction as st
from Utility import Utility as utility




class CyberSafetyPredcitor:
    
    def __init__(self):
        self.rootPath = "C:\\Users\\RahatIbnRafiq\\workspace\\CyberSafetySystem\\"
        self.negativeWordDict = dict()
        self.predcitor = self.LoadPredictor()
        
    
    def TransformIntoVectorsPrediction(self,totalData):
        v = DictVectorizer(sparse=True)
        
        X =  v.fit_transform(totalData)   
        
        return X
    
    
    def FeatureExtractionPrediction(self,mediaSession):
        featureDictionary = defaultdict(int)
        sentiment = st(mediaSession.postDescription)
        featureDictionary["postDescriptionPolarity"] = float(1.0- float(sentiment.getSentimentPolarity()))
        featureDictionary["postDescriptionSubjectivity"] = float(1.0- float(sentiment.getSentimentSubjectivity()))
        featureDictionary["postLikeCount"] = float(mediaSession.likeCount)
    
        mediaSession.postDescriptionPolarity = featureDictionary["postDescriptionPolarity"]
        mediaSession.postDescriptionSubjectivity = featureDictionary["postDescriptionSubjectivity"]
        
        userDescriptionPolaity = utility.getUserDescriptionSentiment(mediaSession.userId)
        mediaSession.postDescriptionPolarity = float(1.0- float(userDescriptionPolaity))
        
        return featureDictionary
    
    
    
    def startPrediction(self,mediaSession,predictor):
        featureDictionary =  self.FeatureExtractionPrediction(mediaSession)
        X= self.TransformIntoVectorsPrediction([featureDictionary])
        return predictor.predict(X)[0]
        
    
    def LoadPredictor(self):
        totalData,totalLabel = self.SplitIntoTestTrainingDataset(self.rootPath+"Data\\vine_meta_data.csv")
        X,Y = self.TransformIntoVectors(totalData,totalLabel)
        X = X.todense()
        
        classifierList = []
        classifierList.append((linear_model.LogisticRegression(),"LogisticRegression"))
        
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y, test_size=0.4, random_state=0)
    
        for classifier in classifierList:
            clf = self.classifierPerformance(classifier,X_train,y_train,X_test,y_test)
            return clf
    
    
    def classifierPerformance(self,classifier,X,Y,X_test,Y_test):
        clf = classifier[0]
        clf.fit(X, Y)
        return clf
        
    
    
    def TransformIntoVectors(self,totalData,totalLabel):
        v = DictVectorizer(sparse=True)
        
        X =  v.fit_transform(totalData)   
        Y = array(totalLabel)
        
        return (X,Y)
        
        
    
    def loadNegativeWordList(self):
        f = open(self.rootPath+"TextFiles\\negative-words.txt","r")
        for line in f:
            line = line.strip()
            self.negativeWordDict[line] = 1
        f.close()
        
        
        
    def SplitIntoTestTrainingDataset(self,filename):
        total_data = DictReader(open(filename, 'Ur'))
        totalData = []
        totalLabel = []
        bullyCount = 0
        notBullyCount = 0
        for ii in total_data:
            tag = str(ii["question2"])
            confidence = float(str(ii["question2:confidence"]))
            if confidence <= 0.6:
                continue
            if tag == "noneBll":
                notBullyCount += 1
                if notBullyCount > 179:
                    continue
            else:
                bullyCount += 1
            featureDictionary = self.FeatureExtraction(ii)
            totalData.append(featureDictionary)
            totalLabel.append(self.getPriorityLabels(tag,confidence))
        return (totalData,totalLabel)
    
    
    
    def FeatureExtraction(self,data):
        featureDictionary = defaultdict(int)
        featureDictionary["postDescriptionPolarity"] = float(1.0- float(data["postDescriptionPolarity"]))
        featureDictionary["postDescriptionSubjectivity"] = float(1.0- float(data["postDescriptionSubjectivity"]))
        featureDictionary["postLikeCount"] = float(float(data["postLikeCount"]))
        return featureDictionary
    
    
    
    def getPriorityLabels(self,tag,confidence):
        if tag == "bullying":
            return 1
        elif tag == "noneBll":
            return 2
        return 1
