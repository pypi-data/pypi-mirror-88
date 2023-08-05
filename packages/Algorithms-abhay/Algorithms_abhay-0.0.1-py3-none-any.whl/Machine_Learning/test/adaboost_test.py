import os, sys
import unittest 
from ..utils import my_train_test_split, encoder,file_prep
# from ...machine_learning.utils import my_train_test_split, encoder, file_prep
from ...machine_learning.adaboost import ada_boost

PATH = os.path.join(os.getcwd(), '..')
DATAPATH = os.path.join(PATH, 'dataset')
DATAFILES = os.listdir(DATAPATH)

FILESPATH = os.path.join(DATAPATH, DATAFILES[0])
X, y, features = file_prep(FILESPATH)
X_train, X_test, y_train, y_test = my_train_test_split(
    X, y, test_size=0.20, random_state=42)

class TestAdaBoost(unittest.TestCase):
    '''
    Class to test the Ada boost classifer
    '''
    def test_initial_clf(self):
        '''
        Function to test the inital state of the classifer
        '''
        my_ada_boost = ada_boost()
        self.assertIsNotNone(my_ada_boost.clf)
        self.assertEqual(my_ada_boost.n_estimators, 10)
        self.assertEqual(len(my_ada_boost.scores),0)
        self.assertEqual(len(my_ada_boost.weak_clf),0)

    def test_behavior(self):
        '''
        Function to test the behavior of the classifer
        '''
        my_ada_boost = ada_boost()
        my_ada_boost.fit(X_train, y_train)
        expected_features = [4, 1, 9, 8, 0, 8, 4, 10, 0, 1]
        for i, clf in enumerate(my_ada_boost.weak_clf):
            self.assertEqual(clf.feature_index, expected_features[i])

if __name__ == "__main__":
    unittest.main()