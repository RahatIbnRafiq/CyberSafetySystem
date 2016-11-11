'''
Created on Nov 11, 2016

@author: RahatIbnRafiq
'''

class MediaSession:
    def __init__(self,postId,userId):
        self.postId = postId
        self.userId = userId
        self.shareUrl = ""
        self.lastPolled = None
        
        
        
        self.postDescription = ""
        
        self.postDescriptionPolarity = 0.0 
        self.postDescriptionSubjectivity = 0.0
        self.userDescriptionPolarity = 0.0
        self.likeCount = 0.0
        
        self.allCommentPolarityTotal = 100.0
        self.allCommentSubjectivityTotal = 100.0

        
        
        
        self.negativeCommentCountUntilNow = 0
        self.commentCountUntilNow = 0.0
        self.negativeWordCountUntilNow = 0.0
        
        self.priority = -1
        
        
        self.history = []
        self.confidence = []
        self.lastHistoryAlertIndex = 0
        
        self.alert = 0
        
        self.newComments = False
