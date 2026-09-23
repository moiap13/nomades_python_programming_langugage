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
    employee_data: pd.DataFrame = pd.read_csv(os.path.join(CURRENT_DIR, "employee_data.csv"), index_col=0)
    return employee_data


def calculate_total_sales(sales_data: pd.DataFrame) -> int:
    """
    Calculates the total sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - total_sales (int): Total sales amount.
    """
    total_sales: int = sales_data.Amount.sum()
    return total_sales


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
    Finds the employee with the lowest total of sales amount .

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - employee_name (str): Name of the employee with the highest sales amount.
    - department_name (str): Name of the department of the employee with the highest sales amount.
    """
    sum_per_employee: pd.Series = sales_data.groupby("EmployeeID")["Amount"].sum()
    id_max_employee: int = sum_per_employee.idxmax()
    max_employee: pd.Series = employee_data.loc[id_max_employee]
    return max_employee["Name"], max_employee["Department"]


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
    # emp_dep: dict[int, str] = {}
    # for idx, emp in employee_data.iterrows():
    #     emp_dep[idx] = emp["Department"]

    # departements: pd.Series = sales_data["EmployeeID"].map(lambda id_emp: emp_dep[id_emp])
    # sales_data["Department"] = departements
    # sales_per_department: pd.Series = sales_data.groupby("Department")["Amount"].sum()
    # return sales_per_department.idxmax()

    # departements: pd.Series = sales_data["EmployeeID"].map(lambda id_emp: employee_data.loc[id_emp, "Department"])
    # sales_data["Department"] = departements
    # sales_per_department: pd.Series = sales_data.groupby("Department")["Amount"].sum()
    # return sales_per_department.idxmax()
    
    sales_emp_indexed: pd.DataFrame = sales_data.set_index("EmployeeID")
    merged_df: pd.DataFrame = sales_emp_indexed.join(employee_data)
    sales_per_department: pd.Series = merged_df.groupby("Department")["Amount"].sum()
    return sales_per_department.idxmax()


def plot_sales_by_department(sales_data, employee_data):
    """
    Plots a bar chart showing the total sales by department.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.
    - employee_data (list): List of dictionaries representing employee data.

    Returns: None
    """
    departements: pd.Series = sales_data["EmployeeID"].map(lambda id_emp: employee_data.loc[id_emp, "Department"])
    sales_data["Department"] = departements
    sales_per_department: pd.Series = (sales_data
                                       .groupby("Department")["Amount"]
                                       .sum()
                                       .sort_values(ascending=False))

    sales_per_department.plot.bar()

    # plt.bar(sales_per_department.index, sales_per_department.values)

    # plt.xlabel("Departments")
    # plt.ylabel("Sales")
    # plt.title("Sales per departments")

    plt.savefig(os.path.join(CURRENT_DIR, "sales_dep.png"))


def plot_sales_vs_salary(sales_data, employee_data):
    """
    Plots a scatter plot showing the relationship between sales and salary.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.
    - employee_data (list): List of dictionaries representing employee data.

    Returns: None
    """
    sum_per_employee: pd.Series = sales_data.groupby("EmployeeID")["Amount"].sum().sort_index()
    salary_per_employee: pd.Series = employee_data.Salary.sort_index()

    df: pd.DataFrame = pd.DataFrame([sum_per_employee, salary_per_employee]).T
    df.plot.scatter("Salary", "Amount")

    plt.title("Salary vs Sales")

    plt.savefig(os.path.join(CURRENT_DIR, "sales_vs_salary.png"))
    
    

    # print(sum_per_employee.values)
    # print(salary_per_employee.values)

    # plt.scatter(sum_per_employee.values, salary_per_employee.values)

    # plt.xlabel("Sales")
    # plt.ylabel("Salary")
    # plt.title("Sales vs Salary")





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
