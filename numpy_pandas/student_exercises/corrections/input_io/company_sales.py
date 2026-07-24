import csv

import os

import pandas as pd
import matplotlib.pyplot as plt

CURRENT_DIR: str = os.path.dirname(os.path.realpath(__file__))


def read_sales_data() -> pd.DataFrame:
    """
    Reads the sales data from the "sales_data.csv" file.

    Arguments: None

    Returns:
    - sales_data (pd.DataFrame): Dataframe containing the sales with Amount as int
    """
    sales_path: str = os.path.join(CURRENT_DIR, "sales_data.csv")
    sales_data: pd.DataFrame = pd.read_csv(sales_path, index_col=0)
    return sales_data


def read_employee_data() -> pd.DataFrame:
    """
    Reads the employee data from the "employee_data.csv" file.

    Arguments: None

    Returns:
    - employee_data (pd.DataFrame): DataFrame of the dictionnaries with Salary as int
    """
    employee_path: str = os.path.join(CURRENT_DIR, "employee_data.csv")
    return pd.read_csv(employee_path, index_col=0)


def calculate_total_sales(sales_data: pd.DataFrame) -> int:
    """
    Calculates the total sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - total_sales (float): Total sales amount.
    """
    return sales_data.Amount.sum()


def calculate_average_sales(sales_data: pd.DataFrame) -> float:
    """
    Calculates the average sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - average_sales (float): Average sales amount.
    """
    return sales_data.Amount.mean()


def calculate_median_sales(sales_data: pd.DataFrame) -> float:
    """
    Calculates the median sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - median_sales (float): Median sales amount.
    """
    return sales_data.Amount.median()


def calculate_total_salary_expenses(employee_data: pd.DataFrame) -> int:
    """
    Calculates the total salary expenses.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - total_salary_expenses (float): Total salary expenses.
    """
    return employee_data.Salary.sum()


def calculate_average_salary(employee_data: pd.DataFrame) -> float:
    """
    Calculates the average salary.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - average_salary (float): Average salary.
    """
    return employee_data.Salary.mean()


def calculate_median_salary(employee_data: pd.DataFrame) -> float:
    """
    Calculates the median salary.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - median_salary (float): Median salary.
    """
    return employee_data.Salary.median()


def find_employee_with_highest_sales(
    sales_data: pd.DataFrame, employee_data: pd.DataFrame
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
    tot_emp: pd.Series = sales_data.groupby("EmployeeID").Amount.sum()
    max_emp_id: int = tot_emp.idxmax()
    max_emp: pd.Series = employee_data.loc[max_emp_id]
    return max_emp["Name"], max_emp["Department"]


def find_department_with_highest_sales(
    sales_data: pd.DataFrame, employee_data: pd.DataFrame
) -> str:
    """
    Finds the department with the total highest sales.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - department_name (str): Name of the department with the highest sales.
    """
    sales_data_new_index = sales_data.reset_index().set_index("EmployeeID")
    sales_join = sales_data_new_index.join(employee_data)
    return sales_join.groupby("Department").Amount.sum().idxmax()


def plot_sales_by_department(sales_data, employee_data):
    """
    Plots a bar chart showing the total sales by department.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.
    - employee_data (list): List of dictionaries representing employee data.

    Returns: None
    """
    sales_data_new_index = sales_data.reset_index().set_index("EmployeeID")
    sales_join = sales_data_new_index.join(employee_data)
    dep_tot: pd.Series = sales_join.groupby("Department").Amount.sum()

    # plt.bar(dep_tot.index, dep_tot)
    dep_tot.plot.bar()
    plt.show()
    


def plot_sales_vs_salary(sales_data, employee_data):
    """
    Plots a scatter plot showing the relationship between sales and salary.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.
    - employee_data (list): List of dictionaries representing employee data.

    Returns: None
    """
    sales_data_new_index = sales_data.reset_index().set_index("EmployeeID")
    sales_join = sales_data_new_index.join(employee_data).reset_index().set_index("SalesID")
    salary_tot: pd.Series = sales_join.groupby(["Salary", "Name"]).Amount.sum().reset_index()

    # plt.scatter(salary_tot.Salary, salary_tot.Amount)
    # plt.show()
    salary_tot.plot.scatter("Salary", "Amount")
    plt.show()
    #dep_tot: pd.Series = sales_join.groupby("Department").Amount.sum() 


def main():
    # Read sales data
    sales_data: pd.DataFrame = read_sales_data()

    # Read employee data
    employee_data: pd.DataFrame = read_employee_data()

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
    plot_sales_by_department(sales_data, employee_data)

    # Plot sales vs. salary
    plot_sales_vs_salary(sales_data, employee_data)


if __name__ == "__main__":
    main()
