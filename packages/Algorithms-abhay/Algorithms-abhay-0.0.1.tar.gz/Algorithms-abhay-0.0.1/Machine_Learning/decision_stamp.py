'''
    Decision Stamp
'''
import numpy as np

class decision_stamp():
    def __init__(self):
        # The index of the feature used to make classification
        self.feature_index = None
        # The threshold value that the feature should be measured against
        self.threshold = 0
        # Pairity of the threshold
        self.pairty = 1
        self.weight_error = 0
        self.weights = None
    
    def get_params(self):
        parameters = {"feature_index": self.feature_index, 
                        "threshold":self.threshold,
                        "pairty":self.pairty, 
                        "weight_error":self.weight_error}
        return parameters

    
    def fit(self, data=None, label=None, weight=None):
        '''
        X, y, W should all be numpy array
        X shape = [N,M] 
        Y shape = [1,N]
        W shape = [1,N]
        '''
        if (data is None and label is None):
            print("Improper input in the function")
        else:
            f_star = float('inf')
            [row, col] = data.shape
            labels, counts = np.unique(label, return_counts=True)
            if (counts[0] > counts[1]):
                label = -1*label
                self.pairty = -1
            if weight is None:
                counts = (1/labels.shape[0])*(1/np.array(counts))
                new_init_weight = [counts[np.where(labels == l)[0][0]] for l in list(label)]
                weight = np.array(new_init_weight)
            for j in range(col):
                index = data[:,j].argsort()
                x_j = data[:,j][index]
                y_j = label[index]
                d_j = weight[index] 
                f_curr = sum(d_j[y_j == 1])
                if f_curr<f_star:
                    f_star = f_curr
                    theta_star = x_j[0] - 1
                    j_star = j  
                for i in range(0,row-1):
                    f_curr -= y_j[i]*d_j[i]
                    if (f_curr<f_star and x_j[i]!=x_j[i+1]):
                        f_star = f_curr
                        theta_star= 0.5*((x_j[i] + x_j[i+1]))
                        j_star=j
            self.feature_index = j_star
            self.threshold = theta_star
            self.weight_error = f_star
            self.weights = weight
        return self
    def predict(self, data):
        if self.pairty == -1:
            prediction = (data[:,self.feature_index] > self.threshold).astype(int) 
        else :
            prediction = (data[:,self.feature_index] <= self.threshold).astype(int)
        prediction = 2*prediction - 1
        return prediction
    
    def score(self, label, prediction):
        same_check = lambda y1,y2: y1 == y2
        total = sum(map(same_check, label, prediction))
        score = total/len(list(label))
        return score