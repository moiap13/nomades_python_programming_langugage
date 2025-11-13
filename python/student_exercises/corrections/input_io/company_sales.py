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

    with open(sales_path, "r") as sales_file:
        reader = csv.DictReader(sales_file)
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
    employees_path: str = os.path.join(CURRENT_DIR, "employee_data.csv")
    with open(employees_path, "r") as employees_file:
        employee_data: list[dict[str, str | int]] = [
            row | {"Salary": int(row["Salary"])}
            for row in csv.DictReader(employees_file)
        ]
    return employee_data


def calculate_total_sales(sales_data: list[dict[str, str | int]]) -> int:
    """
    Calculates the total sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - total_sales (float): Total sales amount.
    """
    # total: int = 0
    # for sale in sales_data:
    #     amount = sale.get("Amount")
    #     total += amount
    # return total

    return sum([sale.get("Amount") for sale in sales_data])


def calculate_average_sales(sales_data: list[dict[str, str | int]]):
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
    res: list[int] = sorted([sale.get("Amount") for sale in sales_data])
    mid: int = len(res) // 2
    return (res[mid] + res[(mid) - 1]) / 2 if len(res) % 2 == 0 else float(res[mid])


def calculate_total_salary_expenses(employee_data: list[dict[str, str | int]]):
    """
    Calculates the total salary expenses.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - total_salary_expenses (float): Total salary expenses.
    """
    return sum([employee["Salary"] for employee in employee_data])


def calculate_average_salary(employee_data: list[dict[str, str | int]]):
    """
    Calculates the average salary.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - average_salary (float): Average salary.
    """
    return calculate_total_salary_expenses(employee_data) / len(employee_data)


def calculate_median_salary(employee_data: list[dict[str, str | int]]):
    """
    Calculates the median salary.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - median_salary (float): Median salary.
    """
    import statistics

    return statistics.median([employee["Salary"] for employee in employee_data])


def find_employee_with_highest_sales(
    sales_data: list[dict[str, str | int]], employee_data: list[dict[str, str | int]]
):
    """
    Finds the employee with the highest total of sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - employee_name (str): Name of the employee with the highest sales amount.
    - department_name (str): Name of the department of the employee with the highest sales amount.
    """
    max_sale: float = 0.0
    max_emp: dict = {"Name": None, "Department": None}

    for employee in employee_data:
        employee["total_sales"] = 0
        for sale in sales_data:
            if sale["EmployeeID"] == employee["EmployeeID"]:
                employee["total_sales"] += float(sale["Amount"])

        if employee["total_sales"] > max_sale:
            max_sale = employee["total_sales"]
            max_emp = employee

    return max_emp["Name"], max_emp["Department"]


def find_department_with_highest_sales(
    sales_data: list[dict[str, str | int]], employee_data: list[dict[str, str | int]]
):
    """
    Finds the department with the total highest sales.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - department_name (str): Name of the department with the highest sales.
    """
    emp_dep: dict[str, str] = {}
    for employee in employee_data:
        emp_dep[employee["EmployeeID"]] = employee["Department"]

    dep_amouts: dict[str, int] = {}
    for sale in sales_data:
        employee_department: str = emp_dep[sale["EmployeeID"]]
        if employee_department not in dep_amouts:
            dep_amouts[employee_department] = 0

        dep_amouts[employee_department] += sale["Amount"]

    # max_amount: int = 0
    # max_dep: str = ""
    # for dep, amount in dep_amouts.items():
    #     if amount > max_amount:
    #         max_amount = amount
    #         max_dep = dep

    # return max_dep

    return max(dep_amouts, key=lambda dep: dep_amouts[dep])
    return max(dep_amouts, key=dep_amouts.get)


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
    total_sales: int = calculate_total_sales(sales_data)
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
