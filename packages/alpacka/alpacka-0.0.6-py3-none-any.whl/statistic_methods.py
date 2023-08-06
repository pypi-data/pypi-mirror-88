# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 09:41:26 2020

@author: Fredrik Möller

File contatins functions that performs statistical analysis on the user sepcified input data.
"""
import numpy as np
import keras as ks 

from sklearn.feature_extraction.text import TfidfVectorizer



    
def calc_NCOF_from_raw_data(Data, Labels, Class_perspective, nr_words):
    """Calculates the Normalized Comparative Occurence Frequency for the input data and its asociated labels
        Data: X data, list of strings
        Labels: Y data, list integer labels for the data 
        Class_perspective: integer, from which class persepctive should the NCOF score be produced?
        Outputs the NCOF score for the dataset with the specified class perspective, and a list with the word index used"""
        
    "create a tokenizer that tranforms words from lettwers to text"
    t=ks.preprocessing.text.Tokenizer(num_words = nr_words)
    t.fit_on_texts(Data)
    
    "Tranform the letter sentences to integer representations"
    Data_int=t.texts_to_sequences(Data)
    
    "Create a matrix to store all word occurences for all sentences in each available class "
    rows =  len(np.unique(Labels))
    "cols = len +1 due to index 0 is reserved and unused in the tokenizer "
    if t.num_words == None:
        cols = len(t.index_word)+1
    else:
        cols = nr_words + 1
        
    occurrences = np.zeros([rows,cols]) 
    
    "Loop through all labels and seperate sentences in regards to their class belonging"
    "Couunt the noumer of occurences of each index for each available class. save in the occurence matrix, seperate for each class, corresponding row to each class "
    for i , lab in enumerate(Labels):
        for elm in Data_int[i]:
            occurrences[lab][elm] = occurrences[lab][elm] + 1
    
    "Summerize the number of words in each class and normalize the ocurrence score for each class with this score"
    occ_norm = np.zeros([rows,cols])
    for i , elm in enumerate(occurrences):
        occ_norm[i] = elm / np.sum(elm)

    "make all scores except the ones from the wanted class perspective negative"
    occ_norm = occ_norm *-1    
    occ_norm[Class_perspective] = occ_norm[Class_perspective] *-1

    "OUTPUT"
    "Clculate the NCOF score by summerizing the matrix for each integer, or by 'collapsing' the rows of the matrix"
    NCOF = np.sum(occ_norm,0)
    "A list of each words index in the NCOF score"
    index_words = t.index_word
    
    "removing the first index (0) in the NCOF score and index-dict since it is reserved from the keras tokenizer implementation. https://github.com/keras-team/keras-preprocessing/blob/master/keras_preprocessing/text.py"
    "this is also done to keep the indexation cosistent through the package"
    NCOF = NCOF[1:]
    
    words = [elm for elm in index_words.values()]
    dictionary = { i : words[i] for i in range(0, cols-1 ) }
    
    
    return NCOF , dictionary


def calc_TFIDF_from_raw_data(Data, Labels, nr_words):
    """Calculates the TF-IDF scores all data what correspondinig to the classes in Labels seperately
    Data: list of strings
    Labels: lst of integers"""
    
    "Seperaates the indexes of which data samples in Data that belongs to each class"
    class_indexes=[]
    for elm in np.unique(Labels):
        class_indexes.append([i for i, e in enumerate(Labels) if e == elm])
        
    " create and fit a tfidf tokenizer to the entirety of the data"
    v = TfidfVectorizer(max_features = nr_words)
    v.fit(Data)
    
    "save the tokenizer dictionary and invert it for consistent formatting"
    dictionary = v.vocabulary_
    dictionary = {i: k for k, i in dictionary.items()}
    
    "used to preallocate memory for matrixes"
    dict_size = len(v.vocabulary_)
    "seperate the data o the corresponding class "
    data_sep = []
    for elm in np.unique(Labels):
        data_sep.append([Data[i] for i in class_indexes[elm]])
    
    "Calculate the TF-IDF score for each class seperately and stort the score for all classes in a matrix "
    TF_IDF_score = np.zeros((len(np.unique(Labels)), dict_size))
    for i , elm in enumerate(data_sep):
        "calculation of TF-IDF"
        tmp = v.transform(elm)
        "Get indices that recived a TF-IDF score"
        ind = tmp.indices
        "Store score in the matrix"
        TF_IDF_score[i][ind] = tmp.data

    "OUTPUT: an array of floats so containing all TF-IDF scores for the words in the dictionary "
    "A dictionary containing a map between the tokenizer index and words in the corpus dictionary"
    return TF_IDF_score , dictionary
   

if __name__ == '__main__':
     pass 


    
    