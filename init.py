from vital_articles import get_vitals, levels_to_df
from data_cleaning import filter_data

from map_display import add_selfs,  display_w2v
from word2vec.w2v_mapping import file_prep, create_w2v_map


if __name__ == "__main__":
    get_vitals()
    levels_to_df()
    # Take only data from the vital articles
    filter_data()
    # Say that articles reference themselves (so they are the farthest in their own axis)
    add_selfs()
    # W2V stuff
    file_prep()
    create_w2v_map()
    # Display w2v vectors
    display_w2v() # color='l2'