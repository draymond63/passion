from vital_articles import get_vitals, levels_to_df
from data_cleaning import filter_data

from word2vec.w2v_mapping import file_prep, create_w2v_map
from map_display import get_projector_files, display_map


if __name__ == "__main__":
    print("VITALS")
    get_vitals()
    levels_to_df()
    # Take only data from the vital articles
    print("\n\nFILTERING")
    filter_data()
    # Say that articles reference themselves (so they are the farthest in their own axis)
    print("\n\nDATA PREP")
    file_prep()
    # W2V stuff
    print("\n\nMAPPING")
    create_w2v_map()
    # Display w2v vectors
    print("\n\nDISPLAY")
    # get_projector_files()
    display_map() # color='l2'
