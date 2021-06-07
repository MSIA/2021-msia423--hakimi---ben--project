import pytest

import pandas as pd

import src.cleanRaw as cr

df_in = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1], [3, 1, 2, 1,"",0, 0, 0], [2, 1, 1, 1,5,0,5,1], [5, 0, 5, 1,"",0,0,0], [1, 2, 1, 1,"",0,0,0]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2"])

def test_findFavored():
    df_test = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1,"V"], [3, 1, 2, 1,"",0, 0, 0,"V"], [2, 1, 1, 1,5,0,5,1,"V"], [5, 0, 5, 1,"",0,0,0,"V"], [1, 2, 1, 1,"",0,0,0,"V"]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2","Fav"])
    df_out = cr.findFavored(4, df_in)
    assert df_test.equals(df_out)