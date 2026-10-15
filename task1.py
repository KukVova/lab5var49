#Варіант 49. Фармацевтичний склад
#Завдання 1. Перевірка записів і пошук за кодом
from calculations3 import value_record,linear_search,binary_search

def main():
    # n рядків код;назва;значення;кількість
    while True:
        try:
            n_input = input()
            n = int(n_input)
            if 0 <= n <= 20:
                break
            print("Помилка: n має бути в діапазоні від 0 до 20. Спробуйте знову.")
        except (ValueError, EOFError):
            print("Помилка: введіть ціле число. Спробуйте знову.")

    #q кодів запиту
    while True:
        try:
            q_input = input()
            q = int(q_input)
            if 1 <= q <= 10:
                break
            print("Помилка: q має бути в діапазоні від 1 до 10. Спробуйте знову.")
        except (ValueError, EOFError):
            print("Помилка: введіть ціле число. Спробуйте знову.")

    rejections = []#відхилені запити
    accepted = []#прийняті запити
    existing_codes = set()

    for i in range(1, n + 1):# цикл який закидує всі записані дані в value_record де вже вони будуть як раз розкидуватися до прийняті і відхилені
        try:
            line = input()
        except EOFError:
            break

        res = value_record(line, existing_codes, i)#ось тут як раз закидує
        if isinstance(res, str):#перевірка на те чи є результат текстом бо якщо так то запит буде відхилено а якщо ні то то воно буде повертати словник з функції value_record
            rejections.append(res)
        else:
            accepted.append(res)
            existing_codes.add(res['code'])

    queries = []#запроси
    for _ in range(q):# ми задаємо кількість повтору
        try:
            queries.append(int(input()))#кожен новий рядок який ми вписуємо
        except (EOFError, ValueError):
            queries.append(0)#якщо буде помилка то код продовжеться

    #цикл для перевірки кожного рядку в відхилинях
    for rej in rejections:
        print(rej)
    #результат
    print(f"Прийнято записів: {len(accepted)}")
    print(f"Відхилено записів: {len(rejections)}")

    sorted_codes = sorted([r['code'] for r in accepted])#сортує за зростанням, а r['code'] бере як раз число зі словника яке вже збережено в словник після проходження перевірки на помилки
    if sorted_codes:
        print("Коди за зростанням:", ", ".join(map(str, sorted_codes)))#числа стають рядками а потім пишуться разом через пробіли та коми
    else:
        print("Коди за зростанням: немає")

    sorted_records_by_code = sorted(accepted, key=lambda x: x['code'])#інша копія прийнятих запитів для бінарного пошуку за завданням

    #цикл який бере число для запиту
    for query in queries:
        print(f"Запит: {query}")
#при використанні r я кожен раз звертаюся до value_record тим самим беру всі дані з словника
        lin_idx, lin_checked = linear_search(accepted, query)# звертання до лінарного пошуку
        if lin_idx is not None:#чи вщагалі щось є
            r = accepted[lin_idx]
            total_indicator = r['value'] * r['quantity']# для знаходження маси кожної одиниці
            print(
                f"Лінійний: {r['code']} | {r['name']} | {r['value']} міліграмів | {r['quantity']} од. | {total_indicator} міліграмів; переглянуто: {lin_checked}")
        else:
            print(f"Лінійний: немає; переглянуто: {lin_checked}")
#тут все робиться теж саме що і для лінійного пошуку
        bin_idx, bin_checked = binary_search(sorted_records_by_code, query)
        if bin_idx is not None:
            r = sorted_records_by_code[bin_idx]
            total_indicator = r['value'] * r['quantity']
            print(
                f"Бінарний: {r['code']} | {r['name']} | {r['value']} міліграмів | {r['quantity']} од. | {total_indicator} міліграмів; переглянуто: {bin_checked}")
        else:
            print(f"Бінарний: немає; переглянуто: {bin_checked}")
#тут перевіряється як раз збіг результатів
        if lin_idx is not None and bin_idx is not None:
            match_str = "так" if accepted[lin_idx]['code'] == sorted_records_by_code[bin_idx]['code'] else "ні"
        elif lin_idx is None and bin_idx is None:
            match_str = "так"
        else:
            match_str = "ні"

        print(f"Результати збігаються: {match_str}")


if __name__ == '__main__':
    main()
