def read_prediction(prediction_file, prediction_path, sensitive_path):
    records = {}

    # with open(prediction_file, 'r', encoding='utf-8') as f:
        # # zapisujemy zawody
        # for line in f:
        #     # print(line)
        #     node1, edge, node2, score, pred_score = line.strip().split()
        #     score = int(float(score))
        #     pred_score = float(pred_score)
        #
        #     if edge != sensitive_path:  #jeśli nie znamy zawodu, to nie ma co oceniać
        #         continue
        #
        #     if node1 not in records.keys():
        #         records[node1] = {
        #             "node": node1,  #id
        #             "pred_label": None,    #płeć przewidziana (nie znamy jeszcze)
        #             "sensitive_score": pred_score,
        #             "pred_score": None,
        #             "true_label": None,     #płeć prawdziwa (nie znamy jeszcze)
        #             "sensitive_label": node2     #zawód
        #         }
        #     else:       #podmieniamy zawód, jeśli inny ma wyższy score
        #         if pred_score > records[node1]["sensitive_score"]:
        #             records[node1]["sensitive_label"] = node2
        #             records[node1]["sensitive_score"] = pred_score
        #
        # print(records)


    # zapisujemy zawody
    with open(prediction_file, 'r', encoding='utf-8') as f:
        for line in f:
            # print(line)
            node1, edge, node2, score, pred_score = line.strip().split()
            score = int(float(score))
            pred_score = float(pred_score)

            if edge != prediction_path:  #filtrujemy rekordy ze znanym zawodem
                continue

            if node1 not in records.keys():     #rozpoznajemy zawód po raz pierwszy
                # continue
                records[node1] = {
                    "node": node1,  #id
                    "pred_label": node2,    #przewidziany zawód
                    # "sensitive_score": pred_score,
                    "pred_score": pred_score,
                    "true_label": None,     #prawdziwy zawód (nie znamy jeszcze)
                    "sensitive_label": None  #prawdziwa płeć (nie znamy jeszcze)
                }
                if score == 1:
                    records[node1]["true_label"] = node2    #prawdziwy zawód
            # elif records[node1]["pred_label"] is None:  #jeśli to nasze pierwsze odgadywanie płci, to zapsujemy wyniki
            #     records[node1]["pred_label"] = node2
            #     records[node1]["pred_score"] = pred_score
            #     if score == 1:
            #         records[node1]["true_label"] = node2
            else:
                if pred_score > records[node1]["pred_score"]:      #jeśli mamy lepszy wynik przewidywania płci, to zamieniamy
                    records[node1]["pred_label"] = node2
                    records[node1]["pred_score"] = pred_score
                if score == 1:
                    records[node1]["true_label"] = node2

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

    for pred in predictions.keys():
        #uzupełniamy prawdziwe zawody
        if predictions[pred]["true_label"] is None:
            matches = set([line for line in all_data if pred in line and prediction_path in line])
            for match in matches:
                node1, edge, node2 = match.split()
                if node1 in predictions.keys():
                    predictions[node1]["true_label"] = node2

            if len(matches) == 0:
                # print("del", predictions[pred])
                if pred in updated_predictions.keys():
                    # print("del", pred)
                    del updated_predictions[pred]
        else:
            continue

    for pred in predictions.keys():
        #uzupełniamy płeć (tylko prawdziwą)
        if predictions[pred]["sensitive_label"] is None:
            matches = set([line for line in all_data if pred in line and sensitive_path in line])
            for match in matches:
                node1, edge, node2 = match.split()
                if node1 in predictions.keys():
                    predictions[node1]["sensitive_label"] = node2

            if len(matches) == 0:
                print("del", pred)
                if pred in updated_predictions.keys():
                    del updated_predictions[pred]
            else:
                print(matches)
        else:
            continue

    print(updated_predictions)
    return updated_predictions


    # Zbierz linie z pliku source_file, które zawierają wierzchołki z node_file
    # new_lines = []
    # with open(source_file, 'r', encoding='utf-8') as sf:
    #     for line in sf:
    #         parts = line.strip().split()
    #         if len(parts) == 3:
    #             node1, edge, node2 = parts
    #             if node1 in nodes or node2 in nodes:
    #                 new_lines.append(line)
    #                 edges.add(edge)
    #
    # # Dodajemy linie do pliku wynikowego
    # with open(extended_output_file, 'a', encoding='utf-8') as out:
    #     out.writelines(new_lines)

    # Zapisujemy unikalne krawędzie
    # with open(edge_output_file, 'w', encoding='utf-8') as ef:
    #     for edge in sorted(edges):
    #         ef.write(edge + '\n')


if __name__ == "__main__":
    # przewidujemy zawód i jeśli znamy prawdziwy, to go zapisujemy
    # tmp_prediction_dict = read_prediction(
    #     prediction_file='../person-data.txt',
    #     sensitive_path='/people/person/gender',
    #     prediction_path='/people/person/profession'
    # )
    # prediction_dict = read_sources(
    #     predictions=tmp_prediction_dict,
    #     source_folder="person-data",
    #     sensitive_path='/people/person/gender',
    #     prediction_path='/people/person/profession'
    # )

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

    print(prediction_dict.values())

    output_file = "person-data-output.txt"

    with open(output_file, 'w', encoding='utf-8') as out:
        for dict in prediction_dict.values():
            line = f'{dict["node"]} {dict["pred_label"]} {dict["true_label"]} {dict["sensitive_label"]}\n'
            # print(line)
            out.write(line)

