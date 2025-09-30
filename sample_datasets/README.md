# Sample Datasets for Multi-Agent Decision System

This folder contains various sample datasets to demonstrate the capabilities of the multi-agent decision-making system.

## 📊 Available Datasets

### 1. **Laptops** (`laptops.csv`)
**Use Case**: Technology purchase decisions
- **Columns**: description, price, brand, category, rating, specs
- **Sample Queries**:
  - "I need a laptop for programming under $1500"
  - "What's the best gaming laptop with good performance?"
  - "I want a lightweight laptop for business travel"

### 2. **Investment Options** (`investment_options.csv`)
**Use Case**: Financial planning and investment decisions
- **Columns**: description, expected_return, risk_level, minimum_investment, category, liquidity
- **Sample Queries**:
  - "I want to invest $10,000 with moderate risk for retirement"
  - "What's the safest investment option for emergency funds?"
  - "I'm looking for high-growth investments for long-term wealth building"

### 3. **Vacation Destinations** (`vacation_destinations.csv`)
**Use Case**: Travel planning and destination selection
- **Columns**: description, cost_per_week, climate, activities, difficulty, season
- **Sample Queries**:
  - "I want an adventurous vacation with beautiful nature under $1500"
  - "What's the best romantic destination for a honeymoon?"
  - "I need a family-friendly vacation with easy activities"

### 4. **Career Paths** (`career_paths.csv`)
**Use Case**: Career planning and professional development
- **Columns**: description, avg_salary, growth_outlook, education_required, work_life_balance, remote_friendly
- **Sample Queries**:
  - "I want a high-paying tech career with remote work options"
  - "What career has the best growth potential in the next 10 years?"
  - "I'm looking for a meaningful career that helps people"

### 5. **Housing Options** (`housing_options.csv`)
**Use Case**: Real estate and living situation decisions
- **Columns**: description, monthly_cost, location, size_sqft, commute_time, amenities
- **Sample Queries**:
  - "I need affordable housing with a short commute to downtown"
  - "What's the best family-friendly neighborhood with good schools?"
  - "I want luxury living with modern amenities"

### 6. **Fitness Programs** (`fitness_programs.csv`)
**Use Case**: Health and fitness planning
- **Columns**: description, monthly_cost, time_commitment, intensity_level, equipment_needed, location
- **Sample Queries**:
  - "I want an effective workout program that I can do at home"
  - "What's the best fitness option for building strength and community?"
  - "I need a low-impact exercise program for joint health"

## 🚀 How to Use These Datasets

### Option 1: Run the Demo Script
```bash
python demo_datasets.py
```
This will run automated demos for each dataset with sample queries.

### Option 2: Use the Streamlit App
```bash
streamlit run ui/app.py
```
1. Upload any of the CSV files
2. Enter your own query
3. Get AI-powered recommendations

### Option 3: Create Your Own Dataset
Follow this format for your CSV:
- **Required**: `description` column with detailed information about each option
- **Optional**: Add relevant columns like price, category, rating, etc.
- **Tips**: More detailed descriptions lead to better AI analysis

## 📝 Dataset Format Guidelines

### Essential Column
- **`description`**: Detailed text describing each option (required)

### Common Additional Columns
- **`price`/`cost`**: Numerical values for cost comparison
- **`category`**: Grouping similar options
- **`rating`**: Quality or satisfaction scores
- **`location`**: Geographic information
- **`difficulty`**: Complexity or skill level required

### Example Row
```csv
description,price,category,rating
"MacBook Air M2 with 8GB RAM, excellent battery life, perfect for students",1199,ultrabook,4.8
```

## 🎯 Query Examples by Category

### Technology Decisions
- "Best laptop for video editing under $2000"
- "Most reliable smartphone with great camera"
- "Budget-friendly tablet for reading and note-taking"

### Financial Planning
- "Conservative investment for retirement savings"
- "High-yield options for emergency fund"
- "Diversified portfolio for young investor"

### Lifestyle Choices
- "Romantic vacation destination in Europe"
- "Family-friendly activities for summer"
- "Adventure travel for solo backpacker"

### Career Development
- "High-growth career in technology"
- "Work-from-home friendly professions"
- "Careers that make a social impact"

## 🔧 Customization Tips

1. **Add Domain-Specific Columns**: Include metrics relevant to your decision
2. **Rich Descriptions**: More detail = better AI analysis
3. **Consistent Format**: Keep similar data types in each column
4. **Balanced Options**: Include variety in your choices for better comparison

## 📊 Data Quality Best Practices

- **Completeness**: Fill in as many relevant details as possible
- **Accuracy**: Ensure data reflects real-world options
- **Diversity**: Include options across different price points and categories
- **Relevance**: Focus on factors that matter for decision-making

Start with these samples and create your own datasets for any decision you need to make!