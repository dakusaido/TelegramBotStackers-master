def rank_counter(test_points, max_test, active_points, max_active):
    active_k = 1  # коэффициент увеличения активности
    test_k = 1  # коэффициент увеличения тестов

    if (0 <= active_points / max_active < 0.3):
        test_k = 1
    if (0.3 <= active_points / max_active < 0.6):
        test_k = 1.3
    if (0.6 <= active_points / max_active < 0.8):
        test_k = 1.6
    if (0.8 <= active_points / max_active <= 1):
        test_k = 2

    if (0 <= test_points / max_test < 0.3):
        active_k = 1
    if (0.3 <= test_points / max_test < 0.6):
        active_k = 1.5
    if (0.6 <= test_points / max_test < 0.8):
        active_k = 2
    if (0.8 <= test_points / max_test <= 1):
        active_k = 3

    rank_points = test_k * test_points + (active_k * active_points) / 20

    return rank_points


print("Rank points is:", rank_counter(1, 1000, 100, 1000))
