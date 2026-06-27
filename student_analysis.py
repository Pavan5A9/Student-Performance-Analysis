"""
Student Performance Analysis

Author: Patturi Pavan Kumar

Description:
This project analyzes student marks using Python, Pandas,
NumPy, Matplotlib, and Seaborn. It calculates average scores,
assigns grades, performs statistical analysis, and visualizes
performance metrics.
"""

# --------------------------------------------------
# Import Libraries
# --------------------------------------------------
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for professional charts
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------
def calculate_grade(avg):
    """
    Assigns a letter grade based on the average marks.
    """
    if avg >= 90:
        return 'A'
    elif avg >= 75:
        return 'B'
    elif avg >= 60:
        return 'C'
    else:
        return 'D'

# --------------------------------------------------
# Main Function
# --------------------------------------------------
def main():
    # --------------------------------------------------
    # Load Dataset
    # --------------------------------------------------
    csv_file = "students.csv"
    print("--------------------------------------------------")
    print(f"Loading Dataset: {csv_file}")
    print("--------------------------------------------------")
    
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
        print("Please run the script in the directory containing the dataset.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while loading the dataset: {e}")
        return

    # --------------------------------------------------
    # Explore Dataset
    # --------------------------------------------------
    print("\n[Raw Dataset preview (first 5 rows)]:")
    print(df.head())

    print("\n[Dataset Info]:")
    df.info()

    print("\n[Statistical Summary (Numeric Columns)]:")
    print(df.describe())

    # --------------------------------------------------
    # Data Processing
    # --------------------------------------------------
    print("\nProcessing student data...")
    # Calculate average scores using Pandas mean (axis=1 is row-wise)
    df['Average'] = df[['Math', 'Science', 'English']].mean(axis=1)

    # Assign grades using the refactored function
    df['Grade'] = df['Average'].apply(calculate_grade)

    # Calculate status (Pass/Fail) - Pass if each subject is >= 40
    df['Status'] = np.where(
        (df['Math'] >= 40) & (df['Science'] >= 40) & (df['English'] >= 40), 
        'Pass', 
        'Fail'
    )

    print("\n[Processed Dataset Preview]:")
    print(df.head())

    # --------------------------------------------------
    # Advanced Data Analysis
    # --------------------------------------------------
    print("\n" + "="*50)
    print("             ADVANCED DATA ANALYSIS REPORT        ")
    print("="*50)

    # 1. Subject-wise Maximum and Minimum Marks
    subjects = ['Math', 'Science', 'English']
    print("\n[Subject Statistics]:")
    for sub in subjects:
        max_mark = df[sub].max()
        min_mark = df[sub].min()
        avg_mark = df[sub].mean()
        print(f" - {sub:7s} | Avg: {avg_mark:.2f} | Max: {max_mark} | Min: {min_mark}")

    # 2. Class Average and Top Student
    class_average = df['Average'].mean()
    top_student_idx = df['Average'].idxmax()
    top_student = df.loc[top_student_idx]

    # 3. Overall Highest and Lowest Average Marks
    highest_avg = df['Average'].max()
    lowest_avg = df['Average'].min()

    # 4. Pass Percentage
    pass_count = df[df['Status'] == 'Pass'].shape[0]
    total_students = df.shape[0]
    pass_percentage = (pass_count / total_students) * 100

    print(f"\n[Overall Class Metrics]:")
    print(f" - Class Average Score : {class_average:.2f}")
    print(f" - Highest Avg Score   : {highest_avg:.2f}")
    print(f" - Lowest Avg Score    : {lowest_avg:.2f}")
    print(f" - Total Pass Count    : {pass_count} / {total_students} ({pass_percentage:.1f}%)")
    
    print(f"\n[Top Performing Student]:")
    print(f" - Name     : {top_student['Name']}")
    print(f" - Avg Score: {top_student['Average']:.2f}")
    print(f" - Grade    : {top_student['Grade']}")
    print(f" - Marks    : Math: {top_student['Math']}, Science: {top_student['Science']}, English: {top_student['English']}")
    print("="*50)

    # --------------------------------------------------
    # Save Processed Dataset
    # --------------------------------------------------
    output_csv = "student_analysis.csv"
    try:
        df.to_csv(output_csv, index=False)
        print(f"\nSuccessfully saved processed dataset to '{output_csv}'")
    except Exception as e:
        print(f"Error saving processed dataset: {e}")

    # --------------------------------------------------
    # Data Visualization
    # --------------------------------------------------
    print("\nGenerating charts...")

    # 1. Bar Chart - Average Marks
    plt.figure(figsize=(10, 6))
    plt.bar(
        df["Name"],
        df["Average"],
        color="skyblue",
        edgecolor="black",
        alpha=0.9
    )
    plt.axhline(class_average, color='red', linestyle='--', label=f'Class Avg ({class_average:.1f})')
    plt.title("Average Marks of Students", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Students", fontsize=12)
    plt.ylabel("Average Marks", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 110)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("average_marks.png", dpi=300)
    plt.close()
    print(" - Saved: average_marks.png")

    # 2. Pie Chart - Grade Distribution
    plt.figure(figsize=(8, 6))
    grade_counts = df['Grade'].value_counts().reindex(['A', 'B', 'C', 'D']).dropna()
    colors = ["gold", "lightgreen", "orange", "tomato"]
    # map colors to actual present grades
    present_grades = grade_counts.index.tolist()
    mapped_colors = [colors[['A', 'B', 'C', 'D'].index(g)] for g in present_grades]

    plt.pie(
        grade_counts, 
        labels=present_grades,
        autopct='%1.1f%%',
        colors=mapped_colors,
        startangle=140,
        wedgeprops={'edgecolor': 'black', 'linewidth': 1, 'antialiased': True}
    )
    plt.title("Grade Distribution", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig("grade_distribution.png", dpi=300)
    plt.close()
    print(" - Saved: grade_distribution.png")

    # 3. Line Plot - Subject comparison
    plt.figure(figsize=(12, 6))
    plt.plot(df['Name'], df['Math'], label='Math', color='royalblue', marker='o', linewidth=2)
    plt.plot(df['Name'], df['Science'], label='Science', color='forestgreen', marker='s', linewidth=2)
    plt.plot(df['Name'], df['English'], label='English', color='crimson', marker='^', linewidth=2)
    plt.title("Subject-wise Performance Trend", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Students", fontsize=12)
    plt.ylabel("Marks", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 110)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("subject_comparison.png", dpi=300)
    plt.close()
    print(" - Saved: subject_comparison.png")

    # 4. Box Plot - Marks distribution by subject (New Chart)
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df[['Math', 'Science', 'English']], palette="Set2")
    plt.title("Marks Distribution across Subjects", fontsize=14, fontweight='bold', pad=15)
    plt.ylabel("Marks", fontsize=12)
    plt.xlabel("Subjects", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig("subject_box_plot.png", dpi=300)
    plt.close()
    print(" - Saved: subject_box_plot.png")

    # 5. Scatter Plot - Math vs Science correlation (New Chart)
    plt.figure(figsize=(8, 6))
    sns.regplot(
        x='Math', 
        y='Science', 
        data=df, 
        scatter_kws={'color': 'darkcyan', 's': 60, 'alpha': 0.8},
        line_kws={'color': 'red', 'linewidth': 1.5}
    )
    plt.title("Correlation between Math and Science Marks", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Math Marks", fontsize=12)
    plt.ylabel("Science Marks", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig("math_vs_science_scatter.png", dpi=300)
    plt.close()
    print(" - Saved: math_vs_science_scatter.png")

    # 6. Heatmap - Correlation Matrix (New Chart)
    plt.figure(figsize=(6, 5))
    corr_matrix = df[['Math', 'Science', 'English', 'Average']].corr()
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        cmap="coolwarm", 
        fmt=".2f", 
        linewidths=.5, 
        vmin=-1, 
        vmax=1,
        square=True
    )
    plt.title("Subject Score Correlation Matrix", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig("subject_correlation_heatmap.png", dpi=300)
    plt.close()
    print(" - Saved: subject_correlation_heatmap.png")

    # 7. Horizontal Bar Plot - Top 5 Students (New Chart)
    plt.figure(figsize=(8, 5))
    top_5 = df.nlargest(5, 'Average').sort_values('Average', ascending=True)
    plt.barh(
        top_5['Name'], 
        top_5['Average'], 
        color='teal', 
        edgecolor='black', 
        height=0.6,
        alpha=0.85
    )
    plt.title("Top 5 Students by Average Score", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Average Score", fontsize=12)
    plt.ylabel("Students", fontsize=12)
    plt.xlim(0, 110)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig("top_students_horizontal.png", dpi=300)
    plt.close()
    print(" - Saved: top_students_horizontal.png")

    # 8. Histogram - Average Marks Distribution (New Chart)
    plt.figure(figsize=(8, 5))
    sns.histplot(
        df['Average'], 
        bins=8, 
        kde=True, 
        color='purple', 
        edgecolor='black',
        alpha=0.6
    )
    plt.title("Distribution of Student Average Scores", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Average Score", fontsize=12)
    plt.ylabel("Number of Students", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig("average_marks_histogram.png", dpi=300)
    plt.close()
    print(" - Saved: average_marks_histogram.png")

    print("\nAll tasks completed successfully!")

if __name__ == "__main__":
    main()
