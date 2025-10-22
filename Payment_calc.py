from datetime import date, datetime


def mortgage_interest_calculator(
    loan_amount: float,
    annual_rate: float,
    start_date: str,
    loan_years: int = 30,
    payments_per_year: int = 12,
    today: str = None,
):
    """
    Calculate mortgage payment details.

    Args:
        loan_amount (float): Principal loan amount (e.g. 417000)
        annual_rate (float): Annual interest rate as percent (e.g. 5 for 5%)
        start_date (str): Start date in 'MM/DD/YYYY'
        loan_years (int): Loan period in years (default 30)
        payments_per_year (int): Number of payments per year (default 12)
        today (str): Current date in 'MM/DD/YYYY' format (optional)

    Returns:
        dict: Contains monthly payment, interest paid to date, and remaining interest
    """

    # Convert rates
    r = (annual_rate / 100) / payments_per_year
    n = loan_years * payments_per_year

    # Monthly payment formula
    payment = loan_amount * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

    # Convert dates
    start = datetime.strptime(start_date, "%m/%d/%Y").date()
    today_date = datetime.strptime(today, "%m/%d/%Y").date() if today else date.today()

    # Total months elapsed
    months_elapsed = max(
        0, (today_date.year - start.year) * 12 + (today_date.month - start.month)
    )

    # Total payments made so far
    payments_made = min(months_elapsed, n)

    # Total interest paid to date (amortization formula)
    # Remaining balance after 'payments_made' payments:
    if payments_made == 0:
        balance_remaining = loan_amount
    else:
        balance_remaining = (
            loan_amount * ((1 + r) ** n - (1 + r) ** payments_made) / ((1 + r) ** n - 1)
        )

    # Total paid so far
    total_paid = payments_made * payment

    # Interest paid so far
    interest_paid_to_date = total_paid - (loan_amount - balance_remaining)

    # Total interest over full loan
    total_interest = (payment * n) - loan_amount

    # Remaining interest
    interest_remaining = total_interest - interest_paid_to_date

    return {
        "Monthly Payment": round(payment, 2),
        "Payments Made": int(payments_made),
        "Interest Paid To Date": round(interest_paid_to_date, 2),
        "Interest Remaining": round(interest_remaining, 2),
        "Total Interest": round(total_interest, 2),
        "Balance Remaining": round(balance_remaining, 2),
    }


def get_user_input():
    """Get user input for loan parameters"""
    print("=== Mortgage Payment Calculator ===")
    print("Enter loan details (press Enter for defaults):")

    # Get loan amount
    while True:
        try:
            loan_input = input("Loan amount (default: $417,000): $").strip()
            if not loan_input:
                loan_amount = 417000
            else:
                loan_amount = float(loan_input.replace(",", ""))
            break
        except ValueError:
            print("Please enter a valid number.")

    # Get interest rate
    while True:
        try:
            rate_input = input("Annual interest rate % (default: 5%): ").strip()
            if not rate_input:
                annual_rate = 5.0
            else:
                annual_rate = float(rate_input)
            break
        except ValueError:
            print("Please enter a valid percentage.")

    # Get start date
    while True:
        try:
            start_input = input("Start date MM/DD/YYYY (default: 02/12/2025): ").strip()
            if not start_input:
                start_date = "02/12/2025"
            else:
                # Validate date format
                datetime.strptime(start_input, "%m/%d/%Y")
                start_date = start_input
            break
        except ValueError:
            print("Please enter date in MM/DD/YYYY format.")

    # Get loan term
    while True:
        try:
            term_input = input("Loan term in years (default: 30): ").strip()
            if not term_input:
                loan_years = 30
            else:
                loan_years = int(term_input)
            break
        except ValueError:
            print("Please enter a valid number of years.")

    return loan_amount, annual_rate, start_date, loan_years


