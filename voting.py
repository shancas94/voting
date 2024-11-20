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