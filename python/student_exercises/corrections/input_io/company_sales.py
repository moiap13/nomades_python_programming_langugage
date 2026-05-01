import csv

# import matplotlib.pyplot as plt
import os

from my_array import median, average

CURRENT_DIR: str = os.path.dirname(os.path.realpath(__file__))


def read_sales_data() -> list[dict[str, str | int]]:
    """
    Reads the sales data from the "sales_data.csv" file.

    Arguments: None

    Returns:
    - sales_data (list): List of dictionaries representing sales data.
    """
    sales_path: str = os.path.join(CURRENT_DIR, "sales_data.csv")
    sales_data: list[dict[str, str | int]] = []
    # Open the sales_data.csv file and return the list of dictionnary
    with open(sales_path, "r") as sales_csv_file:
        sales_reader = csv.DictReader(sales_csv_file)

        for sale in sales_reader:
            sale["Amount"] = int(sale["Amount"])
            sales_data.append(sale)
        
    return sales_data


def read_employee_data() -> list[dict[str, str | int]]:
    """
    Reads the employee data from the "employee_data.csv" file.

    Arguments: None

    Returns:
    - employee_data (list): List of dictionaries representing employee data.
    """
    employee_path: str = os.path.join(CURRENT_DIR, "employee_data.csv")
    employee_data: list[dict[str, str | int]] = []
    with open(employee_path) as employee_csv_file:
        employees_reader = csv.DictReader(employee_csv_file)

        for employee in employees_reader:
            employee["Salary"] = int(employee["Salary"])
            employee_data.append(employee) 
    return employee_data


def calculate_total_sales(sales_data: list[dict[str, str | int]]) -> float:
    """
    Calculates the total sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - total_sales (float): Total sales amount.
    """
    # total: float = 0.0
    # for sale in sales_data:
    #     total += sale["Amount"]
    # return total
    
    amounts: list[int] = [sale["Amount"] for sale in sales_data]
    return sum(amounts)    


def calculate_average_sales(sales_data: list[dict[str, str | int]]) -> float:
    """
    Calculates the average sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - average_sales (float): Average sales amount.
    """
    return calculate_total_sales(sales_data) / len(sales_data)


def calculate_median_sales(sales_data: list[dict[str, str | int]]) -> float:
    """
    Calculates the median sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - median_sales (float): Median sales amount.
    """
    # sorted_amounts: list[int] = sorted([sale["Amount"] for sale in sales_data])
    # mid: int = len(sorted_amounts) // 2
    # return (
    #     float(sorted_amounts[mid]) 
    #     if len(sorted_amounts) % 2 == 1 
    #     else (sorted_amounts[mid] + sorted_amounts[mid-1]) / 2
    # )
    return median([sale["Amount"] for sale in sales_data])



def calculate_total_salary_expenses(employee_data: list[dict[str, str | int]]) -> int:
    """
    Calculates the total salary expenses.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - total_salary_expenses (float): Total salary expenses.
    """
    return sum([employee["Salary"] for employee in employee_data]) 


def calculate_average_salary(employee_data: list[dict[str, str | int]]) -> float:
    """
    Calculates the average salary.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - average_salary (float): Average salary.
    """
    return average([employee["Salary"] for employee in employee_data])


def calculate_median_salary(employee_data: list[dict[str, str | int]]) -> float:
    """
    Calculates the median salary.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - median_salary (float): Median salary.
    """
    return median([employee["Salary"] for employee in employee_data])


