#!/usr/bin/env python
# coding: utf-8

# In[2674]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])


# In[2675]:


#Variables for the District Summary Statistics - Part 1
total_schools = len(school_data_complete["school_name"].unique())
total_students = len(school_data_complete["student_name"])
total_budget = school_data["budget"].sum()
average_math_score = school_data_complete["math_score"].mean()
average_reading_score = school_data_complete["reading_score"].mean()


# In[2676]:


#Calculations for the Percentage Passing Variables below - extra steps to make sure data is clean and complete
passing_math_df = school_data_complete.loc[school_data_complete["math_score"] >=70,:]
number_passing_math = len(passing_math_df)
impossible_score_math_df = school_data_complete.loc[(school_data_complete["math_score"] <0) | (school_data_complete["math_score"] > 100),:]
not_shown_taken_math = len (impossible_score_math_df)
total_shown_taken_math = total_students - not_shown_taken_math

passing_reading_df = school_data_complete.loc[school_data_complete["reading_score"] >=70,:]
number_passing_reading = len(passing_reading_df)
impossible_score_reading_df = school_data_complete.loc[(school_data_complete["reading_score"] <0) | (school_data_complete["reading_score"] > 100),:]
not_shown_taken_reading = len (impossible_score_reading_df)
total_shown_taken_reading = total_students - not_shown_taken_math


# In[2677]:


#Variables for the District Summary Statistics - Part 2 - Percentage of Students Passing Variables
perc_passing_math = number_passing_math/total_shown_taken_math
perc_passing_reading = number_passing_reading/total_shown_taken_reading

#This line below would be the overall passrate, but the direction specifically ask for averaging the total reading and math final percentages instead of a real overall average
#perc_overall_passing = (number_passing_math + number_passing_reading)/(total_shown_taken_math + total_shown_taken_reading)

#Overall average based on the instructions:
perc_overall_passing=(perc_passing_math+perc_passing_reading)/2


# In[2678]:


#This creates the data frame for the Distric Summary

district_summary_df = pd.DataFrame({ "Total Schools": [total_schools], "Total Students": [total_students], "Total Budget": [total_budget], "Average Math Score": [average_math_score], "Average Reading Score": [average_reading_score], "% Passing Math": [perc_passing_math], "% Passing Reading": [perc_passing_reading], "% Overall Passing Rate":[perc_overall_passing]})


# In[2679]:


# Formatting Columns for District Summary 

district_summary_df["Total Schools"] = district_summary_df["Total Schools"].map("{:,}".format) 
district_summary_df["Total Students"] = district_summary_df["Total Students"].map("{:,}".format) 
district_summary_df["Total Budget"] = district_summary_df["Total Budget"].map("${:,.2f}".format)
district_summary_df["Average Math Score"] = district_summary_df["Average Math Score"].map("{:.3f}".format) 
district_summary_df["Average Reading Score"] = district_summary_df["Average Reading Score"].map("{:.3f}".format) 
district_summary_df["% Passing Math"] = district_summary_df["% Passing Math"].map("{:.3%}".format) 
district_summary_df["% Passing Reading"] = district_summary_df["% Passing Reading"].map("{:.3%}".format) 
district_summary_df["% Overall Passing Rate"] = district_summary_df["% Overall Passing Rate"].map("{:.3%}".format) 


# In[2680]:


#Report for District Summary

district_summary_df.head(10)


# In[2681]:


# This starts the School Summary Section

#This adds a column for Spending Per Student 
school_data_complete["Per Student Budget"] = school_data_complete["budget"]/school_data_complete["size"]


# In[2682]:


grouped_by_school = school_data_complete.groupby(['school_name'])


# In[2683]:


school_type = grouped_by_school["type"].unique().apply(', '.join)


# In[2684]:


student_count_by_school = grouped_by_school["student_name"].count()


# In[2685]:


budget_by_school = grouped_by_school["budget"].max()


# In[2686]:


per_student_budget_by_school = grouped_by_school["Per Student Budget"].max()


# In[2687]:


ave_math_by_school = grouped_by_school["math_score"].mean()


# In[2688]:


ave_reading_by_school = grouped_by_school["reading_score"].mean()


# In[2689]:


