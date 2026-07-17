import csv

# import matplotlib.pyplot as plt
import os

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
        reader = csv.DictReader(sales_csv_file)
        for row in reader:
            row["Amount"] = int(row["Amount"])
            sales_data.append(row)
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
    # Open the sales_data.csv file and return the list of dictionnary
    with open(employee_path, "r") as employee_csv_file:
        reader = csv.DictReader(employee_csv_file)
        for row in reader:
            row["Salary"] = int(row["Salary"])
            employee_data.append(row)
    return employee_data


def calculate_total_sales(sales_data: list[dict[str, str | int]]) -> int:
    """
    Calculates the total sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - total_sales (float): Total sales amount.
    """
    # sum_: int = 0
    # for sale_dict in sales_data:
    #     sum_ += sale_dict["Amount"]
    # return sum_

    l: list[int] = [sale_dict["Amount"] for sale_dict in sales_data]
    return sum(l)


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
    sales_amout_sorted: list[int] = sorted([sale_dict["Amount"] for sale_dict in sales_data])
    mid: int = len(sales_amout_sorted) // 2

    if len(sales_amout_sorted) % 2 == 1:
        return float(sales_amout_sorted[mid])

    return (sales_amout_sorted[mid-1] + sales_amout_sorted[mid]) / 2


def calculate_total_salary_expenses(employee_data: list[dict[str, str | int]]) -> int:
    """
    Calculates the total salary expenses.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - total_salary_expenses (float): Total salary expenses.
    """
    return sum([emp_dict["Salary"] for emp_dict in employee_data])


def calculate_average_salary(employee_data: list[dict[str, str | int]]) -> float:
    """
    Calculates the average salary.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - average_salary (float): Average salary.
    """
    return calculate_total_salary_expenses(employee_data) / len(employee_data)


def calculate_median_salary(employee_data: list[dict[str, str | int]]) -> float:
    """
    Calculates the median salary.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - median_salary (float): Median salary.
    """
    import statistics

    return float(statistics.median([emp_dict["Salary"] for emp_dict in employee_data]))


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
    # emp_amount: dict[str, int] = {
    #     emp_id: sum([sd["Amount"] for sd in sales_data if sd["EmployeeID"] == emp_id]) 
    #     for emp_id in list(set([sd["EmployeeID"] for sd in sales_data]))
    # }
    # print(emp_amount)

    emp_amount: dict[str, int] = {}

    # for sale_dict in sales_data:
    #     if sale_dict["EmployeeID"] not in emp_amount:
    #         emp_amount[sale_dict["EmployeeID"]] = 0

    #     emp_amount[sale_dict["EmployeeID"]] += sale_dict["Amount"]
    
    # for sale_dict in sales_data:
    #     if sale_dict["EmployeeID"] in emp_amount:
    #         emp_amount[sale_dict["EmployeeID"]] += sale_dict["Amount"]
    #     else:
    #         emp_amount[sale_dict["EmployeeID"]] = sale_dict["Amount"]
    

    for sale_dict in sales_data:
        emp_amount[sale_dict["EmployeeID"]] = emp_amount.get(sale_dict["EmployeeID"], 0) + sale_dict["Amount"]
    # print(emp_amount)

    # max_emp, max_amount = '', 0

    # for emp_id, amount in emp_amount.items():
    #     if amount > max_amount:
    #         max_emp = emp_id
    #         max_amount = amount

    # max_emp = max(emp_amount, key=lambda emp_id: emp_amount[emp_id])
    max_emp = max(emp_amount, key=emp_amount.get)

    for emp_dict in employee_data:
        if emp_dict["EmployeeID"] == max_emp:
            return emp_dict["Name"], emp_dict["Department"]
    
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
    emp_dep: dict[str, str] = {emp_dict["EmployeeID"]: emp_dict["Department"] for emp_dict in employee_data}
    # print(emp_dep)

    dep_amount: dict[str, int] = {}
    for sale_dict in sales_data:
        employee_dep: str = emp_dep[sale_dict["EmployeeID"]]

        if employee_dep not in dep_amount:
            dep_amount[employee_dep] = 0
        dep_amount[employee_dep] += sale_dict["Amount"]


    return max(dep_amount, key=lambda department_name: dep_amount[department_name])

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
