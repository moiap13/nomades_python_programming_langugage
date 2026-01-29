import csv

# import matplotlib.pyplot as plt
import os

CURRENT_DIR: str = os.path.dirname(os.path.realpath(__file__))

int_values: list[str] = ["Amount", "Salary"]


def read_sales_data() -> list[dict[str, str | int]]:
    """
    Reads the sales data from the "sales_data.csv" file.

    Arguments: None

    Returns:
    - sales_data (list): List of dictionaries representing sales data.
    """
    sales_path: str = os.path.join(CURRENT_DIR, "sales_data.csv")
    sales_data: list[dict[str, str | int]] = []

    with open(sales_path) as sales_csv:
        reader = csv.reader(sales_csv)
        header: list[str] = next(reader)

        # Open the sales_data.csv file and return the list of dictionnary
        for row in reader:
            dict_row_data: dict[str, str | int] = {}
            for idx, column_name in enumerate(header):
                dict_row_data[column_name] = (
                    row[idx] if column_name not in int_values else int(row[idx])
                )
            sales_data.append(dict_row_data)

    return sales_data


def read_employee_data() -> list[dict[str, str | int]]:
    """
    Reads the employee data from the "employee_data.csv" file.

    Arguments: None

    Returns:
    - employee_data (list): List of dictionaries representing employee data.
    """
    employee_path: str = os.path.join(CURRENT_DIR, "employee_data.csv")
    employee_data = []

    with open(employee_path) as employee_csv:
        reader = csv.DictReader(employee_csv)

        for row in reader:
            # for key in row.keys(): # O(n)
            #     if key in int_values: # O(m)
            #         row[key] = int(row[key])
            for int_value in int_values:
                if int_value in row:
                    row[int_value] = int(row[int_value])
            employee_data.append(row)

    return employee_data


def calculate_total_sales(sales_data: list[dict[str, str | int]]) -> int:
    """
    Calculates the total sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - total_sales (int): Total sales amount.
    """
    # total: int = 0
    # for sale in sales_data:
    #     total += sale["Amount"]

    # return total

    # amounts: list[int] = []
    # for sale in sales_data:
    #     amounts.append(sale["Amount"])
    # return sum(amounts)

    return sum([sale["Amount"] for sale in sales_data])


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
    amounts: list[int] = [
        sale["Amount"] for sale in sales_data
    ]  # list[dict[str, str | int]] -> list[int]

    # amounts.sort() # inplace
    sorted_amounts: list[int] = sorted(amounts)  # return a new sorted list
    mid: int = len(sorted_amounts) // 2
    return (
        float(sorted_amounts[mid])
        if len(sorted_amounts) % 2 == 1
        else (sorted_amounts[mid] + sorted_amounts[mid - 1]) / 2
    )


def calculate_total_salary_expenses(employee_data: list[dict[str, str | int]]) -> int:
    """
    Calculates the total salary expenses.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - total_salary_expenses (float): Total salary expenses.
    """
    from functools import reduce

    salaries: list[int] = [employee["Salary"] for employee in employee_data]
    return reduce(lambda total_salary, salary: total_salary + salary, salaries, 0)
    max_ = reduce(
        lambda max_salary, current_salary: (
            current_salary if current_salary > max_salary else max_salary
        ),
        salaries,
        salaries[0],
    )
    return max_


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
    employee_sorted: list[dict] = sorted(
        employee_data, key=lambda employee_dict: employee_dict["Salary"]
    )
    n: int = len(employee_sorted)
    mid: int = n // 2
    return (
        float(employee_sorted[mid]["Salary"])
        if n % 2 == 1
        else (employee_sorted[mid]["Salary"] + employee_sorted[mid - 1]["Salary"]) / 2
    )


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
    # 1. counted the total sales per employee id
    total_sale_per_employee_id: dict[str, int] = {}
    for sale in sales_data:
        total_sale_per_employee_id[sale["EmployeeID"]] = (
            total_sale_per_employee_id.get(sale["EmployeeID"], 0) + sale["Amount"]
        )

    # 2. find the employee id with the highest sales
    emp_id: str = max(
        total_sale_per_employee_id,
        key=lambda emp_id: total_sale_per_employee_id[emp_id],
    )

    # 3. given the employee id find the employee name and department
    for employee in employee_data:
        if employee["EmployeeID"] == emp_id:
            return employee["Name"], employee["Department"]


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
    # 1. created a dict with employee id as key and department as value
    emp_dep: dict[str, str] = {}
    for employee in employee_data:
        emp_dep[employee["EmployeeID"]] = employee["Department"]

    # 2. counted the total sales per department, given the dictionary created in step 1
    sales_per_dep: dict[str, int] = {}
    for sale in sales_data:
        sales_per_dep[emp_dep[sale["EmployeeID"]]] = (
            sales_per_dep.get(emp_dep[sale["EmployeeID"]], 0) + sale["Amount"]
        )

    # 3. find the department with the highest sales
    return max(sales_per_dep, key=sales_per_dep.get)

    dep_max: str = ""
    max_total: int = -1e100

    for dep, total in sales_per_dep.items():
        if total > max_total:
            max_total = total
            dep_max = dep

    return dep_max


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
