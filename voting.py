def dictatorship(preferences, agent) -> int:
    if agent not in preferences.voters():
        raise ValueError("Invalid agent")
    candidates = preferences.candidates()
    for candidate in candidates:
        if preferences.get_preference(candidate, agent) == 0:
            return candidate
        
def scoring_rule(preferences, score_vector, tie_break) -> int:
    candidates = preferences.candidates()
    voters = preferences.voters()

    if len(score_vector) != len(candidates):
        raise ValueError("Score vector length must match the number of candidates")

    scores = {candidate: 0 for candidate in candidates}

    for voter in voters:
        for candidate in candidates:
            rank = preferences.get_preference(candidate, voter)
            scores[candidate] += score_vector[rank]

    max_score = max(scores.values())
    top_candidates = [candidate for candidate, score in scores.items() if score == max_score]

    # Apply tie-breaking
    return tie_breaking(preferences, top_candidates, tie_break)

def plurality(preferences, tie_break) -> int:
    candidates = preferences.candidates()
    voters = preferences.voters()

    first_place_count = {candidate: 0 for candidate in candidates}

    for voter in voters:
        for candidate in candidates:
            if preferences.get_preference(candidate, voter) == 0:
                first_place_count[candidate] += 1
                break

    max_count = max(first_place_count.values())
    top_candidates = [candidate for candidate, count in first_place_count.items() if count == max_count]

    # Apply tie-breaking
    return tie_breaking(preferences, top_candidates, tie_break)

def veto(preferences, tie_break) -> int:
    candidates = preferences.candidates()
    voters = preferences.voters()

    scores = {candidate: 0 for candidate in candidates}

    for voter in voters:
        for candidate in candidates:
            if preferences.get_preference(candidate, voter) != len(candidates) - 1:
                scores[candidate] += 1

    max_score = max(scores.values())
    top_candidates = [candidate for candidate, score in scores.items() if score == max_score]

    # Apply tie-breaking
    return tie_breaking(preferences, top_candidates, tie_break)

def borda(preferences, tie_break) -> int:
    candidates = preferences.candidates()
    voters = preferences.voters()

    scores = {candidate: 0 for candidate in candidates}

    for voter in voters:
        for candidate in candidates:
            rank = preferences.get_preference(candidate, voter)
            scores[candidate] += len(candidates) - 1 - rank

    max_score = max(scores.values())
    top_candidates = [candidate for candidate, score in scores.items() if score == max_score]

    # Apply tie-breaking
    return tie_breaking(preferences, top_candidates, tie_break)

def stv(preferences, tie_break) -> int:
    candidates = preferences.candidates()
    voters = preferences.voters()

    while len(candidates) > 1:
        first_place_count = {candidate: 0 for candidate in candidates}

        for voter in voters:
            for candidate in candidates:
                if preferences.get_preference(candidate, voter) == 0:
                    first_place_count[candidate] += 1
                    break

        min_count = min(first_place_count.values())
        eliminated_candidates = [candidate for candidate, count in first_place_count.items() if count == min_count]

        if len(candidates) - len(eliminated_candidates) == 0:
            break

        candidates = [candidate for candidate in candidates if candidate not in eliminated_candidates]

    # Apply tie-breaking
    return tie_breaking(preferences, candidates, tie_break)

def tie_breaking(preferences, candidates, tie_break) -> int:
    if tie_break not in preferences.voters():
        raise ValueError("Invalid tie-breaking agent")

    best_candidate = None
    best_rank = float('inf')

    for candidate in candidates:
        rank = preferences.get_preference(candidate, tie_break)
        if rank < best_rank:
            best_rank = rank
            best_candidate = candidate

    return best_candidate

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

