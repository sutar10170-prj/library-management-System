from decimal import Decimal, ROUND_HALF_UP


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

CENT = Decimal("0.01")


def money(value):
    """Round a monetary amount to two decimal places."""
    return Decimal(value).quantize(
        CENT,
        rounding=ROUND_HALF_UP
    )


def format_money(value):
    """Format an amount using Indian currency notation."""
    value = money(value)
    return f"₹{value:,.2f}"


# --------------------------------------------------
# MAIN LOAN CALCULATION METHOD
# --------------------------------------------------

def calculate_loan(
    principal,
    annual_rate,
    tenure_months,
    interest_method
):
    """
    Calculate a loan using either Flat or Reducing interest.

    Parameters:
        principal: Original loan amount
        annual_rate: Annual interest rate in percentage
        tenure_months: Loan tenure in months
        interest_method: 'flat' or 'reducing'

    Returns:
        Loan details and monthly repayment schedule.
    """

    # Convert inputs to Decimal for financial precision
    principal = Decimal(str(principal))
    annual_rate = Decimal(str(annual_rate))
    tenure_months = int(tenure_months)

    interest_method = interest_method.lower().strip()

    # Validate inputs
    if principal <= 0:
        raise ValueError(
            "Loan principal must be greater than zero."
        )

    if annual_rate < 0:
        raise ValueError(
            "Interest rate cannot be negative."
        )

    if tenure_months <= 0:
        raise ValueError(
            "Tenure must be greater than zero."
        )

    if interest_method not in ("flat", "reducing"):
        raise ValueError(
            "Interest method must be 'flat' or 'reducing'."
        )

    # Calculate monthly interest rate
    monthly_rate = annual_rate / Decimal("1200")

    # Initialize variables
    schedule = []
    outstanding = principal

    # --------------------------------------------------
    # FLAT INTEREST CALCULATION
    # --------------------------------------------------

    if interest_method == "flat":

        # Total interest is calculated on original principal
        total_interest = money(
            principal
            * annual_rate
            * tenure_months
            / Decimal("1200")
        )

        # Total amount payable
        total_payable = principal + total_interest

        # Regular EMI, rounded to two decimal places
        emi = money(
            total_payable / tenure_months
        )

        # Divide flat interest across the installments.
        # The last month's interest is adjusted for rounding.
        regular_interest = money(
            total_interest / tenure_months
        )

        interest_paid_so_far = Decimal("0.00")

        for month in range(1, tenure_months + 1):

            if month == tenure_months:
                interest = money(
                    total_interest - interest_paid_so_far
                )
            else:
                interest = regular_interest

            interest_paid_so_far += interest

            # Make the final installment clear the balance
            if month == tenure_months:
                principal_repaid = outstanding
                payment = money(
                    principal_repaid + interest
                )

            else:
                payment = emi
                principal_repaid = money(
                    payment - interest
                )

                # Protect against a negative outstanding balance
                principal_repaid = min(
                    principal_repaid,
                    outstanding
                )

            outstanding = money(
                outstanding - principal_repaid
            )

            if outstanding < 0:
                outstanding = Decimal("0.00")

            schedule.append({
                "month": month,
                "emi": payment,
                "principal": principal_repaid,
                "interest": interest,
                "outstanding": outstanding
            })

    # --------------------------------------------------
    # REDUCING BALANCE CALCULATION
    # --------------------------------------------------

    else:

        # Calculate EMI using the reducing balance formula
        if monthly_rate == 0:

            emi = money(
                principal / tenure_months
            )

        else:

            factor = (
                Decimal("1") + monthly_rate
            ) ** tenure_months

            exact_emi = (
                principal
                * monthly_rate
                * factor
                / (factor - Decimal("1"))
            )

            emi = money(exact_emi)

        for month in range(1, tenure_months + 1):

            # Interest is calculated on the outstanding principal
            interest = money(
                outstanding * monthly_rate
            )

            # The final payment clears the remaining balance
            if month == tenure_months:

                principal_repaid = outstanding

                payment = money(
                    principal_repaid + interest
                )

            else:

                payment = emi

                principal_repaid = money(
                    payment - interest
                )

                # Prevent the principal from exceeding the balance
                principal_repaid = min(
                    principal_repaid,
                    outstanding
                )

                # If rounding causes an early payoff,
                # clear the balance without overcharging.
                if principal_repaid >= outstanding:
                    principal_repaid = outstanding
                    payment = money(
                        principal_repaid + interest
                    )

            outstanding = money(
                outstanding - principal_repaid
            )

            if outstanding < 0:
                outstanding = Decimal("0.00")

            schedule.append({
                "month": month,
                "emi": payment,
                "principal": principal_repaid,
                "interest": interest,
                "outstanding": outstanding
            })

    # --------------------------------------------------
    # FINAL TOTALS
    # --------------------------------------------------

    actual_interest = sum(
        (row["interest"] for row in schedule),
        Decimal("0.00")
    )

    total_repayment = sum(
        (row["emi"] for row in schedule),
        Decimal("0.00")
    )

    return {
        "principal": money(principal),
        "annual_rate": annual_rate,
        "tenure_months": tenure_months,
        "interest_method": interest_method,
        "monthly_emi": emi,
        "total_interest": money(actual_interest),
        "total_repayment": money(total_repayment),
        "schedule": schedule
    }