def find_employee_with_highest_sales(
    sales_data: list[dict[str, str | int]], employee_data: list[dict[str, str | int]]
) -> tuple[str, str]:
    """
    Finds the employee with the highest total of sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - employee_name (str): Name of the employee with the highest sales amount.
    - department_name (str): Name of the department of the employee with the highest sales amount.
    """
    # 1. We compute the amount per employee
    employee_sale: dict[str, int] = {}
    for sale in sales_data:
        # if sale["EmployeeID"] in employee_sale:
        #     employee_sale[sale["EmployeeID"]] = employee_sale[sale["EmployeeID"]] + sale["Amount"]
        # else:
        #     employee_sale[sale["EmployeeID"]] = 0 + sale["Amount"]

        # employee_sale[sale["EmployeeID"]] = employee_sale.get(sale["EmployeeID"], 0) + sale["Amount"]

        if sale["EmployeeID"] not in employee_sale:
            employee_sale[sale["EmployeeID"]] = 0

        employee_sale[sale["EmployeeID"]] += sale["Amount"]
    
    # 2. find the employee with the highest sale amount
    max_id, max_amount = '', 0
    for employee_id, amount in employee_sale.items():
        if amount > max_amount:
            max_id = employee_id
            max_amount = amount

    # 3. Get the employee name and department of the max employee saler
    for employee in employee_data:
        if employee["EmployeeID"] == max_id:
            return employee["Name"], employee["Department"]
        
    # We should never come here
    return None, None


def find_department_with_highest_sales(
    sales_data: list[dict[str, str | int]], employee_data: list[dict[str, str | int]]
) -> str:
    """
    Finds the department with the total highest sales.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - department_name (str): Name of the department with the highest sales.
    """
    # 1. Create a map between employee id and employeee deparmtent
    employee_dep: dict[str, str] = {}
    for employee in employee_data:
        employee_dep[employee["EmployeeID"]] = employee["Department"]

    # 2. compute the sum per departement
    department_sale: dict[str, int] = {}
    for sale in sales_data:
        if employee_dep[sale["EmployeeID"]] not in department_sale:
            department_sale[employee_dep[sale["EmployeeID"]]] = 0
        department_sale[employee_dep[sale["EmployeeID"]]] += sale["Amount"]
    
    # 3. get the departemnet with the maximum sale amount
    max_dep, max_amount = '', 0
    for dep, amount in department_sale.items():
        if amount > max_amount:
            max_amount = amount
            max_dep = dep
    
    # 4. return the maximum departmenet name
    return max_dep
        


# def plot_sales_by_department(sales_data, employee_data):
#     """
#     Plots a bar chart showing the total sales by department.

#     Arguments:
#     - sales_data (list): List of dictionaries representing sales data.
#     - employee_data (list): List of dictionaries representing employee data.

#     Returns: None
#     """
#     pass


# def plot_sales_vs_salary(sales_data, employee_data):
#     """
#     Plots a scatter plot showing the relationship between sales and salary.

#     Arguments:
#     - sales_data (list): List of dictionaries representing sales data.
#     - employee_data (list): List of dictionaries representing employee data.

#     Returns: None
#     """
#     pass


def main():
    # Read sales data
    sales_data: list[dict[str, str | int]] = read_sales_data()

    # Read employee data
    employee_data: list[dict[str, str | int]] = read_employee_data()

    # Calculate total sales amount
    total_sales = calculate_total_sales(sales_data)
    print("Total Sales Amount:", total_sales)

    # Calculate average sales amount
    average_sales = calculate_average_sales(sales_data)
    print("Average Sales Amount:", average_sales)

    # Calculate median sales amount
    median_sales = calculate_median_sales(sales_data)
    print("Median Sales Amount:", median_sales)

    # Calculate total salary expenses
    total_salary_expenses = calculate_total_salary_expenses(employee_data)
    print("Total Salary Expenses:", total_salary_expenses)

    # Calculate average salary
    average_salary = calculate_average_salary(employee_data)
    print("Average Salary:", average_salary)

    # Calculate median salary
    median_salary = calculate_median_salary(employee_data)
    print("Median Salary:", median_salary)

    # Find the employee with the highest sales amount
    highest_sales_employee, highest_sales_employee_dep = (
        find_employee_with_highest_sales(sales_data, employee_data)
    )
    print(
        "Employee with Highest Sales Amount:",
        highest_sales_employee,
        highest_sales_employee_dep,
    )

    # Find the department with the highest sales
    highest_sales_department = find_department_with_highest_sales(
        sales_data, employee_data
    )
    print("Department with Highest Sales:", highest_sales_department)

    # Plot total sales by department
    # plot_sales_by_department(sales_data, employee_data)

    # Plot sales vs. salary
    # plot_sales_vs_salary(sales_data, employee_data)


if __name__ == "__main__":
    main()
