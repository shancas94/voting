from Preference import Preference
from voting import *

def test_dictatorship_success(pref_obj):
    print(f"Testing dictatorship() success...")
    for voter in pref_obj.voters():
        winner = dictatorship(pref_obj, voter)
        print(f"Voter: {voter} | Winner: {winner}")
    return

def test_dictatorship_failure(pref_obj):
    print(f"Testing dictatorship() failure...")
    try:
        dictatorship(pref_obj, 4)
    except ValueError as e:
        print(e)
    return

def test_scoring_rule():
    pass

def test_plurality():
    pass

def test_veto():
    pass

def test_borda():
    pass

def test_STV():
    pass

if __name__ == "__main__":
    my_pref_data = Preference({
        1: [3, 1, 2],
        2: [1, 3, 2],
        3: [2, 1, 3]
    })
    test_dictatorship_success(my_pref_data)
    test_dictatorship_failure(my_pref_data)
