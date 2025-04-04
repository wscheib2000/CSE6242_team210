# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 13:18:44 2025

@author: samue
"""

import pandas as pd
import numpy as np
import sys
from sklearn.metrics.pairwise import cosine_similarity
import pickle

#Gets the cosine similarity between our given song vector and
#the other rows in the reference

def get_cossim(d, reference, index): 
    a = d[index, :].reshape(1, -1)  # Query vector
    similarities = cosine_similarity(a, d)[0]  # Compute similarity for all rows
    outlist = sorted(enumerate(similarities), key=lambda x: -x[1]) 
    return outlist

# Runs through original data set and prints out artist names and artist terms. 
# Mostly for checking if the rest of this is working well.

# get_terms is only if you want to see the artist_terms. I don't recommend it,
# because it's gonna clutter up the output. I just had it on hand because it
# was useful when checking accuracy. 

def check_artists(inlist, reference, listlen=10):
    #get_terms = lambda x: ast.literal_eval(reference.iloc[inlist[x][0]]['artist_terms'])[0:5]
    a = [[inlist[i][0],reference.iloc[inlist[i][0]]['artist_name'],
                        inlist[i][1]] for i in range(listlen)]
    b = '\n'.join([str(i) for i in a])
    return a, b


# Combines and and weights the measurements from earlier
def combine_cos_sims(inlist, weights = None):
    if weights == None: 
        weights = [1/sum(weights) for _ in inlist]
    #This else clause was just for normalizing the weights. Didn't seem super useful, though.
    else: 
        weights = [i/sum(weights) for i in weights]
    inlist = [sorted(i, key = lambda x: x[0]) for i in inlist]
    inlist = [[inlist[0][i][0], sum([(inlist[j][i][1]*weights[j]) for j in range(len(inlist))])] for i in range(len(inlist[0]))]
    return sorted(inlist, key = lambda x: -x[1])


def similar_artists_id_and_cossim(df, index): 
    row = df.iloc[index]
    sorted_row = row[2:len(row)].sort_values(ascending=False)
    outlist = [(sorted_row.index[i], sorted_row.iloc[i]) for i in range(len(sorted_row))]
    return outlist

    


## Takes in up to three values: a row to compare against, user-defined weights,
# and the number of outputs you want to see. 

# By default, the weights are all equal, and the number of outputs is 10. 
# If you want to mess around with weights, just input it as a list like you
# would in Python, like [1,2,3,4,5]. You'll need 5 elements in the list. 


if __name__ == '__main__':
    
    # I'm not sure how you want to handle the databases, so everything below is 
    # just the data you'll need. Feel free to mess with its organization as you see fit. 
    # The one thing I would recommend is that you leave similar_artists as
    # a pickled file or something similar, as the .csv file for it is far larger.
    
    genre_PCA = pd.read_csv('./data/artist_term_components.csv',index_col = 'Unnamed: 0')
    with open('./data/relevant_artist_columns.pkl', 'rb') as f: 
        similar_artists = pickle.load(f)
    with open('./data/pitches_PCA.pkl', 'rb') as f: 
        pitches_PCA = pickle.load(f)
    with open('./data/timbre_PCA.pkl', 'rb') as f: 
        timbre_PCA = pickle.load(f)
    with open('./data/non_nest_PCA.pkl', 'rb') as f: 
        non_nest_PCA = pickle.load(f)
    subset = pd.read_csv('./data/artist_id_and_name.csv',index_col = 'Unnamed: 0')
    
    # Processes command-line arguments
    compare_row = int(sys.argv[1])
    if len(sys.argv) > 3: 
        artist_output = int(sys.argv[3])
    else: 
        artist_output = 10
    if len(sys.argv) > 2: 
        weights = sys.argv[2][1:-1]
        weights = list(weights.split(','))
        weights = [float(i) for i in weights]
    else: 
        weights = [1 for _ in range(5)]
        

    #Gets cosine similarities. My work and Jessica's were in different formats,
    #hence why similar_artists_checklist uses a different function
    non_nest_PCA_checklist = get_cossim(non_nest_PCA, subset, compare_row)
    pitches_PCA_checklist  = get_cossim(pitches_PCA,subset,compare_row)
    timbre_PCA_checklist = get_cossim(timbre_PCA,subset,compare_row)
    genre_PCA_checklist = get_cossim(genre_PCA.to_numpy(),subset,compare_row)
    similar_artists_checklist = similar_artists_id_and_cossim(similar_artists,compare_row)
    
    
    # Assembles a list, runs weighted sum, gets output
    use_list = [non_nest_PCA_checklist,pitches_PCA_checklist,timbre_PCA_checklist,
                genre_PCA_checklist,similar_artists_checklist]
    cossim_combined = combine_cos_sims(use_list,weights)
    outlist, outstr = check_artists(cossim_combined,subset,artist_output)
    outlist = np.array([np.array(i) for i in outlist])
    outlist = pd.DataFrame(outlist)
    outlist = outlist.set_axis(['index','artist_name','weighted_similarity'],axis=1)
    outlist = outlist.reset_index().rename(columns={"level_0": "rank"})
    print(outlist.to_csv(lineterminator='\n', index=False), end="")