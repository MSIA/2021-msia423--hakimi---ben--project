import pytest

import pandas as pd

import src.cleanFull as cf

df_in = pd.DataFrame([[1,"BuffaloBills", "LasVegas"], [0,"SanDiego", "LARams"], [1,"Buffalo", "LAChargers"], [2,"HoustonTexans", "Washington"], [0,"KansasCity", "Houston"]], columns = ["Home_Cover", "H_Team", "V_Team"])

def test_noPush():
    df_test = pd.DataFrame([[1,"BuffaloBills", "LasVegas"], [0,"SanDiego", "LARams"], [1,"Buffalo", "LAChargers"], [0,"KansasCity", "Houston"]], columns = ["Home_Cover", "H_Team", "V_Team"])
    df_out = cf.noPush(df_in, "Home_Cover")
    assert df_test.equals(df_out)

def test_noPush_non_df():
    df_in = 'I am not a dataframe'
    
    with pytest.raises(TypeError):
        cf.noPush(df_in, "Home_Cover")