passing_math_by_school = passing_math_df.groupby(['school_name'])
perc_passing_math_by_school = passing_math_by_school["math_score"].count()/grouped_by_school["math_score"].count()


# In[2690]:


passing_reading_by_school = passing_reading_df.groupby(['school_name'])
perc_passing_reading_by_school = passing_reading_by_school["reading_score"].count()/grouped_by_school["reading_score"].count()


# In[2691]:


average_math_reading_together_by_school = pd.DataFrame({"% Overall Passing Rate":(perc_passing_math_by_school+perc_passing_reading_by_school)/2})


# In[2692]:


#Merging all the dataframes together into the School Summary dataframe for the report

school_summary_df = pd.merge(school_type, student_count_by_school, how="outer", on=["school_name"])
school_summary_df = pd.merge(school_summary_df, budget_by_school, how="outer", on=["school_name"])
school_summary_df = pd.merge(school_summary_df, per_student_budget_by_school, how="outer", on=["school_name"])
school_summary_df = pd.merge(school_summary_df, ave_math_by_school, how="outer", on=["school_name"])
school_summary_df = pd.merge(school_summary_df, ave_reading_by_school, how="outer", on=["school_name"])
school_summary_df = pd.merge(school_summary_df, perc_passing_math_by_school, how="outer", on=["school_name"])
school_summary_df = pd.merge(school_summary_df, perc_passing_reading_by_school, how="outer", on=["school_name"])
school_summary_df = pd.merge(school_summary_df, average_math_reading_together_by_school, how="outer", on=["school_name"])


# In[2693]:


# Change column names
school_summary_df=school_summary_df.rename(columns={"type": "School Type", "student_name": "Total Students", "budget": "Total School Budget", "math_score_x":"Average Math Score","reading_score_x":"Average Reading Score","math_score_y":"% Passing Math","reading_score_y":"% Passing Reading"})


# In[2694]:


#This is to fix the "school_name" being seen above the index of school names when printed

school_summary_df=school_summary_df.set_index([pd.Index(school_data_complete["school_name"].unique())])


# In[2695]:


#Formatting columns
 
school_summary_df["Total Students"] = school_summary_df["Total Students"].map("{:,}".format) 
school_summary_df["Total School Budget"] = school_summary_df["Total School Budget"].map("${:,.2f}".format)
school_summary_df["Per Student Budget"] = school_summary_df["Per Student Budget"].map("${:,.2f}".format)
school_summary_df["Average Math Score"] = school_summary_df["Average Math Score"].map("{:.3f}".format) 
school_summary_df["Average Reading Score"] = school_summary_df["Average Reading Score"].map("{:.3f}".format) 
school_summary_df["% Passing Math"] = school_summary_df["% Passing Math"].map("{:.3%}".format) 
school_summary_df["% Passing Reading"] = school_summary_df["% Passing Reading"].map("{:.3%}".format) 
school_summary_df["% Overall Passing Rate"] = school_summary_df["% Overall Passing Rate"].map("{:.3%}".format) 


# In[2696]:


#This sorts for the schools with the highest Overall Passing Rate at the top

Top_Performing_schools = school_summary_df.sort_values(["% Overall Passing Rate"], ascending=False)


# In[2697]:


# Report for Top Performing Schools (By Passing Rate): Sort and display the top five schools in overall passing rate

Top_Performing_schools.head(5)


# In[2698]:


#This sorts for the schools with the lowest Overall Passing Rate at the top

Bottom_Performing_schools = school_summary_df.sort_values(["% Overall Passing Rate"], ascending=True)


# In[2699]:


# Report for Bottom Performing Schools (By Passing Rate): Sort and display the five worst-performing schools

Bottom_Performing_schools.head(5)


# In[2700]:


# This starts the Scores by Grade Section

#Filtering the complete data frame by grade levels

grade9_only = school_data_complete.loc[school_data_complete["grade"] == "9th",:]
grade10_only = school_data_complete.loc[school_data_complete["grade"] == "10th",:]
grade11_only = school_data_complete.loc[school_data_complete["grade"] == "11th",:]
grade12_only = school_data_complete.loc[school_data_complete["grade"] == "12th",:]


# In[2701]:


