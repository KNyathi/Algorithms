import random


def generate_hotel_price():
    stars = random.randint(1, 5)  # Randomly generate stars (1 to 5)
    base_price = 50  # Base price for a 1-star hotel
    # Each star level has a different price range, ensuring higher stars have higher prices
    price_multiplier = random.uniform(1 + (stars - 1) * 0.5, 1 + stars * 0.5)  # Ensure higher stars have higher ranges
    price = base_price * stars * price_multiplier  # Price increases with stars and price_multiplier
    return round(price, 2)

def find_optimal_hotel(budget):
    observed_hotels = []  # List to track hotels observed during the exploration phase
    num_hotels_to_observe = int(0.3 * 100)  # It is difficult to give a proper number of hotels 
                                            # to observe here because they are infinite. We will stick to 30% 
                                            # of 100 hotels for the sake of observation
    hotel_counter = 0
    best_price = None  # Track the best price observed during the selection phase
    
    while True:
        hotel_price = generate_hotel_price()
        hotel_counter += 1
        
        # Check if hotel fits within the budget
        if hotel_price > budget:
            print(f"Hotel {hotel_counter}: Price ${hotel_price} exceeds your budget ${budget}. Moving on...")
            continue
        
        # Add to observed hotels during exploration phase
        if hotel_counter <= num_hotels_to_observe:
            observed_hotels.append(hotel_price)
            print(f"Hotel {hotel_counter}: Price ${hotel_price}. Observing during exploration phase...")
            continue
        
        # After the observation phase, choose the first hotel that is less than or equal to the observed minimum
        if best_price is None or hotel_price <= best_price:
            if observed_hotels:
                best_price = min(observed_hotels)
            else:
                best_price = float('inf')  # No observed hotels to compare against
       
        if hotel_price <= best_price:
            print(f"Hotel {hotel_counter}: Price ${hotel_price}. This is a deal equal to or better than observed minimum!")
            return hotel_price, observed_hotels
        
        continue


def calculate_success_rate(budget, num_runs=100, batch_size=5):
    successes = 0
    total_batches = 0
    
    for _ in range(num_runs):
        observed_hotels = []
        success = False
        
        while True:
            selected_price, observed_hotels = find_optimal_hotel(budget)
            
            # Calculate the observed minimum from observed_hotels
            if len(observed_hotels) > 0:
                optimal_price = min(observed_hotels)
            else:
                optimal_price = float('inf')
            
            # Check each batch of hotels
            batch_success = False
            for _ in range(batch_size):
                hotel_price = generate_hotel_price()
                if hotel_price <= optimal_price:
                    batch_success = True
                    break
            
            if batch_success:
                success = True
            
            total_batches += 1
            
            # Check if we have processed enough batches
            if total_batches % batch_size == 0:
                break
        
        if success:
            successes += 1

    # Success rate is the percentage of successful batches
    success_rate = (successes / (num_runs)) * 100
    return success_rate



budget = int(input("Enter your budget: "))
find_optimal_hotel(budget)  

success_rate = calculate_success_rate(budget)
print(f"Success rate of the algorithm: {success_rate}%")