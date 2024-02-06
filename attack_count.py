if __name__ == "__main__":
    node_set = set()
    # result_path = "./result/label_1-3.txt"
    result_path = "./result/label_1-4.txt"
    with open(result_path, "r") as file:
    # with open("./attack_data/125.txt", "r") as file:
        for line in file:
            details = line.split("\t")
            node_set.add(details[0])
            node_set.add(details[2])
    print(len(node_set))