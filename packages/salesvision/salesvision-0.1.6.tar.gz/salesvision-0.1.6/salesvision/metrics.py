import numpy as np


def set2set_similarity_metric(pred1: dict, pred2: dict) -> float:
    """
    Evaluate similarity between two predictions,
    than greater value, than more similar things clothes
    Args:
        pred1: system prediction
        pred2: system prediction

    Returns:
        Similarity score
    """
    if pred1['prediction']['status'] != '0' or \
            pred2['prediction']['status'] != '0':
        return -1E+5

    score = 0
    alpha = [1.0, 0.1]
    beta = [[1.0, 0.8], [0.5, 1.0]]
    matches_count = 0
    matched_items = []

    for item1 in pred1['prediction']['result']:
        for item2 in pred2['prediction']['result']:
            if item2 in matched_items:
                continue

            matched_tags_count = 0
            if 'tags' in item1.keys() and 'tags' in item2.keys():
                for category in item1['tags'].keys():
                    matched_tags_count += int(
                        item1['tags'][category] == item2['tags'][category]
                    )
            matched_tags_rate = matched_tags_count / 7.0

            colors_similarity_score = 2.0 - np.linalg.norm(
                np.array(item1['color_embedding']) -
                np.array(item2['color_embedding'])
            )

            if item1['category'] == item2['category']:
                items_score = alpha[0]*(
                        beta[0][0]*matched_tags_rate +
                        beta[0][1]*colors_similarity_score
                )
                matched_items.append(item2)
            else:
                items_score = alpha[1] * (
                        beta[1][0] * matched_tags_rate +
                        beta[1][1] * colors_similarity_score
                )

            matches_count += 1
            score += items_score

    score = score / matches_count
    return score


def set2element_similarity_metric(
        pred1: dict, pred2: dict,
        alpha: float = 0.5, beta: float = 0.9) -> float:
    """
    Evaluate similarity between two predictions,
    than greater value, than more similar things clothes
    Args:
        pred1: system prediction
        pred2: system prediction
        alpha:
        beta:

    Returns:
        Similarity score
    """
    if pred1['prediction']['status'] != '0' or \
            pred2['prediction']['status'] != '0':
        return -1E+5

    assert 0 <= alpha <= 1
    assert 0 <= beta <= 1

    matches_count = 0
    match_scores = []

    for item1 in pred1['prediction']['result']:
        for item2 in pred2['prediction']['result']:
            matched_tags_count = 0
            if 'tags' in item1.keys() and 'tags' in item2.keys():
                for category in item1['tags'].keys():
                    matched_tags_count += int(
                        item1['tags'][category] == item2['tags'][category]
                    )
            matched_tags_rate = matched_tags_count / 7.0

            colors_similarity_score = (2.0 - np.linalg.norm(
                np.array(item1['color_embedding']) -
                np.array(item2['color_embedding'])
            )) / 2.0

            item_score = \
                matched_tags_rate * alpha \
                + colors_similarity_score * (1.0 - alpha)

            matches_count += 1
            match_scores.append(
                item_score * beta
                if item1['category'] == item2['category'] else
                item_score * (1.0 - beta)
            )

    match_scores.sort(reverse=True)

    score = match_scores[0]
    return score
