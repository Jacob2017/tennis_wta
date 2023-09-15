import sqlite3
import pandas as pd
import os
import constants as cn
from db_utils import DbUtils
from match_loader import MatchLoader

class SqliteOperator:
    def __init__(self, db_folder, db_file):
        self.db_folder = db_folder
        self.db_file = db_file

    def add_year_to_table(self, year, table_name, if_exists='fail'):
        if year >= 2000:
            folder = "current_matches"
        else:
            folder = "old_matches"
        wta = MatchLoader(folder, "wta")
        tour_df, qual_df = wta.load_matches(year)

        all_matches_df = pd.concat([tour_df, qual_df], axis=0, ignore_index=True)
        all_matches_df.sort_values(by=["tourney_date","match_id"], axis=0, inplace=True)

        if len(all_matches_df) > 0:
            if SqliteOperator.check_table_available(table_name, all_matches_df):
                try:
                    DbUtils.df_to_table(all_matches_df, table_name, if_exists='append', index=False)
                except sqlite3.IntegrityError as e:
                    all_matches_df = SqliteOperator.find_duplicated_matches(all_matches_df)
                    DbUtils.df_to_table(all_matches_df, table_name, if_exists='append', index=False)
                    # raise e
                # con.commit()
            # con.close()
        else:
            print(f"No matches found for {year}. No DB changes made.")

    @staticmethod
    def find_duplicated_matches(df):
        # df_print(df[df.duplicated(subset=['match_id'],keep=False)])
        dupe_tourney_ids = list(df[df.duplicated(subset=['match_id'],keep=False)]['tourney_id'].unique())
        print(dupe_tourney_ids)
        df = SqliteOperator.fix_duped_ids(df,dupe_tourney_ids)
        return df

    @staticmethod
    def fix_duped_ids(df, tourney_ids):
        for t in tourney_ids:
            t_md_df = df[(df['tourney_id'] == t) & (df['draw_str'] == 'MD')].copy()
            t_q_df = df[(df['tourney_id'] == t) & (df['draw_str'] == 'Q')].copy()
            df = df[df['tourney_id'] != t]
            for temp_df in [t_md_df, t_q_df]:
                temp_df['round_cat'] = pd.Categorical(temp_df['round'],cn.round_order)
                temp_df.sort_values(by=["round_cat","match_num"], axis=0, inplace=True)
                new_match_nums = list(range(1,len(temp_df)+1))
                temp_df['match_num'] = new_match_nums
                temp_df["match_id"] = temp_df.tourney_id + "-" + temp_df.draw_str + "-" + temp_df.match_num.map('{:03d}'.format)
                temp_df.drop(columns=['round_cat'],inplace=True)
                df = pd.concat([df, temp_df], axis=0, ignore_index=True)
        return df
    
    # @staticmethod
    # def make_new_matches_table():
    #     DbUtils.reset_table("wta_matches_v2",cn.output_cols)
    #     player_id_map = csv_to_dict(os.path.join("outputs","wta_player_id_mapping.csv"))
    #     annual_query_template = SqliteOperator.get_sql_file("annual_matches.sql")
    #     year = 1967

    @staticmethod
    def get_sql_file(filename, folder):
        path = os.path.join(folder,filename)
        with open(path,'r') as sql_file:
            sql_str = sql_file.read()
        return sql_str
    
    @staticmethod
    def check_table_available(table_name, all_matches_df):
        table_exists = DbUtils.check_table_exists(table_name)
        if not table_exists:
            print("No table found.")
            return True
        
        sample_size = round(len(all_matches_df) * 0.01)
        match_id_sample = list(all_matches_df.sample(sample_size).match_id)
        match_id_str = ", ".join(["'" + x + "'" for x in match_id_sample])
        
        try:
            res = DbUtils.run_query(f"SELECT match_id FROM {table_name} WHERE match_id in ({match_id_str})", get_df=True, verbose=False)
        except sqlite3.OperationalError as e:
            if "no such column" in str(e):
                print(e)
                return True
            else:
                raise e
            
        if len(res) > 0:
            print(f"{len(res)} results of {sample_size} found. Not available.")
            return False
        else:
            print("No matching results found. Table available.")
            return True
        


# gs_ids1 = list(tour_df[tour_df['tourney_level']=='G']['tourney_id'].unique())
# gs_ids2 = list(qual_df[qual_df['tourney_level']=='G']['tourney_id'].unique())

# gs_sample_df = all_matches_df[all_matches_df['tourney_id']==gs_ids[0]]
# print(gs_ids1+gs_ids2)
# print(tour_df.columns)
# df_print(tour_df.sample(25))
# # print(tour_df.shape)
# # print(qual_df.shape)

# df_print(qual_df.sample(50))
# print(all_matches_df.shape)
# print(all_matches_df.columns)


# print(all_matches_df.columns)
