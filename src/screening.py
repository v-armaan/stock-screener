def apply_condition(df, metric, operator, value): #to check if one condition passes

    latest = df.iloc[-1]
    if isinstance(value, str):
        value = latest[value]

    if operator == ">":
        return latest[metric] > value

    elif operator == "<":
        return latest[metric] < value

    elif operator == ">=":
        return latest[metric] >= value

    elif operator == "<=":
        return latest[metric] <= value

    elif operator == "==":
        return latest[metric] == value

    elif operator == "!=":
        return latest[metric] != value

    else:
        raise ValueError("Invalid operator")

def screen_stock(df, conditions):   #to check whether all the conditions pass

    for metric, operator, value in conditions:

        if not apply_condition(df, metric, operator, value):
            return False

    return True
