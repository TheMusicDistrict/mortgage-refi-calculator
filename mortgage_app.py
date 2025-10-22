import streamlit as st
from datetime import date, datetime
import pandas as pd


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

    # Calculate remaining balance using standard mortgage formula
    if payments_made == 0:
        balance_remaining = loan_amount
    else:
        # Standard mortgage balance formula: P * [(1+r)^n - (1+r)^p] / [(1+r)^n - 1]
        balance_remaining = (
            loan_amount * ((1 + r) ** n - (1 + r) ** payments_made) / ((1 + r) ** n - 1)
        )

    # Total paid so far
    total_paid = payments_made * payment

    # Principal paid so far
    principal_paid = loan_amount - balance_remaining

    # Interest paid so far
    interest_paid_to_date = total_paid - principal_paid

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
        "Principal Paid": round(principal_paid, 2),
    }


def main():
    st.set_page_config(page_title="Mortgage Calculator", page_icon="🏠", layout="wide")

    # Header section
    st.markdown(
        """
    <div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0; font-size: 2.5em;">It's Not Rocket Science. It's Math.</h1>
        <p style="color: white; font-size: 1.2em; margin: 10px 0;">Have questions? Want to leverage the equity in your property and take cash out?</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Email contact button
    col_contact1, col_contact2, col_contact3 = st.columns([1, 2, 1])
    with col_contact2:
        if st.button(
            "📧 Contact Us: arallo@rhfny.com", type="primary", use_container_width=True
        ):
            st.markdown("**Email:** arallo@rhfny.com")
            st.markdown("**Click to copy:** `arallo@rhfny.com`")

    st.markdown("---")

    st.title("🏠 Mortgage Payment Calculator")
    st.markdown("Calculate your mortgage payments and compare refinance scenarios")

    # Create two columns
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("Current Loan Details")

        # Input fields
        loan_amount = st.number_input(
            "Loan Amount ($)", min_value=0.0, value=417000.0, step=1000.0, format="%.0f"
        )

        annual_rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            max_value=30.0,
            value=5.0,
            step=0.1,
            format="%.2f",
        )

        start_date = st.date_input(
            "Loan Start Date", value=datetime(2025, 2, 12).date()
        )

        loan_years = st.selectbox(
            "Loan Term (Years)", options=[15, 20, 25, 30], index=3
        )

        # Convert date to string format
        start_date_str = start_date.strftime("%m/%d/%Y")

        # Calculate current loan
        if st.button("Calculate Current Loan", type="primary"):
            current_result = mortgage_interest_calculator(
                loan_amount=loan_amount,
                annual_rate=annual_rate,
                start_date=start_date_str,
                loan_years=loan_years,
            )

            st.session_state.current_result = current_result
            st.session_state.loan_amount = loan_amount

    with col2:
        st.header("Refinance Comparison")

        # Refinance inputs
        # Use quick rate if set, otherwise default
        default_rate = 4.0
        if "quick_rate" in st.session_state:
            default_rate = st.session_state.quick_rate

        new_rate = st.number_input(
            "New Interest Rate (%)",
            min_value=0.0,
            max_value=30.0,
            value=default_rate,
            step=0.125,
            format="%.3f",
            key="new_rate",
            help="Use +/- buttons to adjust by 0.125% (1/8 point) increments",
        )

        # Use quick term if set, otherwise default
        default_term_index = 0  # 15 years
        if "quick_term" in st.session_state:
            term_options = [15, 20, 25, 30]
            if st.session_state.quick_term in term_options:
                default_term_index = term_options.index(st.session_state.quick_term)

        new_term = st.selectbox(
            "New Loan Term (Years)",
            options=[15, 20, 25, 30],
            index=default_term_index,
            key="new_term",
        )

        # Closing costs section
        st.subheader("💰 Closing Costs")
        closing_costs = st.number_input(
            "Closing Costs ($)",
            min_value=0.0,
            value=5000.0,
            step=100.0,
            format="%.0f",
            key="closing_costs",
            help="Typical closing costs range from $2,000-$5,000",
        )

        # Option to roll costs into loan
        roll_costs = st.checkbox(
            "Roll closing costs into loan",
            value=True,
            help="If checked, closing costs are added to loan amount. If unchecked, you pay out of pocket.",
        )

        if st.button("Compare Refinance", type="secondary"):
            if "current_result" in st.session_state:
                # Use current balance remaining as the base loan amount for refinance
                current_balance = st.session_state.current_result["Balance Remaining"]

                # Calculate new loan amount based on closing costs option
                if roll_costs:
                    new_loan_amount = current_balance + closing_costs
                    st.session_state.closing_costs_rolled = True
                else:
                    new_loan_amount = current_balance
                    st.session_state.closing_costs_rolled = False

                # Calculate refinance scenario
                new_result = mortgage_interest_calculator(
                    loan_amount=new_loan_amount,
                    annual_rate=new_rate,
                    start_date="01/01/2024",
                    loan_years=new_term,
                )

                # Calculate savings
                monthly_savings = (
                    st.session_state.current_result["Monthly Payment"]
                    - new_result["Monthly Payment"]
                )

                # Compare remaining interest on current loan vs total interest on new loan
                current_remaining_interest = st.session_state.current_result[
                    "Interest Remaining"
                ]
                new_total_interest = new_result["Total Interest"]
                total_interest_savings = current_remaining_interest - new_total_interest

                st.session_state.new_result = new_result
                st.session_state.monthly_savings = monthly_savings
                st.session_state.total_interest_savings = total_interest_savings
                st.session_state.refinance_closing_costs = closing_costs
                st.session_state.new_loan_amount = new_loan_amount

    # Display results
    if "current_result" in st.session_state:
        st.markdown("---")
        st.header("📊 Results")

        # Create results columns
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.subheader("Current Loan")

            # Highlight key metrics with metrics widgets
            col1a, col1b = st.columns(2)
            with col1a:
                st.metric(
                    "Balance Remaining",
                    f"${st.session_state.current_result['Balance Remaining']:,.2f}",
                    help="Outstanding principal balance",
                )
            with col1b:
                st.metric(
                    "Interest Remaining",
                    f"${st.session_state.current_result['Interest Remaining']:,.2f}",
                    help="Total interest left to pay",
                )

            # Additional details in table
            current_df = pd.DataFrame(
                [
                    [
                        "Monthly Payment",
                        f"${st.session_state.current_result['Monthly Payment']:,.2f}",
                    ],
                    [
                        "Total Interest",
                        f"${st.session_state.current_result['Total Interest']:,.2f}",
                    ],
                    [
                        "Interest Paid",
                        f"${st.session_state.current_result['Interest Paid To Date']:,.2f}",
                    ],
                    [
                        "Payments Made",
                        f"{st.session_state.current_result['Payments Made']:,}",
                    ],
                ],
                columns=["Metric", "Value"],
            )
            st.dataframe(current_df, hide_index=True, use_container_width=True)

        if "new_result" in st.session_state:
            with col2:
                st.subheader("Refinance Loan")

                # Show loan amount with closing costs info
                if st.session_state.closing_costs_rolled:
                    st.info(
                        f"💰 Loan includes ${st.session_state.refinance_closing_costs:,.0f} closing costs"
                    )
                else:
                    st.info(
                        f"💵 You pay ${st.session_state.refinance_closing_costs:,.0f} closing costs out of pocket"
                    )

                new_df = pd.DataFrame(
                    [
                        [
                            "Loan Amount",
                            f"${st.session_state.new_loan_amount:,.2f}",
                        ],
                        [
                            "Monthly Payment",
                            f"${st.session_state.new_result['Monthly Payment']:,.2f}",
                        ],
                        [
                            "Total Interest",
                            f"${st.session_state.new_result['Total Interest']:,.2f}",
                        ],
                        [
                            "Payments Made",
                            f"{st.session_state.new_result['Payments Made']:,}",
                        ],
                        [
                            "Balance Remaining",
                            f"${st.session_state.new_result['Balance Remaining']:,.2f}",
                        ],
                    ],
                    columns=["Metric", "Value"],
                )
                st.dataframe(new_df, hide_index=True, use_container_width=True)

            with col3:
                st.subheader("Savings Analysis")

                # Monthly savings
                if st.session_state.monthly_savings > 0:
                    st.success(
                        f"💚 Monthly Savings: ${st.session_state.monthly_savings:,.2f}"
                    )
                else:
                    st.error(
                        f"💸 Monthly Increase: ${abs(st.session_state.monthly_savings):,.2f}"
                    )

                # Total interest savings
                if st.session_state.total_interest_savings > 0:
                    st.success(
                        f"💰 Total Interest Savings: ${st.session_state.total_interest_savings:,.2f}"
                    )
                else:
                    st.error(
                        f"💸 Total Interest Increase: ${abs(st.session_state.total_interest_savings):,.2f}"
                    )

                # Annual savings
                annual_savings = st.session_state.monthly_savings * 12
                st.metric("Annual Savings", f"${annual_savings:,.2f}")

                # Show closing costs impact
                if st.session_state.refinance_closing_costs > 0:
                    st.markdown("---")
                    st.subheader("💡 Closing Costs Impact")

                    # Calculate what the payment would be without closing costs
                    if st.session_state.closing_costs_rolled:
                        # Show impact of rolling costs in
                        current_balance = st.session_state.current_result[
                            "Balance Remaining"
                        ]
                        cost_impact = (
                            st.session_state.new_result["Monthly Payment"]
                            - mortgage_interest_calculator(
                                loan_amount=current_balance,
                                annual_rate=new_rate,
                                start_date="01/01/2024",
                                loan_years=new_term,
                            )["Monthly Payment"]
                        )

                        st.success(
                            f"📈 Rolling in ${st.session_state.refinance_closing_costs:,.0f} costs adds only ${cost_impact:.2f}/month"
                        )
                        st.caption(
                            "Closing costs have minimal impact on monthly payment!"
                        )

                        # Show comparison: out of pocket vs rolled in
                        st.markdown("**💡 Cost Comparison:**")
                        out_of_pocket_payment = mortgage_interest_calculator(
                            loan_amount=current_balance,
                            annual_rate=new_rate,
                            start_date="01/01/2024",
                            loan_years=new_term,
                        )["Monthly Payment"]

                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric(
                                "Pay Out of Pocket",
                                f"${out_of_pocket_payment:.2f}/month",
                            )
                        with col_b:
                            st.metric(
                                "Roll Into Loan",
                                f"${st.session_state.new_result['Monthly Payment']:.2f}/month",
                            )

                        st.caption(
                            f"Difference: Only ${cost_impact:.2f} more per month to avoid paying ${st.session_state.refinance_closing_costs:,.0f} upfront!"
                        )

                        # Add monthly and total interest savings metrics
                        st.markdown("**📊 Refinance Savings:**")

                        # Calculate savings for the refinance scenario
                        refinance_monthly_savings = st.session_state.monthly_savings
                        refinance_total_savings = (
                            st.session_state.total_interest_savings
                        )

                        col_savings1, col_savings2 = st.columns(2)
                        with col_savings1:
                            if refinance_monthly_savings > 0:
                                st.success(
                                    f"💚 Monthly Savings: ${refinance_monthly_savings:.2f}"
                                )
                            else:
                                st.error(
                                    f"💸 Monthly Increase: ${abs(refinance_monthly_savings):.2f}"
                                )

                        with col_savings2:
                            if refinance_total_savings > 0:
                                st.success(
                                    f"💰 Total Interest Savings: ${refinance_total_savings:,.2f}"
                                )
                            else:
                                st.error(
                                    f"💸 Total Interest Increase: ${abs(refinance_total_savings):,.2f}"
                                )

                        # Break-even analysis
                        if refinance_monthly_savings > 0:
                            st.markdown("**⏱️ Break-Even Analysis:**")

                            # Calculate break-even in months
                            break_even_months = (
                                st.session_state.refinance_closing_costs
                                / refinance_monthly_savings
                            )

                            # Convert to years, months, and days
                            years = int(break_even_months // 12)
                            remaining_months = int(break_even_months % 12)
                            days = int((break_even_months % 1) * 30)  # Approximate days

                            # Format the break-even time
                            if years > 0:
                                if remaining_months > 0:
                                    break_even_text = f"{years} year{'s' if years > 1 else ''}, {remaining_months} month{'s' if remaining_months > 1 else ''}"
                                else:
                                    break_even_text = (
                                        f"{years} year{'s' if years > 1 else ''}"
                                    )
                            else:
                                break_even_text = f"{remaining_months} month{'s' if remaining_months > 1 else ''}"

                            if days > 0 and remaining_months < 12:
                                break_even_text += (
                                    f", {days} day{'s' if days > 1 else ''}"
                                )

                            st.info(f"🕐 Break-even: {break_even_text}")
                            st.caption(
                                f"Time to recoup ${st.session_state.refinance_closing_costs:,.0f} in closing costs"
                            )

                            # Show if it's worth it
                            if break_even_months < 24:  # Less than 2 years
                                st.success("✅ Good refinance - recoups costs quickly!")
                            elif break_even_months < 60:  # Less than 5 years
                                st.warning(
                                    "⚠️ Moderate refinance - consider your timeline"
                                )
                            else:
                                st.error(
                                    "❌ Poor refinance - takes too long to break even"
                                )
                        else:
                            st.error(
                                "❌ No monthly savings - refinance not recommended"
                            )

                    else:
                        st.info(
                            f"💵 You pay ${st.session_state.refinance_closing_costs:,.0f} out of pocket to keep loan amount lower"
                        )

    # Sidebar with additional features
    with st.sidebar:
        st.header("🔧 Additional Features")

        # Amortization schedule preview
        if "current_result" in st.session_state:
            st.subheader("Amortization Preview")

            # Calculate first 12 months
            r = (annual_rate / 100) / 12
            n = loan_years * 12
            payment = st.session_state.current_result["Monthly Payment"]

            schedule_data = []
            balance = loan_amount

            for month in range(1, 13):  # First 12 months
                interest_payment = balance * r
                principal_payment = payment - interest_payment
                balance -= principal_payment

                schedule_data.append(
                    {
                        "Month": month,
                        "Payment": f"${payment:,.2f}",
                        "Principal": f"${principal_payment:,.2f}",
                        "Interest": f"${interest_payment:,.2f}",
                        "Balance": f"${balance:,.2f}",
                    }
                )

            schedule_df = pd.DataFrame(schedule_data)
            st.dataframe(schedule_df, hide_index=True, use_container_width=True)

        # Quick scenarios
        st.subheader("⚙️ Quick Actions")
        if st.button("Reset to Defaults"):
            st.session_state.clear()
            st.rerun()

        # Debug information
        if "current_result" in st.session_state:
            st.subheader("🔍 Debug Info")
            st.write(f"**Monthly Rate:** {((annual_rate / 100) / 12):.6f}")
            st.write(f"**Total Payments:** {loan_years * 12}")
            st.write(
                f"**Months Elapsed:** {max(0, (date.today().year - datetime.strptime(start_date_str, '%m/%d/%Y').date().year) * 12 + (date.today().month - datetime.strptime(start_date_str, '%m/%d/%Y').date().month))}"
            )

            # Validation check
            total_should_be = (
                st.session_state.current_result["Principal Paid"]
                + st.session_state.current_result["Balance Remaining"]
            )
            st.write(
                f"**Validation:** Principal + Balance = ${total_should_be:,.2f} (Should equal loan amount: ${loan_amount:,.2f})"
            )

        # Export comprehensive results
        if "current_result" in st.session_state:
            # Create comprehensive report
            report_data = []
            report_data.append("=" * 60)
            report_data.append("MORTGAGE CALCULATION REPORT")
            report_data.append("=" * 60)
            report_data.append(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            report_data.append("")

            # Current loan details
            report_data.append("CURRENT LOAN DETAILS:")
            report_data.append("-" * 30)
            report_data.append(f"Loan Amount: ${loan_amount:,.2f}")
            report_data.append(f"Interest Rate: {annual_rate}%")
            report_data.append(f"Start Date: {start_date_str}")
            report_data.append(f"Loan Term: {loan_years} years")
            report_data.append("")

            # Current loan results
            report_data.append("CURRENT LOAN RESULTS:")
            report_data.append("-" * 30)
            for key, value in st.session_state.current_result.items():
                if isinstance(value, float):
                    report_data.append(f"{key}: ${value:,.2f}")
                else:
                    report_data.append(f"{key}: {value:,}")
            report_data.append("")

            # Refinance results if available
            if "new_result" in st.session_state:
                report_data.append("REFINANCE COMPARISON:")
                report_data.append("-" * 30)
                report_data.append(f"New Interest Rate: {new_rate}%")
                report_data.append(f"New Loan Term: {new_term} years")
                report_data.append(
                    f"Closing Costs: ${st.session_state.refinance_closing_costs:,.2f}"
                )
                report_data.append(
                    f"Costs Rolled In: {'Yes' if st.session_state.closing_costs_rolled else 'No'}"
                )
                report_data.append("")

                report_data.append("REFINANCE LOAN RESULTS:")
                report_data.append("-" * 30)
                for key, value in st.session_state.new_result.items():
                    if isinstance(value, float):
                        report_data.append(f"{key}: ${value:,.2f}")
                    else:
                        report_data.append(f"{key}: {value:,}")
                report_data.append("")

                # Savings analysis
                report_data.append("SAVINGS ANALYSIS:")
                report_data.append("-" * 30)
                report_data.append(
                    f"Monthly Savings: ${st.session_state.monthly_savings:,.2f}"
                )

                # Use the same corrected calculation as the main display
                if st.session_state.total_interest_savings > 0:
                    report_data.append(
                        f"Total Interest Savings: ${st.session_state.total_interest_savings:,.2f}"
                    )
                else:
                    report_data.append(
                        f"Total Interest Increase: ${abs(st.session_state.total_interest_savings):,.2f}"
                    )

                report_data.append(
                    f"Annual Savings: ${st.session_state.monthly_savings * 12:,.2f}"
                )
                report_data.append("")

                # Break-even analysis
                if st.session_state.monthly_savings > 0:
                    break_even_months = (
                        st.session_state.refinance_closing_costs
                        / st.session_state.monthly_savings
                    )
                    years = int(break_even_months // 12)
                    remaining_months = int(break_even_months % 12)
                    days = int((break_even_months % 1) * 30)

                    if years > 0:
                        if remaining_months > 0:
                            break_even_text = f"{years} year{'s' if years > 1 else ''}, {remaining_months} month{'s' if remaining_months > 1 else ''}"
                        else:
                            break_even_text = f"{years} year{'s' if years > 1 else ''}"
                    else:
                        break_even_text = f"{remaining_months} month{'s' if remaining_months > 1 else ''}"

                    if days > 0 and remaining_months < 12:
                        break_even_text += f", {days} day{'s' if days > 1 else ''}"

                    report_data.append("BREAK-EVEN ANALYSIS:")
                    report_data.append(f"Time to recoup costs: {break_even_text}")
                    report_data.append(f"Break-even months: {break_even_months:.1f}")

                    if break_even_months < 24:
                        report_data.append(
                            "Recommendation: ✅ Good refinance - recoups costs quickly!"
                        )
                    elif break_even_months < 60:
                        report_data.append(
                            "Recommendation: ⚠️ Moderate refinance - consider your timeline"
                        )
                    else:
                        report_data.append(
                            "Recommendation: ❌ Poor refinance - takes too long to break even"
                        )
                else:
                    report_data.append("BREAK-EVEN ANALYSIS:")
                    report_data.append(
                        "❌ No monthly savings - refinance not recommended"
                    )

            # Join all data
            report_text = "\n".join(report_data)

            st.download_button(
                label="📥 Download Full Report",
                data=report_text,
                file_name=f"mortgage_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                help="Download comprehensive mortgage calculation report",
            )


if __name__ == "__main__":
    main()