#This groups by school the data tables that have already been filtered by grade above

grade9_grouped_by_school = grade9_only.groupby(['school_name'])
grade10_grouped_by_school = grade10_only.groupby(['school_name'])
grade11_grouped_by_school = grade11_only.groupby(['school_name'])
grade12_grouped_by_school = grade12_only.groupby(['school_name'])


# In[2702]:


# This condenses each grade's math averages by school for each grade

grade9_ave_math_by_school = grade9_grouped_by_school["math_score"].mean()
grade10_ave_math_by_school = grade10_grouped_by_school["math_score"].mean()
grade11_ave_math_by_school = grade11_grouped_by_school["math_score"].mean()
grade12_ave_math_by_school = grade12_grouped_by_school["math_score"].mean()


# In[2703]:


#Merging all the dataframes together into the Math Scores by Grade dataframe for the report

Math_Scores_by_Grade_df = pd.merge(grade9_ave_math_by_school, grade10_ave_math_by_school, how="outer", on=["school_name"], suffixes=("9th", "10th"))
Math_Scores_by_Grade_df = pd.merge(Math_Scores_by_Grade_df, grade11_ave_math_by_school, how="outer", on=["school_name"])
Math_Scores_by_Grade_df = pd.merge(Math_Scores_by_Grade_df, grade12_ave_math_by_school, how="outer", on=["school_name"])


# In[2704]:


# Change column names
Math_Scores_by_Grade_df=Math_Scores_by_Grade_df.rename(columns={"math_score9th": "9th", 
                                                    "math_score10th": "10th",
                                                    "math_score_x": "11th", "math_score_y":"12th"})


# In[2705]:


# This puts the schools (index) in alphabetical order
Math_Scores_by_Grade_df=Math_Scores_by_Grade_df.sort_index()


# In[2706]:


#This is to fix the "school_name" being seen above the index of school names when printed

Math_Scores_by_Grade_df=Math_Scores_by_Grade_df.reset_index()
Math_Scores_by_Grade_df = Math_Scores_by_Grade_df.rename(columns={"school_name": ""})
alphbetical_school_index=(Math_Scores_by_Grade_df[""])
Math_Scores_by_Grade_df=Math_Scores_by_Grade_df.set_index([pd.Index(alphbetical_school_index)])
del Math_Scores_by_Grade_df['']


# In[2707]:


#Formatting columns

Math_Scores_by_Grade_df["9th"] = Math_Scores_by_Grade_df["9th"].map("{:.3f}".format)
Math_Scores_by_Grade_df["10th"] = Math_Scores_by_Grade_df["10th"].map("{:.3f}".format) 
Math_Scores_by_Grade_df["11th"] = Math_Scores_by_Grade_df["11th"].map("{:.3f}".format) 
Math_Scores_by_Grade_df["12th"] = Math_Scores_by_Grade_df["12th"].map("{:.3f}".format) 


# In[2708]:


# Report for Math Scores by Grade

Math_Scores_by_Grade_df.head(20)


# In[2709]:


# This condenses each grade's reading averages by school for each grade

grade9_ave_reading_by_school = grade9_grouped_by_school["reading_score"].mean()
grade10_ave_reading_by_school = grade10_grouped_by_school["reading_score"].mean()
grade11_ave_reading_by_school = grade11_grouped_by_school["reading_score"].mean()
grade12_ave_reading_by_school = grade12_grouped_by_school["reading_score"].mean()


# In[2710]:


#Merging all the dataframes together into the Reading Scores by Grade dataframe for the report

Reading_Scores_by_Grade_df = pd.merge(grade9_ave_reading_by_school, grade10_ave_reading_by_school, how="outer", on=["school_name"], suffixes=("9th", "10th"))
Reading_Scores_by_Grade_df = pd.merge(Reading_Scores_by_Grade_df, grade11_ave_reading_by_school, how="outer", on=["school_name"])
Reading_Scores_by_Grade_df = pd.merge(Reading_Scores_by_Grade_df, grade12_ave_reading_by_school, how="outer", on=["school_name"])


# In[2711]:


# Change column names
Reading_Scores_by_Grade_df=Reading_Scores_by_Grade_df.rename(columns={"reading_score9th": "9th", 
                                                    "reading_score10th": "10th",
                                                    "reading_score_x": "11th", "reading_score_y":"12th"})


