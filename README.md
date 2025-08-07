# Result-Analysis-Dashboard
My College Result Analysis Dashboard which is calculated internal Marks.
# 📊 Result Analysis Dashboard

An interactive web-based dashboard built using **Python and Streamlit** to analyze students’ academic performance from Excel files.

## 🚀 Features

- Upload Excel sheets with students' assessment and midterm marks
- Automatic calculation of:
  - AAT averages
  - Weighted midterm averages
  - Final internal marks
  - Pass/Fail status (Qualified/NQ)
- Visualization using:
  - 📦 Box plots (Internal Marks)
  - 📊 Bar chart (Percentage of NQ students per subject)
- Export final result with status as CSV

---

## 🧾 Input File Format

The input Excel file must include the following columns:

- `Roll Number`, `Name`
- AAT Columns: `s1a1`, `s1a2`, ..., `s6a1`, `s6a2`
- Midterm Columns: `s1m1`, `s1m2`, ..., `s6m1`, `s6m2`

Ensure that:
- Absent values are marked as `A`
- Marks are in numeric format

---

## 🛠️ Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/Avinashbabu-23/Result-Analysis-Dashboard.git

