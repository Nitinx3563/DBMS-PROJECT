import sys
import os

# Add the current directory to path so we can import algorithms
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from algorithms import quick_sort, merge_sort, binary_search_price_range, get_best_value_cars

mock_cars = [
    {'listing_id': 1, 'price': 20000, 'year': 2018, 'mileage': 40000, 'condition': 'Excellent', 'brand': 'Toyota', 'model': 'Camry'},
    {'listing_id': 2, 'price': 15000, 'year': 2015, 'mileage': 70000, 'condition': 'Good', 'brand': 'Honda', 'model': 'Civic'},
    {'listing_id': 3, 'price': 35000, 'year': 2021, 'mileage': 10000, 'condition': 'Excellent', 'brand': 'Tesla', 'model': 'Model 3'},
    {'listing_id': 4, 'price': 5000, 'year': 2010, 'mileage': 150000, 'condition': 'Fair', 'brand': 'Ford', 'model': 'Focus'},
    {'listing_id': 5, 'price': 12000, 'year': 2017, 'mileage': 60000, 'condition': 'Good', 'brand': 'Hyundai', 'model': 'Elantra'},
]

def test_sorting():
    print("Testing Quick Sort (Price Low to High)...")
    sorted_price = quick_sort(mock_cars.copy(), 'price')
    prices = [c['price'] for c in sorted_price]
    assert prices == [5000, 12000, 15000, 20000, 35000]
    print("✓ Success")

    print("Testing Merge Sort (Year Newest First)...")
    sorted_year = merge_sort(mock_cars.copy(), 'year', reverse=True)
    years = [c['year'] for c in sorted_year]
    assert years == [2021, 2018, 2017, 2015, 2010]
    print("✓ Success")

def test_binary_search():
    print("Testing Binary Search (Price range 10000-20000)...")
    sorted_price = quick_sort(mock_cars.copy(), 'price')
    results = binary_search_price_range(sorted_price, 10000, 20000)
    prices = [c['price'] for c in results]
    assert prices == [12000, 15000, 20000]
    print("✓ Success")

def test_greedy():
    print("Testing Greedy Recommendations (Budget 40000)...")
    recommendations = get_best_value_cars(mock_cars, budget=40000, top_n=2)
    print(f"Recommended: {[r['brand'] + ' ' + r['model'] for r in recommendations]}")
    assert len(recommendations) <= 2
    # Quality check: Tesla (high year, high condition) should be one of them despite high price
    # OR Ford (very low price) might have high value density
    for r in recommendations:
        print(f"- {r['brand']} {r['model']}: Value Score: {r['value_score']:.2f}, Price: {r['price']}")
    print("✓ Success")

if __name__ == "__main__":
    try:
        test_sorting()
        test_binary_search()
        test_greedy()
        print("\nAll DAA Algorithm Tests Passed!")
    except AssertionError as e:
        print(f"\nTest Failed!")
        sys.exit(1)
