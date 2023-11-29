from random import randint

'''test_list :list = []
for i in range(25):
    k = randint(5,60)
    i += 1
    test_list.append(k)'''

#test_list = [randint(5, 60) for i in range(8)]

test_list = [8, 11, 6, 5, 3]
def quick_sort(list):
    if len(list) < 2:
        return list

    low, same, high = [], [], []
    pivot = list[randint(0, len(list)-1)]

    for item in list:
        if item == pivot:
            same.append(item)
        elif item < pivot:
            low.append(item)
        elif item > pivot:
            high.append(item)

    return quick_sort(low)+same+quick_sort(high)

if __name__ == "__main__":
    sorted_list = quick_sort(test_list)
    print(sorted_list)


