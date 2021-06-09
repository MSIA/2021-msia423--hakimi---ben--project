import pytest

import pandas as pd

import src.cleanRaw as cr

def test_correctSpread():
    df_in = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1,"V"], [3, 1, 2, 1,"",0, 0, 0,"V"], [2, 1, 1, 1,5,0,5,1,"V"], [5, 0, 5, 1,"",0,0,0,"V"], [1, 2, 1, 1,"",0,0,0,"V"]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2","Fav"])
    df_test = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1,"V",1], [3, 1, 2, 1,"",0, 0, 0,"V",0], [2, 1, 1, 1,5,0,5,1,"V",1], [5, 0, 5, 1,"",0,0,0,"V",0], [1, 2, 1, 1,"",0,0,0,"V",0]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2","Fav","Spread"])
    df_out = cr.correctSpread(4, df_in)
    assert df_test.equals(df_out)

def test_correctSpread_non_df():
    df_in = 'I am not a dataframe'
    
    with pytest.raises(TypeError):
        cr.correctSpread(4, df_in)

def test_findFavored():
    df_in = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1], [3, 1, 2, 1,"",0, 0, 0], [2, 1, 1, 1,5,0,5,1], [5, 0, 5, 1,"",0,0,0], [1, 2, 1, 1,"",0,0,0]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2"])
    df_test = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1,"V"], [3, 1, 2, 1,"",0, 0, 0,"V"], [2, 1, 1, 1,5,0,5,1,"V"], [5, 0, 5, 1,"",0,0,0,"V"], [1, 2, 1, 1,"",0,0,0,"V"]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2","Fav"])
    df_out = cr.findFavored(4, df_in)
    assert df_test.equals(df_out)

def test_findFavored_non_df():
    df_in = 'I am not a dataframe'
    
    with pytest.raises(TypeError):
        cr.findFavored(4, df_in)

def test_homePick():
    df_in = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1,"V",0], [3, 1, 2, 1,"",0, 0, 0,"V",0], [2, 1, 1, 1,5,0,5,1,"V",1], [5, 0, 5, 1,"",0,0,0,"V",0], [1, 2, 1, 1,"",0,0,0,"V",0]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2","Fav","Spread"])
    df_test = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1,"H",0], [3, 1, 2, 1,"",0, 0, 0,"V",0], [2, 1, 1, 1,5,0,5,1,"V",1], [5, 0, 5, 1,"",0,0,0,"V",0], [1, 2, 1, 1,"",0,0,0,"V",0]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2","Fav","Spread"])
    df_out = cr.homePick(4, df_in)
    assert df_test.equals(df_out)

def test_homePick_non_df():
    df_in = 'I am not a dataframe'
    
    with pytest.raises(TypeError):
        cr.homePick(4, df_in)

def test_homeSpread():
    df_in = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1,"H",0,0,2], [3, 1, 2, 1,"",0, 0, 0,"V",0,-1,0], [2, 1, 1, 1,5,0,5,1,"V",1,-1,2], [5, 0, 5, 1,"",0,0,0,"V",0,0,0], [1, 2, 1, 1,"",0,0,0,"V",0,-2,0]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2","Fav","Spread","Diff","H_cov"])
    df_test = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1,"H",0,0,2,0], [3, 1, 2, 1,"",0, 0, 0,"V",0,-1,0,0], [2, 1, 1, 1,5,0,5,1,"V",1,-1,2,1], [5, 0, 5, 1,"",0,0,0,"V",0,0,0,0], [1, 2, 1, 1,"",0,0,0,"V",0,-2,0,0]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2","Fav","Spread","Diff","H_cov","homeSpread"])
    df_out = cr.homeSpread(4, df_in)
    assert df_test.equals(df_out)

def test_homeSpread_non_df():
    df_in = 'I am not a dataframe'
    
    with pytest.raises(TypeError):
        cr.homeSpread(4, df_in)

def test_oneLine():
    df_in = pd.DataFrame([[1, 1, 1, 1], [3, 1, 2, 1], [2, 1, 1, 1], [5, 0, 5, 1], [1, 2, 1, 1]], columns = ["Team", "Final", "Open", "ML"])
    df_test = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1], [3, 1, 2, 1,"",0, 0, 0], [2, 1, 1, 1,5,0,5,1], [5, 0, 5, 1,"",0,0,0], [1, 2, 1, 1,"",0,0,0]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2"])
    df_out = cr.oneLine(4, df_in)
    assert df_test.equals(df_out)

def test_oneLine_non_df():
    df_in = 'I am not a dataframe'
    
    with pytest.raises(TypeError):
        cr.oneLine(4, df_in)

def test_whoCovered():
    df_test = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1,"H",0,0,2], [3, 1, 2, 1,"",0, 0, 0,"V",0,-1,0], [2, 1, 1, 1,5,0,5,1,"V",1,-1,2], [5, 0, 5, 1,"",0,0,0,"V",0,0,0], [1, 2, 1, 1,"",0,0,0,"V",0,-2,0]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2","Fav","Spread","Diff","H_cov"])
    df_in = pd.DataFrame([[1, 1, 1, 1, 3, 1, 2, 1,"H",0], [3, 1, 2, 1,"",0, 0, 0,"V",0], [2, 1, 1, 1,5,0,5,1,"V",1], [5, 0, 5, 1,"",0,0,0,"V",0], [1, 2, 1, 1,"",0,0,0,"V",0]], columns = ["Team", "Final", "Open", "ML", "Team_2", "Final_2", "Open_2", "ML_2","Fav","Spread"])
    df_out = cr.whoCovered(4, df_in)
    assert df_test.equals(df_out)

def test_whiCovere_non_df():
    df_in = 'I am not a dataframe'
    
    with pytest.raises(TypeError):
        cr.whoCovered(4, df_in)