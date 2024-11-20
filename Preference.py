class Preference:
    def __init__(self, preference_data):
        """
        Initialize the Preference object with voter preferences.
        :param preference_data: A dictionary where keys are voter IDs and values are lists of ranked candidates.
                                Example:
                                {
                                    1: [3, 1, 2],  # Voter 1 ranks candidate 3 first, then 1, then 2
                                    2: [1, 3, 2],
                                    3: [2, 1, 3]
                                }
        """
        self.preference_data = preference_data
        self._candidates = list({candidate for prefs in preference_data.values() for candidate in prefs})
        self._voters = list(preference_data.keys())

    def candidates(self):
        """
        Returns a list of candidates in the preference profile.
        :return: List of candidates [1, 2, 3, ...]
        """
        return self._candidates

    def voters(self):
        """
        Returns a list of voters in the preference profile.
        :return: List of voters [1, 2, 3, ...]
        """
        return self._voters

    def get_preference(self, candidate, voter):
        """
        Returns the rank of the given candidate for the given voter.
        Rank 0 indicates the most preferred candidate, and higher values indicate lower preference.
        :param candidate: The candidate whose rank needs to be retrieved.
        :param voter: The voter whose preference is being queried.
        :return: Rank of the candidate for the voter (0 = highest preference).
        :raises ValueError: If the candidate or voter is invalid.
        """
        if voter not in self.voters():
            raise ValueError(f"Invalid voter ID: {voter}")
        if candidate not in self.candidates():
            raise ValueError(f"Invalid candidate ID: {candidate}")
        
        ranked_list = self.preference_data[voter]
        return ranked_list.index(candidate)
