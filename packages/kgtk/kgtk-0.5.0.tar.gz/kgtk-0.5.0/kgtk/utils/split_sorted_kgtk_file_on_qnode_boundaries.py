def split_kgtk_edge_file(f_path: str, output_path: str, file_prefix: str = 'split', split_lines_number: int = 100000):
    f = open(f_path)

    prev = None
    lines_to_write = list()
    file_number = 0

    first_line = f.readline().replace('\n', '').replace('\r', '')
    columns = first_line.split('\t')
    node1_index = columns.index("node1")
    for line in f:
        vals = line.split('\t')
        node = vals[node1_index]
        if node.startswith('Q') or node.startswith('P'):
            if prev is None:
                prev = node

            if not prev.strip() == node.strip():
                prev = node
                if len(lines_to_write) >= split_lines_number:
                    o = open(f'{output_path}/{file_prefix}_{file_number}.tsv', 'w')
                    o.write(f'{first_line}\n')

                    o.write('\n'.join(lines_to_write))

                    lines_to_write = list()
                    file_number += 1

            lines_to_write.append(line.replace('\n', '').replace('\r', ''))

    if len(lines_to_write) > 0:
        o = open(f'{output_path}/{file_prefix}_{file_number}.tsv', 'w')
        o.write(f'{first_line}\n')
        o.write('\n'.join(lines_to_write))

        lines_to_write = list()
        file_number += 1
    print('Done')


split_kgtk_edge_file('/Users/amandeep/Documents/kgtk/2020-08-03/wikidata_sample.tsv', '/tmp/test_split',
                     split_lines_number=1000)
