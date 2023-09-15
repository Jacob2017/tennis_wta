from season import Season

def run_seasons(start,end=None):
    if end is None:
        end = start
    yr = start
    while yr <= end:
        s = Season(yr)
        s.run_year()
        yr += 1


if __name__ == "__main__":
    run_seasons(1990)