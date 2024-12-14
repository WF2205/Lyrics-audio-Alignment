import statistics


# Average absolute error/deviation
# The absolute error measures the time displacement between the actual timestamp 
# and its estimate at the beginning and the end of each lyrical unit. The error is 
# then averaged over all individual errors. An error in absolute terms has the drawback 
# that the perception of an error with the same duration can be different depending on 
# the tempo of the song.
def evaluate_AAE(lrc_results, lrc_reference):
    total_words = len(lrc_reference);
    AAE = 0.0
    for i in range(total_words):
        AAE += (abs(lrc_results[i].start - lrc_reference[i].start) + \
            abs(lrc_results[i].end - lrc_reference[i].end)) / (total_words * 2.0)
    return AAE


# Average absolute median
# The absolute error measures the time displacement between the actual timestamp 
# and its estimate at the beginning and the end of each lyrical unit. The error is 
# then averaged over all individual errors. An error in absolute terms has the drawback 
# that the perception of an error with the same duration can be different depending on 
# the tempo of the song.
def evaluate_AAM(lrc_results, lrc_reference):
    total_words = len(lrc_reference);
    error = []
    for i in range(total_words):
        error.append(abs(lrc_reference[i].start - lrc_results[i].start))
        error.append(abs(lrc_reference[i].end - lrc_results[i].end))

    return statistics.median(error)


# Percentage of correct segments 
# The perceptual dependence on tempo is mitigated by measuring the percentage of the 
# total length of the segments, labeled correctly to the total duration of the song.
def evaluate_PCS(lrc_results, lrc_reference):
    total_words = len(lrc_reference);

    correct_duration = 0.0
    total_duration = lrc_reference[total_words-1].end - lrc_reference[0].start
    for i in range(total_words):
        correct_duration += max(0, min(lrc_reference[i].end,lrc_results[i].end) - max(lrc_reference[i].start, lrc_results[i].start))
        
    return correct_duration / total_duration


# Percentage of correct estimates according to a tolerance window 
# A metric that takes into consideration that the onset displacements from ground truth 
# below a certain threshold could be tolerated by human listeners. We use 0.3 seconds as 
# the tolerance window.
def evaluate_PCE(lrc_results, lrc_reference, tolerance = 0.3):
    # Error Handling
    total_words = len(lrc_reference);
    if len(lrc_results) != total_words:
        return 0.0
    
    correct_num = 0
    for i in range(total_words):
        if (abs(lrc_results[i].start - lrc_reference[i].start)) <= tolerance:
            correct_num += 1
        if (abs(lrc_results[i].end - lrc_reference[i].end)) <= tolerance:
            correct_num += 1
    return (0.5 * correct_num) / total_words


# Evalute all 4 
def MIREXevalute(lrc_results, lrc_reference):
    return evaluate_AAE(lrc_results, lrc_reference), evaluate_AAM(lrc_results, lrc_reference), \
        evaluate_PCS(lrc_results, lrc_reference), evaluate_PCE(lrc_results, lrc_reference)
