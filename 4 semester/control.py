def max_perimeter_triangle(A):
    # Проверка на количество элементов массива
    if len(A) < 3 or len(A) > 10000:
        raise ValueError("Длина массива должна быть от 3 до 10000.")
    
    # Проверка на диапазон значений элементов массива
    for a in A:
        if a < 1 or a > 10**6:
            raise ValueError("Значения элементов массива должны быть в диапазоне от 1 до 10^6.")
    
    # Сортировка массива в порядке убывания
    A.sort(reverse=True)
    
    # Проход по массиву
    for i in range(len(A) - 2):
        # Проверка условия треугольника
        if A[i] < A[i+1] + A[i+2]:
            # Если условие выполнено, возвращаем периметр
            return A[i] + A[i+1] + A[i+2]
    
    # Если не найдено подходящих сторон для треугольника
    return 0

# Примеры
try:
    print(max_perimeter_triangle([2, 1, 2]))  # Вывод: 5
    print(max_perimeter_triangle([1, 2, 1]))  # Вывод: 0
    print(max_perimeter_triangle([3, 2, 3, 4]))  # Вывод: 10
    print(max_perimeter_triangle([3, 6, 2, 3]))  # Вывод: 8

    #print(max_perimeter_triangle([3, 6, 2, 0])) #Error
    print(max_perimeter_triangle([3, 6])) 
except ValueError as e:
    print("Ошибка:", e)
