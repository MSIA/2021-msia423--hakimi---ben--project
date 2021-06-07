import pytest

import pandas as pd

import src.cleanRaw as cr

df_in = pd.DataFrame([[1, 1, 1, 1], [3, 1, 2, 1], [2, 1, 1, 1], [5, 0, 5, 1], [1, 2, 1, 1]], columns = ["Team", "Final", "Open", "ML"])

def test_oneLine():
    df_test = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1], [3, 1, 2, 1,"",0, 0, 0], [2, 1, 1, 1,5,0,5,1], [5, 0, 5, 1,"",0,0,0], [1, 2, 1, 1,"",0,0,0]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2"])
    df_out = cr.oneLine(4, df_in)
    assert df_test.equals(df_out)