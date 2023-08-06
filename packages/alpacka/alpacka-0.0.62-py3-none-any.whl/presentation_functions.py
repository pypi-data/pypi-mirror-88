# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 15:49:26 2020

@author: Fredrik Möller


Functions seperate and plot the raw metric scores produced by the differenct statistical functions
"""
import numpy as np 
import matplotlib.pyplot as plt
plt.style.use('seaborn')


def sigma_splitter(float_arr):
    """seperates the NCOF score into the 1-3 sigma outliers for the NCOF input
    float_arr: an column array of floats """
    
    "calculates the mean and std of the input score"
    mean = np.mean(float_arr)
    std = np.std(float_arr)
    
    "calculate which indexes that are input inliers"
    inliers = np.where(np.logical_and(float_arr>=mean-std,float_arr<= mean+std))
    inliers = inliers[0].tolist()
    
    "Calculates the 1-sigma postive  outliers"
    one_pos_sigma = np.where(np.logical_and(mean+std <= float_arr, float_arr < mean+2*std))
    "Calculates the 2-sigma postive  outliers"
    two_pos_sigma = np.where(np.logical_and(mean+2*std <= float_arr, float_arr < mean+3*std))
    "Calculates the 3-sigma postive  outliers"
    three_pos_sigma = np.where(mean+3*std <= float_arr)
    
    "Calculates the 1-sigma negative  outliers"
    one_neg_sigma = np.where(np.logical_and(mean-2*std < float_arr, float_arr <= mean-std))
    "Calculates the 2-sigma negative  outliers"
    two_neg_sigma = np.where(np.logical_and(mean-3*std < float_arr, float_arr <= mean-2*std))
    "Calculates the 3-sigma negative  outliers"
    three_neg_sigma = np.where(float_arr <= mean-3*std)

    "stores the positive outliers in a list of lists"
    pos_outliers = [one_pos_sigma[0],
                    two_pos_sigma[0],
                    three_pos_sigma[0]]
    pos_outliers = [l.tolist() for l in pos_outliers]
    
    "stores the negative outliers in a list of lists"
    neg_outliers = [one_neg_sigma[0],
                    two_neg_sigma[0],
                    three_neg_sigma[0]]
    neg_outliers = [l.tolist() for l in neg_outliers]
    
    "OUTPUT: list of indexes"
    "inliers: list of all inliers"
    "pos_outliers: list of 3 lists that corresponds to the 1,2,3 positive sigma outlers"
    "neg_outliers: list of 3 lists that corresponds to the 1,2,3 negative sigma outlers"

    
    return inliers , pos_outliers , neg_outliers


def sigma_splitter_TF_IDF(score):
    """Additional step for sigma splitting for the TF-IDF method
    score: a matrix containinig the TF-IDF score for some senences"""
    inliers = []
    pos_outliers = []
    neg_outliers = []
    for lab in score:
        inliers_tmp , pos_outliers_tmp , neg_outliers_tmp = sigma_splitter(lab)
        inliers.append(inliers_tmp)
        pos_outliers.append(pos_outliers_tmp)
        neg_outliers.append(neg_outliers_tmp)

    "OUTPUT: list of indexes"
    "inliers: list of all inliers"
    "pos_outliers: list of lists that corresponds to the 1,2,3 positive sigma outlers for all classes"
    "neg_outliers: list of lists that corresponds to the 1,2,3 negative sigma outlers for all classes"
    return inliers, pos_outliers, neg_outliers


def NCOF_plot(NCOF ,inliers , pos_outliers , neg_outliers, Dot, Class_perspective):
    """Plots the 1-3 sigma NCOF outliers
    NCOF: get from 'calc_NCOF_from_raw_data' function
    inliers: list of indexes, get from NCOF_sigma_spliter
    pos_outliers: list of lists of indexes, get from NCOF_sigma_spliter
    neg_outliers: list of lists of indexes, get from NCOF_sigma_spliter 
    dot: specifies the scatter dot size of the plot 
    Class_perspective: used during the plotting to specify the perspective of the plot"""
    "plot inliers"
    plt.figure()
    fig, ax = plt.subplots()
    ax.set_ylabel('NCOF score')
    ax.set_xlabel('Dictionary index')
    ax.set_title(f"NCOF score in the persepctive of class: {Class_perspective}")
    y = NCOF[inliers]
    "plot outliers"
    plt.scatter(inliers, y, s = Dot, c = 'k')
    colours= ['r' , 'b' , 'g']
    for i  , out in enumerate(pos_outliers):
        plt.scatter(out, NCOF[out], s= Dot, c = colours[i], alpha = 0.7)
    for i , out in enumerate(neg_outliers):
        plt.scatter(out, NCOF[out], s=Dot , c = colours[i], alpha = 0.7)
    ax.legend(['Inliers' , '1-sigma' , '2-sigma' , '3-sigma'])
    
    "Only the outliers version"
    "plot inliers"
    plt.figure()
    fig, ax = plt.subplots()
    ax.set_ylabel('NCOF score')
    ax.set_xlabel('Dictionary index')
    ax.set_title(f"NCOF score for outliers in the persepctive of class: {Class_perspective}")
    "plot outliers"
    colours= ['r' , 'b' , 'g']
    for i  , out in enumerate(pos_outliers):
        plt.scatter(out, NCOF[out], s= Dot, c = colours[i], alpha = 0.7)
    for i , out in enumerate(neg_outliers):
        plt.scatter(out, NCOF[out], s=Dot , c = colours[i], alpha = 0.7)
    ax.legend(['1-sigma' , '2-sigma' , '3-sigma'])

def TFIDF_plot(TFIDF_score , inliers , outliers , Dot, class_name):
    """Plot the TF-IDF score for the specified input. 
    plots seperated by what datapoints that are considered as inliers and 1-3 sigma outliers. 
    INPUT:
        TFIDF_score: np array containing the TF-IDF score
        inliers: list of indexes that are considered inliers
        outliers: list of lists of indexes that are considered 1-3 sigma outliers
        Dot: int ,scatter dot size
        class_name: string, name ofthe class the data comes from"""
    colours= ['r' , 'b' , 'g']
    plt.figure()
    fig, ax = plt.subplots()
    ax.set_ylabel(f"TF-IDF score")
    ax.set_xlabel(f"Dictionary index")
    ax.set_title(f" TF-IDF score for the {class_name} class")
                
    "Plot inliers"
    y = TFIDF_score[inliers]        
    plt.scatter(inliers,y, s = Dot , c = 'k')
    "Plot outliers"
    for elm , c in zip(outliers,colours):
        y =  TFIDF_score[elm]
        plt.scatter(elm, y, s = Dot , c = c)
    
        ax.legend(['Inliers' , '1-sigma' , '2-sigma' , '3-sigma'])

def TFIDF_plot_outliers(TFIDF_score, outliers, Dot, from_class):
    """Plot the TF-IDF score for the specified input. 
    plots seperated by what datapoints that are considered as inliers and 1-3 sigma outliers. 
    INPUT:
    TFIDF_score: np array containing the TF-IDF score
    outliers: list of lists of indexes that are considered 1-3 sigma outliers
    Dot: int ,scatter dot size
    class_name: string, name ofthe class the data comes from"""
    
    colours= ['r' , 'b' , 'g']
    plt.figure()
    fig, ax = plt.subplots()
    ax.set_ylabel(f"TF-IDF score")
    ax.set_xlabel(f"Dictionary index")
    ax.set_title(f" TF-IDF outlier score for the {from_class} class")
    
    for elm , c in zip(outliers,colours):
        y =  TFIDF_score[elm]
        plt.scatter(elm, y, s = Dot , c = c)

        ax.legend(['1-sigma' , '2-sigma' , '3-sigma'])
        


def ind_2_txt(ind_list, dictionary):
    """Transform a list of integers to their text representation corresponding to the info in the dict
        Input:
            ind_list: single slist of integers
            dictionary: dict where the keys are integers and the values are text strings"""
            
    "chck if input list is a list of lists, else process as a single list"
    if any(isinstance(el, list) for el in ind_list):
        words = []
        for i, lst in enumerate(ind_list):
            txt_words = []
            
            for elm in lst:
                txt_words.append(dictionary[elm])
            words.append(txt_words)
    else:
        words = []
        for elm in ind_list:
            words.append(dictionary[elm])
    
       
        
    return words
    
def symmetric_set_difference(a , b):
    """Takes the symmetric set difference of two lists and presentes the results as two lists containing 'in a but not b' & 'in b but not a' 
        INPUT:
        a: list 
        b: list"""
    a_not_in_b = list(set(a).difference(b))
    b_not_in_a = list(set(b).difference(a))
    return a_not_in_b , b_not_in_a



if __name__ == '__main__':
     pass 












