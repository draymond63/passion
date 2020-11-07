from vital_articles import get_vitals, levels_to_df
from data_cleaning import filter_data
from mapping import add_selfs, get_matrix, display_map


if __name__ == "__main__":
    get_vitals()
    levels_to_df()

    # compile_data()
    filter_data()

    add_selfs()
    get_matrix()
    display_map()