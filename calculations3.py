#Завдання 1. Перевірка записів і пошук за кодом
#перевірка умов завдання
def value_record(line, existing_codes, record_num):
    """

    """
    parts = line.strip().split(';')
    if len(parts) != 4:#якщо частин вводу менше чим 4 то запис теж відхиляється
        return f"Запис {record_num}: відхилено (недопустимі значення)"

    try:
        code = int(parts[0])#перетворюю на цілі числа
        name = parts[1]
        value = int(parts[2])#перетворюю на цілі числа
        quantity = int(parts[3])#перетворюю на цілі числа
        #якщо введеться текст то запис відхилиться
    except ValueError:
        return f"Запис {record_num}: відхилено (недопустимі значення)"
    if not (1 <= code <= 9999):
        return f"Запис {record_num}: відхилено (недопустимі значення)"    # Код від 1 до 9999.

    if not (1 <= len(name) <= 40) or ';' in name or name != name.strip():# Назва має 1-40 символів, не містить ';', не має крайових пробілів
        return f"Запис {record_num}: відхилено (недопустимі значення)"

    if not (0 <= value <= 100000) or not (0 <= quantity <= 100):
        return f"Запис {record_num}: відхилено (недопустимі значення)" # Маса  від 0 до 100000 міліграмів, кількість упаковок від 0 до 100

    # Перевірка на повтор коду
    if code in existing_codes:
        return f"Запис {record_num}: відхилено (повтор коду {code})"

    return {#якщо все пройшло успішно то повертає словник
        'code': code,
        'name': name,
        'value': value,
        'quantity': quantity
    }

#для початкового списку прийнятих записів( по завданню)
#умова (Лічильники починаються знуля для кожного виклику; порожній список дає (None, 0))
def linear_search(records, code):
    if not records:
        return None, 0

    best_idx = None
    min_diff = float('inf')
    best_code = -1
    checked = 0
    #перевірка всього списку
    for i, rec in enumerate(records):
        checked += 1
        diff = abs(rec['code'] - code)

        if diff < min_diff or (diff == min_diff and rec['code'] > best_code):#знаходження наймешої різниці
            min_diff = diff
            best_idx = i
            best_code = rec['code']

    return best_idx, checked

#для окремої копії за зростанням коду(по завданню)
def binary_search(records, code):
    if not records:
        return None, 0

    left = 0
    right = len(records) - 1
    checked = 0

    best_idx = None
    min_diff = float('inf')
    best_code = -1

    while left <= right:#по завданню
        mid = (left + right) // 2
        checked += 1
        rec = records[mid]
        diff = abs(rec['code'] - code)
        #ідеальний збіг або нічого
        if diff < min_diff or (diff == min_diff and rec['code'] > best_code):
            min_diff = diff
            best_idx = mid
            best_code = rec['code']

        if rec['code'] == code:
            break
        elif rec['code'] < code:
            left = mid + 1
        else:
            right = mid - 1

    return best_idx, checked
#Завдання 2. Стабільне сортування та відбір
def sort_key(record):
    return record['value'] * record['quantity']#за завданням


def report_value(record):
    return sort_key(record)#цілий показник


def report_matches(record, limit):#результат перевірки
    return sort_key(record) > limit# за завданням

#insertion_sort and merge_sort, повертають нові списки навіть для 0 і 1 запису, не змінюють порядок і поля вхідних записів.
def insertion_sort(records):
    #копія щоб не змінювати оригінальні дані, як і першому завданні(так само робив для бінарного пошуку)
    arr = list(records)
    for i in range(1, len(arr)):
        key_item = arr[i]
        key_val = sort_key(key_item)
        j = i - 1
        # Сортування за спаданням
        while j >= 0 and sort_key(arr[j]) < key_val:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item
    return arr

# Рекрусивне злиття. За це відповідає дві функції перша розбиває список навпіл потім сортує цей список і потім сортується за допомогою додаткової функції злиття
def merge_sort(records):
    #якщо список як раз містить 0 або 1 елемент він вже відсортований
    if len(records) <= 1:
        return list(records)
    #знаходить середину та ділить список на дві частини
    mid = len(records) // 2
    left = merge_sort(records[:mid])
    right = merge_sort(records[mid:])
    #Зливаються відсортовані половинки
    return merge(left, right)


def merge(left, right):#допоміжне злиття
    result = []
    i = j = 0
    # Для сортування за спаданням
    while i < len(left) and j < len(right):
        if sort_key(left[i]) >= sort_key(right[j]):#стабільність
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    # залишки
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Ця функція буде робити правильний порядок ключів, зберігати всі записи і стабілізувати(за завданням)
def check_properties(original, sorted_arr):
    #Правильний порядок ключів за спаданням
    correct_order = "так"
    for i in range(len(sorted_arr) - 1):
        if sort_key(sorted_arr[i]) < sort_key(sorted_arr[i + 1]):
            correct_order = "ні"
            break

    # Збереження всіх записів
    if len(sorted_arr) != len(original):
        all_saved = "ні"
    else:
        # Перевірка на те чи не втрачено коди або назви. Повторюю метод із першого завдання звертаючись до словника
        orig_counts = {}
        for r in original:
            orig_counts[(r['code'], r['name'], r['value'], r['quantity'])] = orig_counts.get((r['code'], r['name'], r['value'], r['quantity']), 0) + 1

        sort_counts = {}
        for r in sorted_arr:
            sort_counts[(r['code'], r['name'], r['value'], r['quantity'])] = sort_counts.get((r['code'], r['name'], r['value'], r['quantity']), 0) + 1

        all_saved = "так" if orig_counts == sort_counts else "ні"

    #Стабільність
    stability = "так"
    for i in range(len(sorted_arr)):
        for j in range(i + 1, len(sorted_arr)):
            # Якщо ключі однакові, перевіряємо їхній початковий порядок
            if sort_key(sorted_arr[i]) == sort_key(sorted_arr[j]):
                # Знаходимо індекси в оригінальному списку
                try:
                    idx_i = original.index(sorted_arr[i])
                    # Шукаємо наступний однаковий елемент для другого
                    idx_j = original.index(sorted_arr[j], idx_i + 1 if sorted_arr[i] == sorted_arr[j] else 0)
                    if idx_i > idx_j:
                        stability = "ні"
                except ValueError:
                    stability = "ні"

    return correct_order, all_saved, stability