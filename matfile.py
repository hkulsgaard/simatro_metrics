import svm as svmclass
import scipy.io as sio
#mat = sio.loadmat('svms.mat')
#mat['svms'][0][1]['predictions'][0][0][1][0]['ark_id_svm']
class MatFile():
    def __init__(self,path):
        self.svms = list()
        self.load_svms(path)
    
    def load_svms(self,path):
        self.mat = sio.loadmat(path)
        for svm in self.mat['svms']:
            self.svms.append(svmclass.SVM(svm))

    def get_svms(self):
        return self.svms