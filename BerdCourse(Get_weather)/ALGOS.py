


# def quicksort(arr):
#     if len(arr) <= 1:
#         return arr  # Базовый случай: массив уже отсортирован
#
#     pivot = arr[len(arr) // 2]  # Выбираем опорный элемент (середина)
#
#     left = [x for x in arr if x < pivot]  # Элементы меньше опорного
#     middle = [x for x in arr if x == pivot]  # Элементы равные опорному
#     right = [x for x in arr if x > pivot]  # Элементы больше опорного
#
#     return quicksort(left) + middle + quicksort(right)  # Рекурсивно сортируем и объединяем
#
#
# # Пример использования:
# arr = [10, 3, 5, 8, 2, 9, 4]
# sorted_arr = quicksort(arr)
# print(sorted_arr)

def hruifr(lst):
    write_index = 0  # Указатель, куда записывать

    for read_index in range(len(lst)):
        if read_index == 0 or not (lst[read_index] == " " and lst[read_index - 1] == " "):
            lst[write_index] = lst[read_index]
            write_index += 1  # Двигаем указатель записи

    # Удаляем лишние элементы в конце списка
    del lst[write_index:]

    return lst

print(hruifr(["А", " ", " ", "В", "А", " ", " "]))



# class Solution:
#     def twoSum(self, nums, target):
#         dict_1 = {}
#
#         for i, num in enumerate(nums):
#             num_2 = target - num
#             if num_2 in dict_1:
#                 return [num_2, num]
#             dict_1[num] = i
#
# test_1 = Solution()
# print(test_1.twoSum([2, 7, 11, 15], 9))


# def isSubsequence(s, t):
#     point_1, point_2 = 0, 0
#
#     for point_2 in range(len(t)):
#         if s[point_1] == t[point_2]:
#             point_1 += 1
#
#         if point_1 == len(s):
#             return True
#     return False
#
# print(isSubsequence("abc", "ahbgdc"))


# def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
#     """
#     Do not return anything, modify nums1 in-place instead.
#     """
#     merged = []  # Новый список для объединенного результата
#     i, j = 0, 0  # Два указателя
#
#     # Пока оба массива не закончились
#     while i < m and j < n:
#         if nums1[i] < nums2[j]:
#             merged.append(nums1[i])
#             i += 1
#         else:
#             merged.append(nums2[j])
#             j += 1
#
#     # Добавляем оставшиеся элементы из nums1, если есть
#     while i < m:
#         merged.append(nums1[i])
#         i += 1
#
#     # Добавляем оставшиеся элементы из nums2, если есть
#     while j < n:
#         merged.append(nums2[j])
#         j += 1
#
#     return merged
#
# print(merge([1,2,3,0,0,0], 3, [2,5,6], 3))


# def rjrjgriij(a: list):
#     left = 0
#
#     for right in range(len(a)):
#         if a[right] == ' ' and a[right - 1] == ' ':
#             continue
#         a[left] = a[right]
#         left += 1
#     del a[left:]
#     return a
#
#
# print(rjrjgriij(['A', ' ', ' ', 'B',' ', ' ', ' ', 'B']))


# clean = ''.join(i.lower() for i in s if i.isalnum())
#
# return clean == clean[::-1]


# def containsDuplicate(nums: list[int]) -> bool:
#     dict_1 = {}
#
#     for num in nums:
#         dict_1[num] = dict_1.get(num, 0) + 1
#
#     return dict_1
#
# print(containsDuplicate([1,2,3,1]))


# def merge(nums1, m, nums2, n):
#     """
#     Do not return anything, modify nums1 in-place instead.
#     """
#     merged = []  # Новый список для объединенного результата
#     i, j = 0, 0  # Два указателя
#
#     # Пока оба массива не закончились
#     while i < m and j < n:
#         if nums1[i] < nums2[j]:
#             merged.append(nums1[i])
#             i += 1
#         else:
#             merged.append(nums2[j])
#             j += 1
#
#     # Добавляем оставшиеся элементы из nums1, если есть
#     while i < m:
#         merged.append(nums1[i])
#         i += 1
#
#     # Добавляем оставшиеся элементы из nums2, если есть
#     while j < n:
#         merged.append(nums2[j])
#         j += 1
#
#     return merged  # Возвращаем новый массив (nums1 не изменяем)
#
#
# print(merge([1,2,3,0,0,0], 3, [2,5,8], 3))


# def mySqrt(x: int) -> int:
#     left, right = 0, x
#     result = 0
#
#     while left <= right:
#         mid = (left + right) // 2
#         if mid * mid <= x:
#             result = mid
#             left += 1
#         else:
#             right += 1
#     return result
#
# print(mySqrt(9))

# def isIsomorphic(s: str, t: str) -> bool:
#     dict_1 = {}
#     for num1 in s:
#         dict_1[num1] = dict_1.get(num1, 0) + 1
#
#     dict_2 = {}
#     for num2 in t:
#         dict_2[num2] = dict_2.get(num2, 0) + 1
#
#     if dict_1[num1] == dict_2[num2]:
#         return True
#
#     return False
#
# print(isIsomorphic("bbbaaaba", "aaabbbba"))



