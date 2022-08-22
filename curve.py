from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import auc
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot 
import numpy as np

class Curve():
    def __init__(self):
        super().__init__()

    def plot_PRC(self,prediction,verbose,plot):
        y = prediction.get('y')
        y_hat = prediction.get('y_hat')
        scores = prediction.get('scores')
        scores = scores[:,1]
        #----------Presicion/Recall Curve-----------
        lr_precision, lr_recall, _ = precision_recall_curve(y, scores)
        lr_f1, lr_auc = f1_score(y, y_hat), auc(lr_recall, lr_precision)
        rec = recall_score(y, y_hat)
        pre = precision_score(y, y_hat)

        no_skill = len(y[y==1]) / len(y)
        #lr_aux_ajusted = ((lr_auc-no_skill)/(1-no_skill))*0.5+0.5;
        lr_aux_ajusted = (lr_auc-no_skill)/(1-no_skill)
        # summarize scores
        if verbose:
            print('Ark_id_svm: %s' % (prediction.get('ark_id_svm')))
            print('Ark_id: %s' % (prediction.get('ark_id')))
            print('No_Skill: %.3f (0)' % (no_skill))
            print('PR_C AUC: %.3f (%.3f)' % (lr_auc,lr_aux_ajusted))
            print('Rec: %.3f | Pre: %.3f | F1: %.3f\n' % (rec,pre,lr_f1))
        if plot:
            # plot the precision-recall curves
            pyplot.plot([0, 1], [no_skill, no_skill], linestyle='--', label='No Skill')
            pyplot.plot(lr_recall, lr_precision, marker='.', label='Logistic')
            # axis labels
            pyplot.xlabel('Recall')
            pyplot.ylabel('Precision')
            pyplot.xticks(np.arange(0, 1.1, step=0.1))
            pyplot.yticks(np.arange(0, 1.1, step=0.1))
            # show the legend
            pyplot.legend()
            # show the plot
            pyplot.show()
        return lr_auc,lr_aux_ajusted

    def plot_ROC(self,prediction,verbose,plot,curve_color):
        y = prediction.get('y')
        y_hat = prediction.get('y_hat')
        scores = prediction.get('scores')
        scores = scores[:,1]
        #----------ROC Curve-----------
        ns_probs = [0 for _ in range(len(y))]
        no_skill = roc_auc_score(y, ns_probs)
        lr_auc = roc_auc_score(y, scores)

        tn, fp, fn, tp = confusion_matrix(y, y_hat).ravel()
        acc = (tp + tn) / (tn + fp + fn + tp)
        sen = recall_score(y, y_hat)
        spe = tn / (tn + fp)
        bacc = (sen+spe)/2
        f1 = f1_score(y, y_hat)

        tpr = tp / (tp + fn) 
        fpr = fp / (fp + tn)
        pre = precision_score(y, y_hat)

        # summarize scores
        if verbose==1:
            print('Ark_id_svm: %s' % (prediction.get('ark_id_svm')))
            print('Ark_id_testset: %s' % (prediction.get('ark_id')))
            #print('No_Skill: %.3f' % (no_skill))
            print('Sensitivity: %.3f' % (sen))
            print('Specificity: %.3f' % (spe))
            print('Precision: %.3f' % (pre))
            print('Bal.Accuracy: %.3f' % (bacc))
            print('F1 Score: %.3f' % (f1))
            print('ROC AUC: %.3f' % (lr_auc))
            #print('TPR: %.3f' % (tpr))
            #print('FPR: %.3f' % (fpr))
            print('')
        elif verbose==2:
            print('SVM: %s' % (prediction.get('ark_id_svm')[0]))
            print('TestSet: %s' % (prediction.get('ark_id')[0]))
            print('Sen    Spe    Pre    BAcc    F1     Auc')
            print('%.3f  %.3f  %.3f %.3f %.3f  %.3f' % (sen,spe,pre,bacc,f1,lr_auc))
            print('')

        if plot:
            # calculate roc curves
            ns_fpr, ns_tpr, _ = roc_curve(y, ns_probs)
            lr_fpr, lr_tpr, _ = roc_curve(y, scores)
            # plot the roc curve for the model
            #pyplot.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
            #pyplot.plot(lr_fpr, lr_tpr, marker='.', label='Logistic')
            pyplot.plot(ns_fpr, ns_tpr, linestyle='--', color='#5f9ec9')
            pyplot.plot(lr_fpr, lr_tpr, marker='.', color=curve_color)
            # axis labels
            pyplot.xlabel('False Positive Rate')
            pyplot.ylabel('True Positive Rate')
            pyplot.xticks(np.arange(0, 1.1, step=0.1))
            pyplot.yticks(np.arange(0, 1.1, step=0.1))
            pyplot.grid(1, 'major', 'both', color='#cccccc', linestyle='dashed', linewidth=0.5)
            # show the legend
            #pyplot.legend()
            # show the plot
            #pyplot.show()
        return sen,spe,pre,bacc,f1,lr_auc

    