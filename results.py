import curve
import matfile
import curve
import numpy as np
import csv
from matplotlib import pyplot 

def save_roc_img(myplot,prefix, ark_id_svm, ark_id_test):
    folder = "D:/Pladema/Datos/scripts/VBM clasico/atrophy_simulation/images tiff/"
    a = str(ark_id_svm).replace("[","(").replace("]",")").replace(", ","_")
    b = str(ark_id_test).replace("[","(").replace("]",")").replace(",","_")
    fname_roc = folder + prefix + a + "_" + b
    myplot.savefig(fname_roc, dpi=600)

def save_metrics_all_csv():
    #Saves the metrics for all the comginations in a CVS file
    with open('aucs.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['svm\\testset'] + svms[0].getPredictionsID())

        for metric, svm in zip(metrics, svms):
            csv_writer.writerow([svm.get('ark_id')[0]]+metric)

def save_metrics_subset_csv(subset):
    #Saves the metrics obtained for the subset in a CVS file
    
    #Take every ith element from every element to converte the columns into rows
    rows = list(list(zip(*metrics))[:])
    
    fname = 'metrics'+str(subset)+'.csv'
    fname = fname.replace(" ","")
    fname = fname.replace(",","_")

    #Writes every element of rows into the CSV file
    with open(fname, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerows(rows[:])

def calculate_metrics_subset(subset, verbose, plot):
    #Gets the metrics values for each SVM from the subset(ark_id)
    for i in range(len(subset)):
        for svm in svms:
            if (svm.get('ark_id')==subset[i]).all() | (svm.get('ark_id')==subset).all(): #seria el "ark_id_svm"
                calculateMetricSVM(svm,subset[i],verbose,plot)
        #save_roc_img(pyplot,"roc_",ark_id,ark_id[i]) #guardar las curvas roc en jpg
        pyplot.show()

    for svm in svms:
            if (svm.get('ark_id')==subset).any(): #seria el "ark_id_svm"
                calculateMetricSVM(svm,subset,verbose,plot)
    #save_roc_img(pyplot,"roc_",ark_id,"ms") #guardar las curvas roc en jpg
    pyplot.show()
    return metrics

def calculateMetricSVM(svm,subset,verbose,plot):
    #print("SVM: ", svm.get('ark_id')) #internal testing
    metric = svm.calculateMetrics(curve,subset, ark_all=0, verbose=verbose, plot=plot)
    metrics.extend(metric)
    #print("Metrics: ", metric) #internal testing
    #print("------------------") #internal testing

def calculate_metrics_all(verbose,plot):
    #Gets metric values for each SVM and prediction
    for svm in svms:
        metric = svm.calculateMetrics(curve, -1, ark_all=1, verbose=verbose, plot=plot)
        #metrics.append(svm.getMetrics())
        metrics.extend(metric)

    return metrics

#------------------------------------------------------------------------------------------------------
#MAIN CODE
#------------------------------------------------------------------------------------------------------

matfile = matfile.MatFile('D:\\Pladema\\Datos\\scripts\\VBM clasico\\atrophy_simulation\\svms4.mat')
svms = matfile.get_svms()
curve = curve.Curve()

#subsets = [[6,11,16],[36,41,46],[66,71,76]]
subsets = [[7,12,17],[37,42,47],[67,72,77]]
#subsets = [[8,13,18],[38,43,48],[68,73,78]]
#subsets = [[9,14,19],[39,44,49],[69,74,79]]

for subset in subsets:
    metrics = list()
#   metrics = calculate_metrics_subset(subset, verbose=2, plot=0)
#   save_metrics_subset_csv(subset)
    metrics = calculate_metrics_all(verbose=2,plot=0)
    save_metrics_subset_csv(str(subset)+'_crossover')


#metrics = calculate_metrics_all(verbose=2,plot=0)
#save_metrics_all_csv()


