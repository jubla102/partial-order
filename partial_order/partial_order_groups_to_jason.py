from partial_order_grouping import get_partial_order_group_sequences


def write_json_file():
    partial_order_groups_main = get_partial_order_group_sequences()
    for i in range(0, len(partial_order_groups_main)):
        print(partial_order_groups_main[i])


if __name__ == '__main__':
    write_json_file()
