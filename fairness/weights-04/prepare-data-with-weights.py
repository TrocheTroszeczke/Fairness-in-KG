import csv

def read_sources(source_file, source_folder, sensitive_path, prediction_path):

    output = []
    sensDict = {}
    predDict = {}

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

    with open(source_file) as sf:
        for line in sf:
            node1, edge, node2 = line.split()
            output.append(line)

            # if edge == sensitive_path:
            #     sensDict[node1] = node2
            if edge == prediction_path:
                predDict[node1] = node2
        print(predDict)

    sens_data = set([line for line in all_data if sensitive_path in line])
    print(sens_data)

    for line in sens_data:
        node1, edge, node2 = line.split()
        if node1 in predDict.keys():
            sensDict[node1] = node2
    print(sensDict)

    for person in sensDict.keys():
        # if person in predDict.keys():
        output.append(f'{person}\t{prediction_path}\t{predDict[person]}\n')

    return output


if __name__ == "__main__":
    dataWithWeights = read_sources(
        source_file="..\\..\\data\\person-data_ind\\test.txt",
        source_folder="person-data",
        sensitive_path='/people/person/nationality',
        prediction_path='/people/person/profession'
    )

    # print(dataWithWeights)

    # # output_file = "{file}-{sensitive}-{prediction}.csv"
    output_file = "..\\..\\data\\person-data-weights_ind\\test.txt"

    with open(output_file, "w") as f:
        for item in dataWithWeights:
            f.write(f"{item}")
