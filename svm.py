import matElement

class SVM(matElement.MatElement):
    def __init__(self,svm_mat):
        #mat['svms'][0][1]['predictions'][0][0][1][0]['ark_id_svm']
        super().__init__(svm_mat)
        self.aucprs = list()
        self.aucnprs = list()
        self.metrics = list()
        self.loadPredictions()

        ark_id = self.get('ark_id')
        if (ark_id==[7,12,17]).all() | (ark_id==[37,42,47]).all() | (ark_id==[67,72,77]).all():
            self.setCurveColor('#b74d59')
        elif (ark_id==[7,37,67]).any():
            self.setCurveColor('#e9d047')
        elif (ark_id==[12,42,72]).any():
            self.setCurveColor('#47bc68')
        elif (ark_id==[17,47,77]).any():
            self.setCurveColor('#6079e3')
        else:
            self.setCurveColor('#000000')

    def loadPredictions(self):
        self.predictions = list()
        for p in self.mat[0]['predictions'][0][0]:
            self.predictions.append(matElement.MatElement(p))

    def getPrediction(self,id):
        return self.predictions[id]

    def calculateAUCPR(self,curve,verbose,plot):
        for pred in self.predictions:
            aucpr,aucnpr = curve.plot_PRC(pred,verbose,plot)
            self.aucprs.append(aucpr)
            self.aucnprs.append(aucnpr)

    def calculateMetrics(self,curve,ark_id,ark_all,verbose,plot):
        metric = list()
        for pred in self.predictions:
            if (pred.get('ark_id')==ark_id).all() or ark_all==1 :
                #print("TestSet: ", pred.get('ark_id')) #internal testing
                result = [curve.plot_ROC(pred,verbose,plot,self.color)]
                #result = [self.get('ark_id')[0].tolist(), pred.get('ark_id')[0].tolist(),curve.plot_ROC(pred,verbose,plot,self.color)]
                metric.extend(result)
        self.metrics.extend(metric)
        return metric
    
    def getMetrics(self):
        return self.metrics

    def getAUCPRS(self):
        return self.aucnprs

    def getPredictionsID(self):
        ids = list()
        for pred in self.predictions:
            ids.append(pred.get('ark_id')[0])
        return ids

    def setCurveColor(self,color):
        self.color = color
