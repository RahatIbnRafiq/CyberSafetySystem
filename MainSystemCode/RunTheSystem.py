

import VineAPI.VineAPI as vineapi 
from PredictorModule.Predictor import CyberSafetyPredcitor as CyberSafetyPredictor


#collect the list of apis
#vine_api_class = vineapi.VineAPIClass()
#vine_api_list = vine_api_class.getVineAPIList()

cybersafety_predictor = CyberSafetyPredictor()
print cybersafety_predictor.predcitor


print "done"

