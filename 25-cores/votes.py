
import numpy
import csv
import re
import json
import sys
import os

sinkfilename = './spikes/spikesource_100.csv.sink'
__location__ = os.path.realpath(
                                os.path.join(os.getcwd(), os.path.dirname(__file__)))
class MNISTImageDest:

    def __init__(self, label, sinkfilename='spikesink.csv'):   
        self.sinkfilename = sinkfilename 
        self.label = label
        with open(sinkfilename, 'r') as csvfile:
            spikes = csv.reader(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            ress = []
            for row in spikes:
               ress.append(int(row[4]))
            if( len(ress)==0):
                self.hist = numpy.zeros(10)
                self.predict = -1
            else:
                self.hist, bin_edges = numpy.histogram(ress, bins=range(0,11))           
                self.predict = numpy.argmax(self.hist)
            if self.predict == 0 and self.hist[0] == 0:
                self.predict = -1;
            self.actual = numpy.argmax(label)    

class MNISTImageDestFloat:

    def __init__(self, label, sinkfilename='spikesink.csv'):   
        self.sinkfilename = sinkfilename 
        self.label = label
        with open(sinkfilename, 'r') as csvfile:
            spikes = csv.reader(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            self.hist = numpy.zeros(10)
            self.predict = -1
            for row in spikes:
                index = int(row[4])
                self.hist[index] += float(row[5])
            self.predict = numpy.argmax(self.hist)
            self.actual = numpy.argmax(label)    
            if self.predict == 0 and self.hist[0] == 0:
                  self.predict = -1;           

def mnist_predict(i):
    file = 'spikesource_'+str(i)+'.csv.sink'
    filename = './spikes/spikesource_'+str(i)+'.csv.sink'
    label_name = os.path.join(__location__, 'labels');
    labels = numpy.loadtxt(label_name)
    index = int(re.findall('\d+', filename )[-1])
    if filename.find("float") > 0 :
        sink = MNISTImageDestFloat(labels[index], filename)
    else :
        sink = MNISTImageDest(labels[index], filename)
    sink.predict = sink.predict
    true_predict = int(sink.predict == sink.actual);
    return true_predict, file,sink.actual,sink.predict
            
def vote_main( start=0, end=10000):
    predicts = 0.0
    for i in range(start, end):
        true_predict, filename, act, pred =  mnist_predict(i)
        predicts = predicts + true_predict
        print('{0}:{1}, Act = {2}, Pred = {3}, True_pred = {4}, Acc = {5}'.format(i,filename,act,pred,true_predict, predicts / (i - start + 1.0)))

    print("Final Accuracy In Simulator:", predicts / (end - start)) 

vote_main( 0, 1000)


   

