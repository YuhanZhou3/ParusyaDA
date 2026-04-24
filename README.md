# ⛪ Youth Group Participant Analytics

A full-stack data analysis project examining participant demographics and behaviour for a Catholic youth group — covering ETL, exploratory data analysis, and an interactive dashboard.

---

## 📌 Project Overview

| | |
|---|---|
| **Domain** | Non-profit / Community Organization |
| **Goal** | Understand participant demographics and attendance behaviour to support program planning and resource allocation |
| **Stack** | Python · SQLite · Pandas · Dash · Plotly |

---

## 🗂️ Project Structure

```
ParusyaDA/
├── data_public/
│   └── cleaned_data.csv
├── extract_transform.py
├── analysis.ipynb
└── README.md
```

ETL: extract_transform.py
EDA & Dashboarding: analysis.ipynb

---

## 🔄 ETL Pipeline

### Extraction
- Queried a **SQLite** relational database using `sqlite3` and raw SQL
- Reverse-engineered the relational schema including foreign key relationships across multiple tables
- Loaded query results into **Pandas DataFrames** for downstream processing

### Transformation
- Handled missing values and corrected data types (e.g. `object` → `datetime`)
- Adjusted timestamps from server time zone to local time zone
- Engineered `age` column derived from participant birthdates
- Filtered out erroneous records (e.g. ages of 0 or 2 years old)
- **De-identified all personal information** to comply with privacy best practices

### Loading
- Cleaned data are stored as a csv file, and loaded in EDA file.

---

## 📊 Exploratory Data Analysis

### Participant Demographics

**Univariate**
- Gender distribution (percentage breakdown)
- Age distribution: mean, median, std, variance; Pareto (80/20) analysis; bar chart

**Bivariate / Multivariate**
- Age × Gender: distribution comparison and mean age by gender (histogram)
- Gender × Attendance: descriptive statistics (mean, std, variance) — no significant relationship found
- Age × Attendance: correlation analysis — no significant correlation found
- Age × Gender × Attendance: grouped histogram

### Participant Behaviour

**Check-in Time Analysis (Minute Rush)**
- Line graph of check-in volume by minute, segmented by event
- Identified peak check-in counts across events → used to estimate optimal staff allocation

**Dropout Risk Analysis**
- Defined a custom dropout threshold based on attendance patterns
- Flagged at-risk participants for potential follow-up

---

## 📈 Dashboard

Built with **Dash** (Python) and HTML/CSS.

### KPI Cards
| Card | Detail |
|---|---|
| Number of Participants | Age range breakdown stacked below |
| Average Age | Median age stacked below |
| Gender Distribution | Mini split bar with percentage labels |
| Attendance Percentage | Overall attendance rate |

### Charts
1. **Age Distribution** — bar chart
2. **Attendance Rate vs. Age & Gender** — grouped histogram
3. **Max Check-in Volume by Time** — time-series line chart

---

## 🔒 Privacy

All participant data used in this project has been de-identified. No real names, contact information, or personally identifiable information (PII) are present in the codebase or outputs.

---

## 🛠️ Setup

```bash
pip install pandas sqlite3 dash plotly
```

---

## 💡 Key Findings

- No statistically significant relationship was found between gender/age and attendance frequency
- Check-in volume peaks occur within the first ~10 minutes of events, informing staffing decisions
- A meaningful subset of participants meets the dropout threshold, suggesting an opportunity for targeted outreach