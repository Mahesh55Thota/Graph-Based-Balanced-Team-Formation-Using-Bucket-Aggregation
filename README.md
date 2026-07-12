# Graph-Based Balanced Team Formation Using Bucket Aggregation

## Project Overview

This project implements a **Graph-Based Balanced Team Formation** algorithm that automatically creates balanced teams from a dataset of employees or candidates.

The algorithm considers:

- Job Role
- Technical Skills
- Experience Level

Instead of randomly assigning members, the system groups candidates into buckets based on their role and experience, constructs a compatibility graph between buckets, and distributes members evenly to create balanced teams.

---

## Objective

The objective of this project is to form balanced teams by ensuring:

- Diverse job roles
- Balanced experience levels
- Wide range of technical skills
- Fair distribution of candidates
- Compatibility analysis between team members

---

## Features

- Reads employee dataset from CSV
- Categorizes candidates into experience levels
- Bucket Aggregation based on Role + Experience
- Graph construction using compatibility scores
- Balanced team formation
- Team compatibility score calculation
- Team summary generation
- CSV output generation

---

## Technologies Used

- Python 3.x
- Pandas
- Random Module

---

## Data Structures Used

### Graph

Graph is used to represent compatibility between buckets.

Each node represents:

```
Role + Experience Level
```

Example:

```
Developer_Junior
Developer_Mid
Tester_Senior
Designer_Mid
```

Edges connect two buckets.

Each edge stores a compatibility score.

---

### Dictionary

Used for

- Bucket storage
- Skills storage
- Experience storage
- Team information

---

### List

Used for

- Team members
- Graph edges
- Skills
- Final outputs

---

## Algorithm

### Step 1

Load employee dataset.

---

### Step 2

Classify experience into

- Junior
- Mid
- Senior

---

### Step 3

Create Buckets

Bucket format:

```
JobRole_ExperienceLevel
```

Example

```
Developer_Junior
Tester_Mid
Manager_Senior
```

---

### Step 4

Build Graph

Each bucket becomes one graph node.

Compatibility score is calculated using

- Skill Diversity
- Role Diversity
- Experience Similarity

Compatibility Formula

```
Compatibility Score =
0.4 × Skill Diversity
+
0.3 × Role Diversity
+
0.3 × Experience Similarity
```

---

### Step 5

Balanced Team Formation

Members from each bucket are evenly distributed across all teams.

This ensures

- balanced skills
- balanced experience
- balanced job roles

---

### Step 6

Calculate Team Compatibility

Average compatibility score of bucket pairs inside each team.

---

### Step 7

Generate Outputs

The project generates

- Final Teams CSV
- Team Summary CSV

---

## Input

CSV file containing

| Column |
|---------|
| Name |
| Job Role |
| Experience (Years) |
| Skills |

---

## Outputs

### 1. Final Teams

Contains

- Team Number
- Member Name

Example

| Team | Member |
|------|---------|
| 1 | Member 1 |
| 1 | Member 2 |
| 2 | Member 3 |

---

### 2. Team Summary

Contains

- Team Number
- Team Size
- Average Experience
- Role Distribution
- Unique Skills
- Compatibility Score

Example

| Team | Size | Avg Experience | Compatibility |
|------|------|----------------|---------------|
| 1 | 4 | 5.2 | 0.84 |

---

## Project Structure

```
Project
│
├── team_algorithm.py
├── input_dataset.csv
├── final_teams.csv
├── team_summary.csv
├── README.md
```

---

## Advantages

- Balanced team formation
- Skill diversity
- Role diversity
- Experience balancing
- Graph-based compatibility analysis
- Simple implementation
- Efficient for large datasets

---

## Future Enhancements

- Machine Learning based compatibility prediction
- Team performance prediction
- Real-time team generation
- Interactive web interface
- Database integration

---

## Author

Student Project

Department of Computer Science

Graph-Based Balanced Team Formation Using Bucket Aggregation
