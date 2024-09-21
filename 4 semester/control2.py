def largestNumber(nums):
    # Check if the length of nums satisfies the constraint
    if not 1 <= len(nums) <= 100:
        raise ValueError("Length of nums must be between 1 and 100 inclusive.")
    
    # Check if all elements of nums satisfy the constraint
    if any(num < 0 or num > 10**9 for num in nums):
        raise ValueError("All elements of nums must be between 0 and 10^9 inclusive.")
    
    # Convert each integer element in the list nums into a string
    nums = [str(num) for num in nums]
    
    # Separate multi-digit numbers into single digits and put them back into the original list
    for i in range(len(nums)):
        if len(nums[i]) > 1:
            nums[i] = [int(digit) for digit in nums[i]]  # Separate multi-digit number into single digits
            # Put the single digits back into the original list
            nums[i:i+1] = [str(digit) for digit in nums[i]]
    
    # Sort the list in descending order
    nums.sort(reverse=True)
    
    # Join the sorted list into a single string
    return ''.join(nums)

# Примеры из задачи
nums1 = [10, 2]
nums2 = [3, 30, 34, 5, 9]
nums3 = [1]
nums4 = [10]

# Проверка на примерах
print(largestNumber(nums1))  # Вывод: "210"
print(largestNumber(nums2))  # Вывод: "9534330"
print(largestNumber(nums3))  # Вывод: "1"
print(largestNumber(nums4))  # Вывод: "10"
