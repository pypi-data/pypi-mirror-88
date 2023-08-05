import os
import unittest
from machine_learning.utils import my_train_test_split, encoder, file_prep
from machine_learning.decision_stamp import decision_stamp

'''
    Testing the Decision Stamp behavior
'''
PATH = os.path.join(os.getcwd(), '..')
DATAPATH = os.path.join(PATH, 'dataset')
DATAFILES = os.listdir(DATAPATH) 
FILESPATH = os.path.join(DATAPATH, DATAFILES[0])
X, y, features = file_prep(FILESPATH)
X_train, X_test, y_train, y_test = my_train_test_split(
    X, y, test_size=0.20, random_state=42)

class TestDecisionTree(unittest.TestCase):
    '''
    Class to test the decision tree
    '''
    def test_initial_clf(self):
        '''
        Function to test the inital state of the classifer
        '''
        my_stamp = decision_stamp()
        self.assertIsNone(my_stamp.feature_index)
        self.assertIsNone(my_stamp.weights)
        self.assertEqual(my_stamp.threshold, 0)
        self.assertEqual(my_stamp.pairty, 1)
        self.assertEqual(my_stamp.weight_error,0)
    
    def test_behavior(self):
        '''
        Function to test the behavior of the classifer
        '''
        my_stamp = decision_stamp()
        my_stamp.fit(X_train,y_train)
        prediction = my_stamp.predict(X_test)
        self.assertEqual(my_stamp.feature_index, 4)

if __name__ == "__main__":
   unittest.main()
