import pytest

import pandas as pd

import src.cleanFull as cf

df_in = pd.DataFrame([[1,"BuffaloBills", "LasVegas"], [0,"SanDiego", "LARams"], [1,"Buffalo", "LAChargers"], [2,"HoustonTexans", "Washington"], [0,"KansasCity", "Houston"]], columns = ["Home_Cover", "H_Team", "V_Team"])

def test_fixNames_home():
    df_test = pd.DataFrame([[1,"Buffalo", "LasVegas"], [0,"LAChargers", "LARams"], [1,"Buffalo", "LAChargers"], [2,"Houston", "Washington"], [0,"KansasCity", "Houston"]], columns = ["Home_Cover", "H_Team", "V_Team"])
    df_out = cf.fixNames(df_in, "home", "H_Team", "V_Team")
    assert df_test.equals(df_out)

def test_fixNames_road():
    df_test = pd.DataFrame([[1,"Buffalo", "LVRaiders"], [0,"LAChargers", "LARams"], [1,"Buffalo", "LAChargers"], [2,"Houston", "Washington"], [0,"KansasCity", "Houston"]], columns = ["Home_Cover", "H_Team", "V_Team"])
    df_out = cf.fixNames(df_in, "away", "H_Team", "V_Team")
    assert df_test.equals(df_out)