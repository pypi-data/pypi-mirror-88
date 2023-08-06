from numpy import round, int8


def group_predictions(prediction_list):
    group_list = []
    temp_group = []
    for pred in prediction_list:
        rounded_page_prediction = round(pred)
        if rounded_page_prediction == 0:
            temp_group.append(pred)
        elif rounded_page_prediction == 1:
            if len(temp_group) != 0:
                group_list.append(temp_group)
                del temp_group
                temp_group = []
            temp_group.append(pred)
        del rounded_page_prediction
    group_list.append(temp_group)
    return group_list


def round_predictions(prediction_list, decimals=0):
    if type(prediction_list[0]) == list:
        return [round(peca, decimals=decimals).tolist() for peca in prediction_list]
    else:
        if decimals == 0:
            return round(prediction_list, decimals=decimals).astype(int8).tolist()
        else:
            return round(prediction_list, decimals=decimals).tolist()