# In[2712]:


# This puts the schools (index) in alphabetical order
Reading_Scores_by_Grade_df=Reading_Scores_by_Grade_df.sort_index()


# In[2713]:


#This is to fix the "school_name" being seen above the index of school names when printed

Reading_Scores_by_Grade_df=Reading_Scores_by_Grade_df.reset_index()
Reading_Scores_by_Grade_df = Reading_Scores_by_Grade_df.rename(columns={"school_name": ""})
Reading_alphbetical_school_index=(Reading_Scores_by_Grade_df[""])
Reading_Scores_by_Grade_df=Reading_Scores_by_Grade_df.set_index([pd.Index(Reading_alphbetical_school_index)])
del Reading_Scores_by_Grade_df['']


# In[2714]:


#Formatting columns

Reading_Scores_by_Grade_df["9th"] = Reading_Scores_by_Grade_df["9th"].map("{:.3f}".format)
Reading_Scores_by_Grade_df["10th"] = Reading_Scores_by_Grade_df["10th"].map("{:.3f}".format) 
Reading_Scores_by_Grade_df["11th"] = Reading_Scores_by_Grade_df["11th"].map("{:.3f}".format) 
Reading_Scores_by_Grade_df["12th"] = Reading_Scores_by_Grade_df["12th"].map("{:.3f}".format) 


# In[2715]:


# Report for Reading Scores by Grade

Reading_Scores_by_Grade_df.head(20)


# In[2716]:


# For binning sections

#This adds a columns for passing math and/or reading with True/False
school_data_complete["Reading Pass T/F"] = school_data_complete["reading_score"] >=70
school_data_complete["Math Pass T/F"] = school_data_complete["math_score"] >=70


# In[2717]:


# Scores by School Spending

# Bins for chart
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]


# In[2719]:


# This saves a side version of the dataframe above for the sections that use binning after this one
new_col_added_full_data1=school_data_complete
new_col_added_full_data2=school_data_complete


# In[2720]:


#This adds a column for Spending Ranges (Per Student)

school_data_complete["Spending Ranges (Per Student)"] = pd.cut(school_data_complete["Per Student Budget"], spending_bins, labels=group_names, include_lowest=True)


# In[2721]:


# Creating a group based off of the bins 
school_data_complete_SpendingBins = school_data_complete.groupby("Spending Ranges (Per Student)")


# In[2722]:


#This captures the average reading and math scores per bin

SpendinBins_ave_scores=school_data_complete_SpendingBins[["math_score","reading_score"]].mean()


# In[2723]:


#This captures the the pass rate for reading and math scores per bin

#Math and Reading Separately
SpendinBins_trues_count=school_data_complete_SpendingBins[["Math Pass T/F","Reading Pass T/F"]].sum()
SpendinBins_total_count=school_data_complete_SpendingBins[["Math Pass T/F","Reading Pass T/F"]].count()
SpendinBins_separate_pass=SpendinBins_trues_count/SpendinBins_total_count
SpendinBins_separate_pass=SpendinBins_separate_pass.rename(columns={"Math Pass T/F":"% Passing Math","Reading Pass T/F":"% Passing Reading"})

#Overall - math and reading together
SpendinBins_BothTrues_count=SpendinBins_trues_count["Math Pass T/F"]+ SpendinBins_trues_count["Reading Pass T/F"]
SpendinBins_BothTotal_count=SpendinBins_total_count["Math Pass T/F"]+ SpendinBins_total_count["Reading Pass T/F"]
SpendinBins_overall_pass=SpendinBins_BothTrues_count/SpendinBins_BothTotal_count

#Converts series that was output from Overall - math and reading together into data frame
SpendinBins_overall_pass_df = pd.DataFrame(SpendinBins_overall_pass)


# In[2724]:


#Merging all the dataframes together into the Scores by School Spending dataframe for the report

Scores_by_SchoolSpending_df = pd.merge(SpendinBins_ave_scores, SpendinBins_separate_pass, how="outer", on=["Spending Ranges (Per Student)"], suffixes=("SpendinBins_ave_scores", "SpendinBins_ave_scores"))
Scores_by_SchoolSpending_df = pd.merge(Scores_by_SchoolSpending_df, SpendinBins_overall_pass_df, how="outer", on=["Spending Ranges (Per Student)"])


