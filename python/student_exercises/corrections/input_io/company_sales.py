import csv
# import matplotlib.pyplot as plt
# conda install matplotlib
import os
from functools import reduce

CURRENT_DIR: str = os.path.dirname(os.path.realpath(__file__))

def read_sales_data() -> list[dict[str, str|int]]:
    """
    Reads the sales data from the "sales_data.csv" file.

    Arguments: None

    Returns:
    - sales_data (list): List of dictionaries representing sales data.
    """
    sales_path: str = os.path.join(CURRENT_DIR, "sales_data.csv")
    sales_data: list[dict[str, str | int]] = []

    with open(sales_path, "r", encoding="utf-8") as sales_csv_file:
        reader = csv.DictReader(sales_csv_file)
        for row in reader:
            row["Amount"] = int(row["Amount"])
            sales_data.append(row)
    return sales_data


def read_employee_data() -> list[dict[str, str|float|int]]:
    """
    Reads the employee data from the "employee_data.csv" file.

    Arguments: None

    Returns:
    - employee_data (list): List of dictionaries representing employee data.
    """
    employee_path: str = os.path.join(CURRENT_DIR, "employee_data.csv")
    employee_data: list[dict[str, str | int]] = []
    
    with open(employee_path, "r", encoding="utf-8") as employee_csv_file:
        reader = csv.DictReader(employee_csv_file)
        for row in reader:
            row["Salary"] = int(row["Salary"])
            employee_data.append(row)
    return employee_data


def calculate_total_sales(sales_data: list[dict[str, str|int]]) -> int:
    """
    Calculates the total sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - total_sales (float): Total sales amount.
    """
    # total: int = 0
    # for dct_sale in sales_data:
    #     total += dct_sale["Amount"] # total = total + dct_sale["Amount"]
    # return total

    # return sum([dct_sale["Amount"] for dct_sale in sales_data])

    # def reduce_sum(pv, cv):
    #     return pv + cv["Amount"]
    # return reduce(reduce_sum, sales_data, 0)
    return reduce(lambda pv, cv: pv + cv["Amount"], sales_data, 0)

        


def calculate_average_sales(sales_data: list[dict[str, str|int]]) -> float:
    """
    Calculates the average sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - average_sales (float): Average sales amount.
    """
    return calculate_total_sales(sales_data) / len(sales_data)

def calculate_median_sales(sales_data: list[dict[str, str|int]]):
    """
    Calculates the median sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - median_sales (float): Median sales amount.
    """
    amounts: list[int] = sorted([sale_dct["Amount"] for sale_dct in sales_data])
    mid: int = len(amounts) // 2
    return amounts[mid] if len(amounts)%2==1 else (amounts[mid-1] + amounts[mid])/2

def calculate_total_salary_expenses(employee_data):
    """
    Calculates the total salary expenses.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - total_salary_expenses (float): Total salary expenses.
    """
    return reduce(lambda pv, cv: pv + cv["Salary"], employee_data, 0)


def calculate_average_salary(employee_data):
    """
    Calculates the average salary.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - average_salary (float): Average salary.
    """
    return calculate_total_salary_expenses(employee_data) / len(employee_data)

def calculate_median_salary(employee_data):
    """
    Calculates the median salary.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - median_salary (float): Median salary.
    """
    salaries: list[int] = sorted([sale_dct["Salary"] for sale_dct in employee_data])
    mid: int = len(salaries) // 2
    return salaries[mid] if len(salaries)%2==1 else (salaries[mid-1] + salaries[mid])/2


def find_employee_with_highest_sales(sales_data, employee_data) -> tuple[str, str]:
    """
    Finds the employee with the highest sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - employee_name (str): Name of the employee with the highest sales amount.
    - department_name (str): Name of the department of the employee with the highest sales amount.
    """
    # employee_total: dict[str, int] = {}
    # for sale_dct in sales_data:
    #     if sale_dct["EmployeeID"] in employee_total:
    #         employee_total[sale_dct["EmployeeID"]] += sale_dct["Amount"]
    #     else:
    #         employee_total[sale_dct["EmployeeID"]] = sale_dct["Amount"]

    # max_amount: int = 10e-100
    # max_id: str = ''

    # for employee_id, total_sales_emp in employee_total.items():
    #     if total_sales_emp > max_amount:
    #         max_amount = total_sales_emp
    #         max_id = employee_id
    
    # for employee in employee_data:
    #     if employee["EmployeeID"] == max_id:
    #         return employee["Name"], employee["Department"]






    employee_total: dict[str, int] = {}
    # for sale_dct in sales_data:
    #     if sale_dct["EmployeeID"] not in employee_total:
    #         employee_total[sale_dct["EmployeeID"]] = 0

    #     employee_total[sale_dct["EmployeeID"]] += sale_dct["Amount"] 
    for sale_dct in sales_data:
        employee_total[sale_dct["EmployeeID"]] = employee_total.get(sale_dct["EmployeeID"], 0) + sale_dct["Amount"]  

    # max_amount: int = 10e-100
    # max_id: str = ''

    # for employee_id, total_sales_emp in employee_total.items():
    #     if total_sales_emp > max_amount:
    #         max_amount = total_sales_emp
    #         max_id = employee_id

    max_id: str = max(employee_total, key=lambda employee_id: employee_total[employee_id])

    # for employee in employee_data:
    #     if employee["EmployeeID"] == max_id:
    #         return employee["Name"], employee["Department"]
            
    employee: dict[str, str | int] = employee_data[int(max_id)-1]
    return employee["Name"], employee["Department"]
    
        
        

def find_department_with_highest_sales(sales_data, employee_data):
    """
    Finds the department with the highest sales.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - department_name (str): Name of the department with the highest sales.
    """
    user_dep: dict[str, str] = {}
    for emp_dct in employee_data:
        user_dep[emp_dct["EmployeeID"]] = emp_dct["Department"]
    
    total_dep_sales: dict[str, int] = {}
    for sale_dct in sales_data:
        user_department: str = user_dep[sale_dct["EmployeeID"]]
        if user_department in total_dep_sales:
            total_dep_sales[user_department] += sale_dct["Amount"]
        else:
            total_dep_sales[user_department] = sale_dct["Amount"]
    
    max_total: int = -(10e-100)
    max_dep: str = ""

    for dep, dep_total_sales in total_dep_sales.items():
        if dep_total_sales > max_total:
            max_total = dep_total_sales
            max_dep = dep
    
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
    highest_sales_employee, highest_sales_employee_dep = find_employee_with_highest_sales(sales_data, employee_data)
    print("Employee with Highest Sales Amount:", highest_sales_employee, highest_sales_employee_dep)

    # Find the department with the highest sales
    highest_sales_department = find_department_with_highest_sales(sales_data, employee_data)
    print("Department with Highest Sales:", highest_sales_department)

    # Plot total sales by department
    # plot_sales_by_department(sales_data, employee_data)

    # Plot sales vs. salary
    # plot_sales_vs_salary(sales_data, employee_data)


if __name__ == '__main__':
    main()
    # d = {"Italy": "Rome", "England": "London", "Germany": "Berlin"}
    # for item in d:
    #     print(item)