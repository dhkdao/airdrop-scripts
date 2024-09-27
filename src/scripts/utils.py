def round_number(val):
    if isinstance(val, float):
        if val < 1:  # keep 4 decimals
            return round(val, 4)
        if val < 100:  # keep 3 decimals
            return round(val, 3)
        else:  # keep 2 decimals
            return round(val, 2)
    return val


def round_output(df):
    for label, col_data in df.items():
        df[label] = col_data.apply(round_number)
    return df


def is_number(i):
    return isinstance(i, (int, float))