# In[2725]:


# Change column names
Scores_by_SchoolSpending_df=Scores_by_SchoolSpending_df.rename(columns={"math_score": "Average Math Score", 
                                                    "reading_score": "Average Reading Score",
                                                    "0": "% Overall Passing Rate"})
#This last column needed a special line to change it
Scores_by_SchoolSpending_df.rename(columns={Scores_by_SchoolSpending_df.columns[4]: "% Overall Passing Rate" }, inplace = True)


# In[2726]:


#Formatting columns

Scores_by_SchoolSpending_df["Average Math Score"] = Scores_by_SchoolSpending_df["Average Math Score"].map("{:.3f}".format)
Scores_by_SchoolSpending_df["Average Reading Score"] = Scores_by_SchoolSpending_df["Average Reading Score"].map("{:.3f}".format) 
Scores_by_SchoolSpending_df["% Passing Math"] = Scores_by_SchoolSpending_df["% Passing Math"].map("{:.3%}".format) 
Scores_by_SchoolSpending_df["% Passing Reading"] = Scores_by_SchoolSpending_df["% Passing Reading"].map("{:.3%}".format) 
Scores_by_SchoolSpending_df["% Overall Passing Rate"] = Scores_by_SchoolSpending_df["% Overall Passing Rate"].map("{:.3%}".format) 


# In[2727]:


Scores_by_SchoolSpending_df


# In[2728]:


# This starts section for Scores by School Size

# Bins for chart
size_bins1 = [0, 1000, 2000, 5000]
group_names1 = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[2729]:



#This adds a column for Spending Ranges (Per Student)

new_col_added_full_data1["School Size"] = pd.cut(new_col_added_full_data1["size"], size_bins1, labels=group_names1, include_lowest=True)


# In[2730]:


# Creating a group based off of the bins 
new_col_added_full_data1_SpendingBins = new_col_added_full_data1.groupby("School Size")


# In[2731]:


#This captures the average reading and math scores per bin

SpendinBins_ave_scores1=new_col_added_full_data1_SpendingBins[["math_score","reading_score"]].mean()


# In[2732]:


#This captures the the pass rate for reading and math scores per bin

#Math and Reading Separately
SpendinBins_trues_count1=new_col_added_full_data1_SpendingBins[["Math Pass T/F","Reading Pass T/F"]].sum()
SpendinBins_total_count1=new_col_added_full_data1_SpendingBins[["Math Pass T/F","Reading Pass T/F"]].count()
SpendinBins_separate_pass1=SpendinBins_trues_count1/SpendinBins_total_count1
SpendinBins_separate_pass1=SpendinBins_separate_pass1.rename(columns={"Math Pass T/F":"% Passing Math","Reading Pass T/F":"% Passing Reading"})

#Overall - math and reading together
SpendinBins_BothTrues_count1=SpendinBins_trues_count1["Math Pass T/F"]+ SpendinBins_trues_count1["Reading Pass T/F"]
SpendinBins_BothTotal_count1=SpendinBins_total_count1["Math Pass T/F"]+ SpendinBins_total_count1["Reading Pass T/F"]
SpendinBins_overall_pass1=SpendinBins_BothTrues_count1/SpendinBins_BothTotal_count1

#Converts series that was output from Overall - math and reading together into data frame
SpendinBins_overall_pass_df1 = pd.DataFrame(SpendinBins_overall_pass1)


# In[2733]:


#Merging all the dataframes together into the Scores by School Spending dataframe for the report

Scores_by_SchoolSpending_df1 = pd.merge(SpendinBins_ave_scores1, SpendinBins_separate_pass1, how="outer", on=["School Size"], suffixes=("SpendinBins_ave_scores", "SpendinBins_ave_scores"))
Scores_by_SchoolSpending_df1 = pd.merge(Scores_by_SchoolSpending_df1, SpendinBins_overall_pass_df1, how="outer", on=["School Size"])


# In[2734]:


