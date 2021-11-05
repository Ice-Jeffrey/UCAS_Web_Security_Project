import pickle

FILE_NAME = 'csdn'
# FILE_NAME = 'yahoo'


def getRule(line):
    indexes = []
    for char in line:  
        if char >= '0' and char <= '9':
            char_index = 'D'
        elif (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z'):
            char_index  = 'L'
        else:
            char_index = 'S'
        indexes.append(char_index)

    # generate rule
    # 123ab32a -> [(D, 3), (L, 2), (D, 2), (L, 1), frequency]
    rule = []
    current = indexes[0]
    count = 0
    indexes.append('\n')
    string = ''
    for index in indexes:
        if index == current:
            count += 1
        else:
            rule.append((current, count))
            string += current + str(count)
            current, count = index, 1
    
    return rule, string
    

def main():
    with open('../data/data_' + FILE_NAME + '.pkl', 'rb') as f:
        lines = pickle.load(f)[0]

    rule_lib = {}
    for line in lines:
        rule, key = getRule(line)
        rule_lib[key] = rule_lib.get(key, 0) + 1
    sorted_list = sorted(rule_lib.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)

    rules = []
    for item in sorted_list:
        rule = list(item[0])
        rule.append(item[1] / len(lines))
        rules.append(rule)
    # print(rules[:5])

    with open('./results/' + FILE_NAME + '_rules.pkl', 'wb') as f:
        pickle.dump(rules, f, pickle.HIGHEST_PROTOCOL)
    f.close()

    # rule = getRule('123ab32a')
    # print(rule)


if __name__ == "__main__":
    main()
