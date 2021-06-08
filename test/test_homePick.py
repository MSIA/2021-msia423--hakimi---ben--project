import pytest

import pandas as pd

import src.cleanRaw as cr

df_in = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1,"V",0], [3, 1, 2, 1,"",0, 0, 0,"V",0], [2, 1, 1, 1,5,0,5,1,"V",1], [5, 0, 5, 1,"",0,0,0,"V",0], [1, 2, 1, 1,"",0,0,0,"V",0]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2","Fav","Spread"])

def test_homePick():
    df_test = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1,"H",0], [3, 1, 2, 1,"",0, 0, 0,"V",0], [2, 1, 1, 1,5,0,5,1,"V",1], [5, 0, 5, 1,"",0,0,0,"V",0], [1, 2, 1, 1,"",0,0,0,"V",0]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2","Fav","Spread"])
    df_out = cr.homePick(4, df_in)
    assert df_test.equals(df_out)

def test_homePick_non_df():
    df_in = 'I am not a dataframe'
    
    with pytest.raises(TypeError):
        cr.homePick(4, df_in)