# Change column names
Scores_by_SchoolSpending_df1=Scores_by_SchoolSpending_df1.rename(columns={"math_score": "Average Math Score", 
                                                    "reading_score": "Average Reading Score",
                                                    "0": "% Overall Passing Rate"})
#This last column needed a special line to change it
Scores_by_SchoolSpending_df1.rename(columns={Scores_by_SchoolSpending_df1.columns[4]: "% Overall Passing Rate" }, inplace = True)


# In[2735]:


#Formatting columns

Scores_by_SchoolSpending_df1["Average Math Score"] = Scores_by_SchoolSpending_df1["Average Math Score"].map("{:.3f}".format)
Scores_by_SchoolSpending_df1["Average Reading Score"] = Scores_by_SchoolSpending_df1["Average Reading Score"].map("{:.3f}".format) 
Scores_by_SchoolSpending_df1["% Passing Math"] = Scores_by_SchoolSpending_df1["% Passing Math"].map("{:.3%}".format) 
Scores_by_SchoolSpending_df1["% Passing Reading"] = Scores_by_SchoolSpending_df1["% Passing Reading"].map("{:.3%}".format) 
Scores_by_SchoolSpending_df1["% Overall Passing Rate"] = Scores_by_SchoolSpending_df1["% Overall Passing Rate"].map("{:.3%}".format) 


# In[2736]:


# Report for Scores by School Size

Scores_by_SchoolSpending_df1


# In[2737]:


#This starts Scores by School Type

type_bins_df=new_col_added_full_data2.groupby("type")


# In[2738]:


SpendinBins_ave_scores2=type_bins_df[["math_score","reading_score"]].mean()


# In[2739]:


#This captures the the pass rate for reading and math scores per bin

#Math and Reading Separately
SpendinBins_trues_count2=type_bins_df[["Math Pass T/F","Reading Pass T/F"]].sum()
SpendinBins_total_count2=type_bins_df[["Math Pass T/F","Reading Pass T/F"]].count()
SpendinBins_separate_pass2=SpendinBins_trues_count2/SpendinBins_total_count2
SpendinBins_separate_pass2=SpendinBins_separate_pass2.rename(columns={"Math Pass T/F":"% Passing Math","Reading Pass T/F":"% Passing Reading"})

#Overall - math and reading together
SpendinBins_BothTrues_count2=SpendinBins_trues_count2["Math Pass T/F"]+ SpendinBins_trues_count2["Reading Pass T/F"]
SpendinBins_BothTotal_count2=SpendinBins_total_count2["Math Pass T/F"]+ SpendinBins_total_count2["Reading Pass T/F"]
SpendinBins_overall_pass2=SpendinBins_BothTrues_count2/SpendinBins_BothTotal_count2

#Converts series that was output from Overall - math and reading together into data frame
SpendinBins_overall_pass_df2 = pd.DataFrame(SpendinBins_overall_pass2)


# In[2740]:


#Merging all the dataframes together into the Scores by School Spending dataframe for the report

Scores_by_SchoolSpending_df2 = pd.merge(SpendinBins_ave_scores2, SpendinBins_separate_pass2, how="outer", on=["type"], suffixes=("SpendinBins_ave_scores", "SpendinBins_ave_scores"))
Scores_by_SchoolSpending_df2 = pd.merge(Scores_by_SchoolSpending_df2, SpendinBins_overall_pass_df2, how="outer", on=["type"])


# In[2741]:


# Change column names
Scores_by_SchoolSpending_df2=Scores_by_SchoolSpending_df2.rename(columns={"math_score": "Average Math Score", 
                                                    "reading_score": "Average Reading Score",
                                                    "0": "% Overall Passing Rate"})
#This last column needed a special line to change it
Scores_by_SchoolSpending_df2.rename(columns={Scores_by_SchoolSpending_df2.columns[4]: "% Overall Passing Rate" }, inplace = True)


# In[2742]:


#Formatting columns

