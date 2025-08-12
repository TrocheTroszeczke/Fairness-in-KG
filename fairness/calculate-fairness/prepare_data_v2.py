import csv
import uuid


def read_prediction(prediction_file, prediction_path, sensitive_path):
    records = {}

    # zapisujemy zawody
    with open(prediction_file, 'r', encoding='utf-8') as f:
        for line in f:
            node1, edge, node2, score, pred_score = line.strip().split()
            score = int(float(score))
            pred_score = float(pred_score)

            if edge != prediction_path:  #filtrujemy rekordy ze znanym zawodem
                continue

            if node1 not in records.keys():     #rozpoznajemy zawód po raz pierwszy
                id = str(uuid.uuid4())
                records[id] = {
                    "node": node1,  #id
                    "pred_label": node2,    #przewidziany zawód
                    "pred_score": pred_score,
                    "true_label": None,     #prawdziwy zawód (nie znamy jeszcze)
                    "sensitive_label": None  #prawdziwa płeć (nie znamy jeszcze)
                }
                if score == 1:
                    records[id]["true_label"] = node2    #prawdziwy zawód

        print(records)
    return records

def read_sources(predictions, source_folder, sensitive_path, prediction_path):

    updated_predictions = predictions.copy()

    with open(f'..\\..\\data\\{source_folder}\\train.txt', 'r', encoding='utf-8') as f_data, \
        open(f'..\\..\\data\\{source_folder}\\test.txt', 'r', encoding='utf-8') as f_data_test, \
        open(f'..\\..\\data\\{source_folder}\\valid.txt', 'r', encoding='utf-8') as f_data_valid, \
        open(f'..\\..\\data\\{source_folder}_ind\\train.txt', 'r', encoding='utf-8') as f_data_ind, \
        open(f'..\\..\\data\\{source_folder}_ind\\test.txt', 'r', encoding='utf-8') as f_data_ind_test, \
        open(f'..\\..\\data\\{source_folder}_ind\\valid.txt', 'r', encoding='utf-8') as f_data_ind_valid:

        data = f_data.readlines()
        data_test = f_data_test.readlines()
        data_valid = f_data_valid.readlines()
        data_ind = f_data_ind.readlines()
        data_ind_test = f_data_ind_test.readlines()
        data_ind_valid = f_data_ind_valid.readlines()

        all_data = data + data_test + data_valid + data_ind + data_ind_valid + data_ind_test

    for id in predictions.keys():
        pred = predictions[id]["node"]
        #uzupełniamy prawdziwe zawody
        if predictions[id]["true_label"] is None:
            matches = set([line for line in all_data if pred in line and prediction_path in line])
            for match in matches:
                node1, edge, node2 = match.split()
                # if node1 in predictions.keys():
                #     predictions[node1]["true_label"] = node2
                for other_id, other_record in predictions.items():
                    if other_record["node"] == node1 and other_record["true_label"] is None:
                        predictions[other_id]["true_label"] = node2

            if len(matches) == 0:
                if id in updated_predictions.keys():
                    del updated_predictions[id]
        else:
            continue

    for id in predictions.keys():
        pred = predictions[id]['node']
        #uzupełniamy płeć (tylko prawdziwą)
        if predictions[id]["sensitive_label"] is None:
            matches = set([line for line in all_data if pred in line and sensitive_path in line])
            for match in matches:
                node1, edge, node2 = match.split()
                # if node1 in predictions.keys():
                #     predictions[node1]["sensitive_label"] = node2
                for other_id, other_record in predictions.items():
                    if other_record["node"] == node1 and other_record["sensitive_label"] is None:
                        predictions[other_id]["sensitive_label"] = node2

            if len(matches) == 0:
                print("del", pred)
                if id in updated_predictions.keys():
                    del updated_predictions[id]
            else:
                print(matches)
        else:
            continue

    print(updated_predictions)
    return updated_predictions

if __name__ == "__main__":
    # przewidujemy zawód i jeśli znamy prawdziwy, to go zapisujemy
    tmp_prediction_dict = read_prediction(
        prediction_file='../person-data.txt',
        sensitive_path='/people/person/nationality',
        prediction_path='/people/person/profession'
    )
    prediction_dict = read_sources(
        predictions=tmp_prediction_dict,
        source_folder="person-data",
        sensitive_path='/people/person/nationality',
        prediction_path='/people/person/profession'
    )

    # tmp_prediction_dict = read_prediction(
    #     prediction_file='../person-data.txt',
    #     sensitive_path='/people/person/nationality',
    #     prediction_path='/people/person/profession'
    # )
    # prediction_dict = read_sources(
    #     predictions=tmp_prediction_dict,
    #     source_folder="person-data",
    #     sensitive_path='/people/person/nationality',
    #     prediction_path='/people/person/profession'
    # )

    print(prediction_dict.values())

    # output_file = "{file}-{sensitive}-{prediction}.csv"
    output_file = "person-data-nationality-profession-v2.csv"

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        row = ["id", "predicted_label", "true_label", "sensitive_label", "score"]
        writer.writerow(row)
        for d in prediction_dict.values():
            row = [d["node"], d["pred_label"], d["true_label"], d["sensitive_label"], d["pred_score"]]
            writer.writerow(row)
