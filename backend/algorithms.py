"""
algorithms.py
Contains core DAA (Design and Analysis of Algorithms) implementations:
1. Quick Sort (Sorting by Price)
2. Merge Sort (Sorting by Year/Mileage)
3. Greedy Algorithm (Best Value Recommendations)
"""

def quick_sort(arr, key, reverse=False):
    """
    Quick Sort Algorithm
    Time Complexity: 
        - Average: O(n log n)
        - Worst: O(n^2) (happens if pivot selection is poor, though we use midpoint)
    Space Complexity: O(log n) for recursion stack
    
    Why Quick Sort?
    - Efficient in-place sorting for large datasets.
    - Faster in practice than many other O(n log n) algorithms for car listing data.
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2][key]
    left = [x for x in arr if x[key] < pivot]
    middle = [x for x in arr if x[key] == pivot]
    right = [x for x in arr if x[key] > pivot]
    
    if reverse:
        return quick_sort(right, key, reverse) + middle + quick_sort(left, key, reverse)
    else:
        return quick_sort(left, key, reverse) + middle + quick_sort(right, key, reverse)

def merge_sort(arr, key, reverse=False):
    """
    Merge Sort Algorithm
    Time Complexity: O(n log n) - Guaranteed performance regardless of input distribution.
    Space Complexity: O(n) - Requires extra space for merging.
    
    Why Merge Sort?
    - Stable sorting algorithm (preserves relative order of equal elements).
    - Useful when sorting by year or mileage where multiple cars might have the same value.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key, reverse)
    right = merge_sort(arr[mid:], key, reverse)

    return merge(left, right, key, reverse)

def merge(left, right, key, reverse):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        condition = left[i][key] > right[j][key] if reverse else left[i][key] < right[j][key]
        if condition:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def get_best_value_cars(cars, budget, top_n=3):
    """
    Greedy Algorithm for Car Recommendations
    Objective: Maximize 'Value' = (Year_Factor + Condition_Factor) / Price
    Year_Factor = (Year - Min_Year) / (Max_Year - Min_Year)
    
    Time Complexity: O(n log n) - primarily due to sorting by value density.
    Space Complexity: O(n) to store value scores.
    
    Logic:
    - We calculate a 'Value Score' for each car.
    - We sort cars by this score in descending order.
    - We greedily pick the top cars that fit within the budget.
    """
    if not cars:
        return []

    # Simple value scoring logic
    scored_cars = []
    for car in cars:
        if car['price'] <= 0: continue
        
        # Condition numeric mapping
        cond_map = {'Excellent': 1.0, 'Good': 0.8, 'Fair': 0.5, 'Poor': 0.2}
        condition_score = cond_map.get(car['condition'], 0.5)
        
        # Value = Year (newer better) * Condition / Price
        # Normalizing year slightly (e.g., relative to 2000)
        year_score = (car['year'] - 2000) / 25 if car['year'] > 2000 else 0.1
        value_score = (year_score + condition_score) * 10000 / car['price']
        
        # Create a dict-like object for easier access if it's a sqlite3.Row
        car_dict = dict(car)
        car_dict['value_score'] = value_score
        scored_cars.append(car_dict)

    # Sort by value_score descending
    # Using our custom quick_sort here to demonstrate integration
    sorted_cars = quick_sort(scored_cars, 'value_score', reverse=True)
    
    # Greedy selection within budget
    recommendations = []
    current_budget = budget
    for car in sorted_cars:
        if car['price'] <= current_budget:
            recommendations.append(car)
            current_budget -= car['price'] # Optional: if we want a "set" of cars, but usually just top list
            if len(recommendations) >= top_n:
                break
                
    return recommendations

def binary_search_price_range(arr, min_price, max_price):
    """
    Binary Search Implementation
    Time Complexity: O(log n) to find boundaries in a sorted list.
    Space Complexity: O(1)
    
    Why Binary Search?
    - Extremely efficient for searching in sorted datasets. 
    - Demonstrates 'Divide and Conquer' logic in search.
    """
    if not arr:
        return []
        
    # Find first index where price >= min_price
    left_idx = find_boundary(arr, min_price, True)
    # Find last index where price <= max_price
    right_idx = find_boundary(arr, max_price, False)
    
    if left_idx == -1 or right_idx == -1 or left_idx > right_idx:
        return []
        
    return arr[left_idx:right_idx + 1]

def find_boundary(arr, target, is_lower_bound):
    low = 0
    high = len(arr) - 1
    abs_idx = -1
    
    while low <= high:
        mid = (low + high) // 2
        if is_lower_bound:
            if arr[mid]['price'] >= target:
                abs_idx = mid
                high = mid - 1
            else:
                low = mid + 1
        else:
            if arr[mid]['price'] <= target:
                abs_idx = mid
                low = mid + 1
            else:
                high = mid - 1
    return abs_idx