def display_results(result):
    """Display calculation results in a formatted way"""
    print("\n" + "=" * 50)
    print("CALCULATION RESULTS")
    print("=" * 50)
    for k, v in result.items():
        if isinstance(v, float):
            print(f"{k}: ${v:,.2f}")
        else:
            print(f"{k}: {v:,}")


def get_refinance_input():
    """Get user input for refinance scenario"""
    print("\n=== REFINANCE SCENARIO ===")
    print("Enter new loan details for comparison:")

    # Get new interest rate
    while True:
        try:
            new_rate_input = input("New interest rate %: ").strip()
            new_rate = float(new_rate_input)
            break
        except ValueError:
            print("Please enter a valid percentage.")

    # Get new loan term
    while True:
        try:
            new_term_input = input("New loan term in years: ").strip()
            new_term = int(new_term_input)
            break
        except ValueError:
            print("Please enter a valid number of years.")

    return new_rate, new_term


def calculate_refinance_comparison(current_result, loan_amount, new_rate, new_term):
    """Calculate refinance comparison"""
    # Calculate new loan scenario
    new_result = mortgage_interest_calculator(
        loan_amount=loan_amount,
        annual_rate=new_rate,
        start_date="01/01/2024",  # Use current date for new loan
        loan_years=new_term,
    )

    # Calculate savings
    monthly_savings = current_result["Monthly Payment"] - new_result["Monthly Payment"]
    total_interest_savings = (
        current_result["Total Interest"] - new_result["Total Interest"]
    )

    return new_result, monthly_savings, total_interest_savings


def display_refinance_comparison(
    current_result, new_result, monthly_savings, total_interest_savings
):
    """Display refinance comparison results"""
    print("\n" + "=" * 60)
    print("REFINANCE COMPARISON")
    print("=" * 60)

    print("\nCURRENT LOAN:")
    for k, v in current_result.items():
        if isinstance(v, float):
            print(f"  {k}: ${v:,.2f}")
        else:
            print(f"  {k}: {v:,}")

    print("\nNEW LOAN:")
    for k, v in new_result.items():
        if isinstance(v, float):
            print(f"  {k}: ${v:,.2f}")
        else:
            print(f"  {k}: {v:,}")

    print("\nSAVINGS:")
    print(f"  Monthly Payment Savings: ${monthly_savings:,.2f}")
    print(f"  Total Interest Savings: ${total_interest_savings:,.2f}")

    if monthly_savings > 0:
        print(f"\n✅ You would save ${monthly_savings:,.2f} per month")
    else:
        print(f"\n❌ You would pay ${abs(monthly_savings):,.2f} more per month")

    if total_interest_savings > 0:
        print(f"✅ You would save ${total_interest_savings:,.2f} in total interest")
    else:
        print(
            f"❌ You would pay ${abs(total_interest_savings):,.2f} more in total interest"
        )


def main():
    """Main function to run the calculator"""
    while True:
        try:
            # Get user input
            loan_amount, annual_rate, start_date, loan_years = get_user_input()

            # Calculate current loan results
            current_result = mortgage_interest_calculator(
                loan_amount=loan_amount,
                annual_rate=annual_rate,
                start_date=start_date,
                loan_years=loan_years,
            )

            # Display current results
            display_results(current_result)

            # Ask if user wants to compare refinance scenario
            print("\n" + "=" * 50)
            refinance = (
                input("Compare with refinance scenario? (y/n): ").strip().lower()
            )

            if refinance in ["y", "yes"]:
                new_rate, new_term = get_refinance_input()
                new_result, monthly_savings, total_interest_savings = (
                    calculate_refinance_comparison(
                        current_result, loan_amount, new_rate, new_term
                    )
                )
                display_refinance_comparison(
                    current_result, new_result, monthly_savings, total_interest_savings
                )

            # Ask if user wants to calculate another scenario
            print("\n" + "=" * 50)
            another = input("Calculate another scenario? (y/n): ").strip().lower()
            if another not in ["y", "yes"]:
                break

        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
