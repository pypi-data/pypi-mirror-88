from __future__ import absolute_import
import pickle
import numpy as np 
from .decision_stamp import decision_stamp

class ada_boost():
    def __init__(self, n_estimators=10, clf=decision_stamp):
        self.clf = clf
        self.n_estimators = n_estimators
        self.alpha = list()
        self.scores = list()
        self.weights = list()
        self.weak_clf = list()
        self.label_pred = list()
        self.weight_error = list()

    def get_params(self):
        return{'n_estimators':self.n_estimators}

    def set_parmas(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

    def weight_cal(self, epsolan, weight, label, prediction):
        label_pred = -1*np.multiply(label,prediction)
        self.label_pred.append(label_pred)
        # Alpha
        epsolan/=sum(weight)
        alpha_m = 0.5*np.log((1-epsolan)/epsolan)
        # New weights
        weight_new = np.multiply(weight,np.exp([float(x) * alpha_m for x in label_pred]))
        self.alpha.append(alpha_m)
        return weight_new

    def predict(self,data):
        row, _ = data.shape
        sum_y_pred = np.zeros((row))
        for i, clf in enumerate(self.weak_clf):
            sum_y_pred += self.alpha[i]*clf.predict(data)
        y_pred = np.sign(sum_y_pred)
        return y_pred

    def fit(self, data,label,weight= None):
        row,col = data.shape
        if weight is None:
            labels, counts = np.unique(label, return_counts=True)
            counts = 0.5*(1/np.array(counts))
            new_init_weight = [counts[np.where(labels == l)[0][0]] for l in list(label)]
            weight = np.array(new_init_weight)
            weight = np.ones(row)/row

        for i in range(self.n_estimators):
            self.weights.append(weight)
            curr_clf = self.clf()
            curr_clf.fit(data,label,weight)
            curr_pred = curr_clf.predict(data)
            weight_error = sum([w*(p != l) for p, l, w in zip(curr_pred, label, weight)])
            weight = self.weight_cal(weight_error,weight,label,curr_pred)
            self.weak_clf.append(curr_clf)
            self.scores.append(self.score(data,label))

    def score(self,data,label):
        pred = self.predict(data)
        equality_check = lambda y1,y2: y1 == y2
        total = sum(map(equality_check, label, pred))
        score = total/len(list(label))
        return score

    def save(self, path):
        model = {
            "clf" : self.clf,
            "n_estimators" : self.n_estimators,
            "alpha" : self.alpha,
            "weak_clf" : self.weak_clf,
            "scores" : self.scores
            }
        pickle.dump(model,open(path, 'wb'))

    def load(self, path):
        model = pickle.load(open(path, 'rb'))
        self.clf = model['clf']
        self.n_estimators = model['n_estimators']
        self.alpha = model['alpha']
        self.scores = model['scores']
        self.weak_clf = model['weak_clf']