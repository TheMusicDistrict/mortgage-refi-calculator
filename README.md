# 🏠 Mortgage Payment Calculator

**"It's Not Rocket Science. It's Math."**

A comprehensive mortgage calculator built with Streamlit that helps users calculate mortgage payments, compare refinance scenarios, and analyze the financial impact of different loan options.

## ✨ Features

### 📊 **Current Loan Analysis**
- Calculate monthly payments, interest, and remaining balance
- Track payments made and interest paid to date
- Highlight key metrics (balance remaining, interest remaining)

### 🔄 **Refinance Comparison**
- Compare current loan with refinance options
- Use current balance remaining as base loan amount
- 0.125% (1/8 point) interest rate increments
- Flexible loan terms (15, 20, 25, 30 years)

### 💰 **Closing Costs Analysis**
- Add closing costs to loan or pay out of pocket
- Show minimal impact on monthly payments
- Break-even analysis (time to recoup costs)
- Cost comparison between payment options

### 📈 **Savings Analysis**
- Monthly payment savings/increases
- Total interest impact (accurate comparison)
- Annual savings calculations
- Color-coded results (green for savings, red for increases)

### 📥 **Export & Reporting**
- Download comprehensive calculation reports
- Professional formatting with all calculations
- Timestamped files for easy organization

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Streamlit

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/mortgage-calculator.git
   cd mortgage-calculator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run mortgage_app.py
   ```

4. **Open in browser:**
   - Navigate to `http://localhost:8501`

## 📋 Usage

### **Step 1: Current Loan Details**
- Enter loan amount, interest rate, start date, and term
- Click "Calculate Current Loan" to see results

### **Step 2: Refinance Comparison**
- Enter new interest rate and loan term
- Set closing costs (default: $5,000)
- Choose to roll costs into loan or pay out of pocket
- Click "Compare Refinance" to see analysis

### **Step 3: Review Results**
- Compare current vs. refinance scenarios
- Review savings analysis and break-even calculations
- Download full report for sharing

## 🎯 Key Calculations

### **Accurate Interest Comparison**
- Compares remaining interest on current loan vs. total interest on new loan
- Shows true financial impact of refinancing
- Color-coded results for easy interpretation

### **Break-Even Analysis**
- Calculates time to recoup closing costs
- Provides recommendations based on timeline
- Shows minimal monthly impact of rolling in costs

## 📁 Project Structure

```
mortgage-calculator/
├── mortgage_app.py          # Main Streamlit application
├── Payment_calc.py          # Core mortgage calculation functions
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## 🔧 Technical Details

### **Mortgage Calculations**
- Standard mortgage payment formula
- Accurate amortization calculations
- Proper balance remaining calculations
- Interest paid to date tracking

### **Refinance Logic**
- Uses current balance remaining as base loan amount
- Accounts for closing costs in loan amount
- Compares apples-to-apples interest calculations

## 📞 Contact

**Have questions? Want to leverage the equity in your property and take cash out?**

📧 **Email:** arallo@rhfny.com

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Built with ❤️ using Streamlit**
