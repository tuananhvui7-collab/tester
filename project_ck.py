# Improved get_user_input with better error handling
def get_user_input_improved():
  stock_id = None
  quantity = None
  price = None
  list_stock = []
  try:
    for i in range(5):
      stock_id = input(f"Enter the stock Id for entry {i+1}: ")
      try:
        quantity = int(input(f"Enter the quantity for {stock_id}: "))
      except ValueError:
        print("Invalid input for quantity. Please enter a number.")
        continue # Skip to the next iteration
      try:
        price = float(input(f"Enter the price for {stock_id}: "))
      except ValueError:
        print("Invalid input for price. Please enter a number.")
        continue # Skip to the next iteration

      # Check for missing data after successful conversion
      if not stock_id or quantity is None or price is None:
        print("Don't miss data.")
        continue # Skip to the next iteration
      else:
        # If all inputs are valid, add to the list
        print(f"Valid input for entry {i+1}: Stock ID: {stock_id}, Quantity: {quantity}, Price: {price}")
        list_stock.append([stock_id, quantity, price])

  except Exception as e:
    print(f"An unexpected error occurred: {e}")

  # Return the list of valid stock entries
  return list_stock

# Calculate sum of money invest
def cal_sum(list_stock):
  total_sum = 0
  for row in list_stock:
    # Ensure quantity and price are numbers before multiplying
    if isinstance(row[1], (int, float)) and isinstance(row[2], (int, float)):
      total_sum += row[1] * row[2]
    else:
      print(f"Warning: Skipping entry with invalid quantity or price: {row}")
  return total_sum

#Find Stock_id have the max value
def find_max(list_stock):
  max_value = 0
  max_stock_id = None # Initialize max_stock_id
  if not list_stock: # Handle empty list case
      return None, 0

  for row in list_stock:
    # Ensure quantity and price are numbers before multiplying
    if isinstance(row[1], (int, float)) and isinstance(row[2], (int, float)):
      total_in_one = row[1] * row[2]
      if total_in_one > max_value:
        max_value = total_in_one
        max_stock_id = row[0]
    else:
      print(f"Warning: Skipping entry with invalid quantity or price for max calculation: {row}")

  return max_stock_id, max_value


# Save into the file
def save_to_file(list_stock):
  file_path = "/content/investment.txt" # Explicit file path
  try:
    with open(file_path,"w+") as f:
      for i in list_stock:
        f.write(f"Mã:{i[0]} - Số lượng: {i[1]} - giá mua: {i[2]} - tổng đầu tư: {i[1] *  i[2]}\n") # Added newline character
      print(f"Dữ liệu đã được lưu vào tệp: {file_path}") # Confirmation message
  except Exception as e:
    print(f"Đã xảy ra lỗi khi lưu tệp: {e}")

def read_file(file_path):
  try:
    with open(file_path,"r") as f:
      lines = f.readlines()
  except FileNotFoundError:
    print(f"File not found {file_path}")
    lines = []

  invest_data = []
  for line in lines:
    try:
      parts = line.strip().split(" - ")

      stock_id = parts[0].split(":")[1].strip()
      quantity = int(parts[1].split(":")[1].strip())
      price = float(parts[2].split(":")[1].strip())
      total_investment_in_one = float(parts[3].split(":")[1].strip())
      invest_entry = {
          "stock_id": stock_id,
          "quantity": quantity,
          "price": price,
          "total_investment_in_one": total_investment_in_one
      }
      invest_data.append(invest_entry)
    except (IndexError, ValueError) as e:
      print(f"Skipping malformed line:{line.strip()} - Error:{e}")
  total = 0
  for entry in invest_data:
    total += entry["total_investment_in_one"]

  count_above_5m = 0
  for entry in invest_data:
    if entry["total_investment_in_one"] > 5000000:
      count_above_5m += 1
  
  print(f"Tổng đầu tư: {total}")
  print(f"Số mã có tổng đầu tư trên 5 triệu: {count_above_5m}")

# Get input from the user
file_path = "/content/investment.txt"
stock_data = get_user_input_improved()

# Calculate and print the total investment
total_investment = cal_sum(stock_data)
print(f"\nTotal invest: {total_investment}")

# Find and print the stock with the maximum value
max_stock_id, max_investment = find_max(stock_data)

if max_stock_id:
    print(f"Stock_ID max: {max_stock_id}, value: {max_investment}")
else:
    print("NO valid data to calculate.")

# Call the save_to_file function with the collected data
save_to_file(stock_data)

# Last request
read_file(file_path)