Scores_by_SchoolSpending_df2["Average Math Score"] = Scores_by_SchoolSpending_df2["Average Math Score"].map("{:.3f}".format)
Scores_by_SchoolSpending_df2["Average Reading Score"] = Scores_by_SchoolSpending_df2["Average Reading Score"].map("{:.3f}".format) 
Scores_by_SchoolSpending_df2["% Passing Math"] = Scores_by_SchoolSpending_df2["% Passing Math"].map("{:.3%}".format) 
Scores_by_SchoolSpending_df2["% Passing Reading"] = Scores_by_SchoolSpending_df2["% Passing Reading"].map("{:.3%}".format) 
Scores_by_SchoolSpending_df2["% Overall Passing Rate"] = Scores_by_SchoolSpending_df2["% Overall Passing Rate"].map("{:.3%}".format) 


# In[2743]:


# Report for Scores by School Type

Scores_by_SchoolSpending_df2


# In[2744]:


# Below is a method for the above binning that is for extra practice


# In[2745]:


##### Please NOTE: Jupyter Lab does not allow Method definitions to be split between cells

#This method is for the binning sections because they all are asking for a similar actions

def ScoresByMethod(x_bins,group_names,col_name_split,col_name_output):
 In_Method_school_data_complete=school_data_complete
 In_Method_school_data_complete[col_name_output] = pd.cut(In_Method_school_data_complete[col_name_split], x_bins, labels=group_names, include_lowest=True)
 
 # Creating a group based off of the bins 
 school_data_complete_WithBins = In_Method_school_data_complete.groupby(col_name_output)
    
 #This captures the average reading and math scores per bin
 WithBins_ave_scores=school_data_complete_WithBins[["math_score","reading_score"]].mean()

 ##### Please NOTE: Jupyter Lab does not allow Method definitions to be split between cells

 #This captures the the pass rate for reading and math scores per bin

 #Math and Reading Separately
 WithBins_trues_count=school_data_complete_WithBins[["Math Pass T/F","Reading Pass T/F"]].sum()
 WithBins_total_count=school_data_complete_WithBins[["Math Pass T/F","Reading Pass T/F"]].count()
 WithBins_separate_pass=WithBins_trues_count/SpendinBins_total_count
 WithBins_separate_pass=WithBins_separate_pass.rename(columns={"Math Pass T/F":"% Passing Math","Reading Pass T/F":"% Passing Reading"})

 #Overall - math and reading together
 WithBins_BothTrues_count=WithBins_trues_count["Math Pass T/F"]+ WithBins_trues_count["Reading Pass T/F"]
 WithBins_BothTotal_count=WithBins_total_count["Math Pass T/F"]+ WithBins_total_count["Reading Pass T/F"]
 WithBins_overall_pass=WithBins_BothTrues_count/WithBins_BothTotal_count

 #Converts series that was output from Overall - math and reading together into data frame
 WithBins_overall_pass_df = pd.DataFrame(WithBins_overall_pass)
 
 #Merging all the dataframes together into the Scores by School Spending dataframe for the report

 df_returned = pd.merge(WithBins_ave_scores, WithBins_separate_pass, how="outer", on=[col_name_output])
 df_returned = pd.merge(df_returned, WithBins_overall_pass_df, how="outer", on=[col_name_output])

 # Change column names
 df_returned=df_returned.rename(columns={"math_score": "Average Math Score", 
                                                     "reading_score": "Average Reading Score",
                                                     "0": "% Overall Passing Rate"})
 #This last column needed a special line to change it
 df_returned.rename(columns={df_returned.columns[4]: "% Overall Passing Rate" }, inplace = True)
 
  #Formatting columns

 df_returned["Average Math Score"] = df_returned["Average Math Score"].map("{:.3f}".format)
 df_returned["Average Reading Score"] = df_returned["Average Reading Score"].map("{:.3f}".format) 
 df_returned["% Passing Math"] = df_returned["% Passing Math"].map("{:.3%}".format) 
 df_returned["% Passing Reading"] = df_returned["% Passing Reading"].map("{:.3%}".format) 
 df_returned["% Overall Passing Rate"] = df_returned["% Overall Passing Rate"].map("{:.3%}".format) 

 return df_returned.head()


# In[2746]:


# Scores by School Spending

# Bins for chart
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]


# In[2747]:


# Scores by School Spending Report done by calling method above

## This has a duplicate output to the Scores by School Spending Report above this section - this is for extra practice

ScoresByMethod(spending_bins,group_names,"Per Student Budget","Spending Ranges (Per Student)")