# --------------------------------------------------
# DISPLAY LOAN SUMMARY
# --------------------------------------------------

def display_loan_summary(result):

    print("\n")
    print("=" * 76)
    print("                  LOAN REPAYMENT SUMMARY")
    print("=" * 76)

    print(
        f"  Interest Method       : "
        f"{result['interest_method'].upper()}"
    )

    print(
        f"  Loan Amount           : "
        f"{format_money(result['principal'])}"
    )

    print(
        f"  Annual Interest Rate  : "
        f"{result['annual_rate']}%"
    )

    print(
        f"  Loan Tenure            : "
        f"{result['tenure_months']} months"
    )

    print("-" * 76)

    print(
        f"  Regular Monthly EMI   : "
        f"{format_money(result['monthly_emi'])}"
    )

    print(
        f"  Total Interest        : "
        f"{format_money(result['total_interest'])}"
    )

    print(
        f"  Total Repayment       : "
        f"{format_money(result['total_repayment'])}"
    )

    print("=" * 76)


# --------------------------------------------------
# DISPLAY REPAYMENT SCHEDULE
# --------------------------------------------------

def display_schedule(result):

    print("\n")
    print(
        f"             {result['interest_method'].upper()} "
        f"INTEREST REPAYMENT SCHEDULE"
    )
    print("=" * 88)

    header = (
        f"{'Month':>5} | "
        f"{'EMI':>14} | "
        f"{'Principal':>14} | "
        f"{'Interest':>14} | "
        f"{'Outstanding':>14}"
    )

    print(header)
    print("-" * 88)

    for row in result["schedule"]:

        print(
            f"{row['month']:>5} | "
            f"{format_money(row['emi']):>14} | "
            f"{format_money(row['principal']):>14} | "
            f"{format_money(row['interest']):>14} | "
            f"{format_money(row['outstanding']):>14}"
        )

    print("-" * 88)

    print(
        f"{'TOTAL':>5} | "
        f"{format_money(result['total_repayment']):>14} | "
        f"{format_money(result['principal']):>14} | "
        f"{format_money(result['total_interest']):>14} | "
        f"{format_money(Decimal('0.00')):>14}"
    )

    print("=" * 88)


# --------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":

    # Example loan details
    loan_amount = 100000
    annual_interest_rate = 12
    tenure = 12

    # Run the same method for both interest types
    for method in ("flat", "reducing"):

        result = calculate_loan(
            principal=loan_amount,
            annual_rate=annual_interest_rate,
            tenure_months=tenure,
            interest_method=method
        )

        display_loan_summary(result)
        display_schedule(result)