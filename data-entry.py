"""
Ethan P. Gould
ethanpgould@gmail.com
"""
import unicodecsv

with open('sample1.csv', 'rb') as f1, open('sample2.csv', 'rb') as f2, \
    open('sample3.csv', 'rb') as f3, open('merge.csv', 'wb') as merge_file, \
    open('conflict.csv', 'wb') as conflict_file:
    # conveniently handles closing all the files again

    rdr1 = unicodecsv.reader(f1, encoding='utf-8-sig')
    rdr2 = unicodecsv.reader(f2, encoding='utf-8-sig')
    rdr3 = unicodecsv.reader(f3, encoding='utf-8-sig')
    file_list = [list(rdr1), list(rdr2), list(rdr3)]

    # get set of relevant labels from csv files
    label_set = set()
    for file in file_list:
        for row in file:
            label_set.add(row[0]) # assume first csv value is label

    # initialize some helpful containers with dict comprehesion
    merge_dict = {item : [] for item in label_set}
    conflict_val_dict = {item : set() for item in label_set}

    # create dictionary for final csv such that each value only occurs once
    for file in file_list:
        for row in file:
            for val in row[1:]:
                if val not in merge_dict[row[0]]:
                    merge_dict[row[0]].append(val)
                else: # a value in the row already on the platform
                    conflict_val_dict[row[0]].add(val)

    # get all the conflict_rows
    conflict_rows = []
    for file in file_list:
        for row in file:
            conflict = False
            for val in row[1:]:
                if val in conflict_val_dict[row[0]]:
                    conflict = True

            if conflict and row not in conflict_rows:
                conflict_rows.append(row)

    # write to merged.csv
    merge_writer = unicodecsv.writer(merge_file, encoding='utf-8-sig')
    for key in merge_dict.keys():
        entry = merge_dict[key]
        entry = [int(x) for x in entry if x != ''] # remove
        entry.sort()
        entry.insert(0, key)
        merge_writer.writerow(entry)

    # write to the conflicts conflict.csv
    conflict_writer = unicodecsv.writer(conflict_file, encoding='utf-8-sig')

    # filecount = 1 # uncomment to append source files
    for file in file_list:
        rowcount = 1
        for row in file:
            for val in row[1:]:
                if val in conflict_val_dict[row[0]]:
                    entry = [rowcount]
                    entry += [row[0],val]
                    # entry += ["sample"+str(filecount)+".csv"] # uncomment to append source files
                    conflict_writer.writerow(entry)
            rowcount += 1
        # filecount += 1 # uncomment to append source files
