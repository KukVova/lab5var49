#Варіант 49. Фармацевтичний склад
#Завдання 2. Стабільне сортування та відбір
from calculations3 import insertion_sort,report_value,report_matches,merge_sort,check_properties
def main():
    #n рядків код;назва;значення;кількість
    while True:
        try:
            n_input = input()
            n = int(n_input)
            if 0 <= n <= 20:
                break
            print("Помилка: n має бути в діапазоні від 0 до 20. Спробуйте знову.")
        except (ValueError, EOFError):
            print("Помилка: введіть ціле число. Спробуйте знову.")

    # limit (ціле число від 0 до 1000000)
    while True:
        try:
            limit_input = input()
            limit = int(limit_input)
            if 0 <= limit <= 1000000:
                break
            print("Помилка: limit має бути в діапазоні від 0 до 1000000. Спробуйте знову.")
        except (ValueError, EOFError):
            print("Помилка: введіть ціле число. Спробуйте знову.")

    records = []#порожній список
    for i in range(1, n + 1):#цикл який повторюється стільки разів скільки ми задали
        try:
            line = input().strip()# рядок
            if not line:
                continue
            parts = line.split(';')# рядок ділиться за допомогою ;
            #створення словника майже за такою ж схемою як я робив в прешому завданні
            if len(parts) != 4:
                continue
            code = int(parts[0])
            name = parts[1]
            value = int(parts[2])
            quantity = int(parts[3])
            records.append({
                'code': code,
                'name': name,
                'value': value,
                'quantity': quantity
            })
        except (EOFError, ValueError):
            break

    #Копія
    original_backup = [dict(r) for r in records]

    #Сортування
    sorted_insertion = insertion_sort(records)
    ins_codes = [r['code'] for r in sorted_insertion]

    sorted_merge = merge_sort(records)
    merge_codes = [r['code'] for r in sorted_merge]

    #Друк кодів після сортувань
    print("Вставками:", ", ".join(map(str, ins_codes)) if ins_codes else "немає")
    print("Злиттям:", ", ".join(map(str, merge_codes)) if merge_codes else "немає")

    #Збіг результатів
    results_match = "так" if ins_codes == merge_codes else "ні"
    print(f"Результати збігаються: {results_match}")

    #сортування вставками
    ins_order, ins_saved, ins_stab = check_properties(records, sorted_insertion)
    print(f"Вставки: порядок {ins_order}; записи {ins_saved}; стабільність {ins_stab}")

    #сортування злиттям
    merge_order, merge_saved, merge_stab = check_properties(records, sorted_merge)
    print(f"Злиттям: порядок {merge_order}; записи {merge_saved}; стабільність {merge_stab}")

    # Перевірка після сортувань
    input_preserved = "так" if records == original_backup else "ні"
    print(f"Початкові дані збережено: {input_preserved}")

    # Відбір записів
    selected = [r for r in sorted_merge if report_matches(r, limit)]

    print(f"Записи з показником більше {limit}:")
    #фільтрує відсортований список
    if selected:
        sum_indicators = 0
        for r in selected:
            ind = report_value(r)
            sum_indicators += ind
            print(f"{r['code']} | {r['name']} | {ind} міліграмів")
        print(f"Відібрано записів: {len(selected)}")
        print(f"Сума відібраних показників: {sum_indicators}")
    else:
        print("немає")
        print("Відібрано записів: 0")
        print("Сума відібраних показників: 0")


if __name__ == '__main__':
    main()
