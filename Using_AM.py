import pandas as pd
import random
import numpy as np

file_path = r"C:\Users\ssath\OneDrive\Desktop\final_50000_dataset.csv"
limit = 50000  
max_team_size = 4

people_df = pd.read_csv(file_path).head(limit)


def experience_level(years):
    if years <= 3:
        return "Junior"
    elif years <= 5:
        return "Mid"
    else:
        return "Senior"

people_df["ExpLevel"] = people_df["Experience (Years)"].apply(experience_level)
people_df["Bucket"] = people_df["Job Role"].astype(str) + "_" + people_df["ExpLevel"]



bucket_skills, bucket_exp, buckets = {}, {}, {}
for bucket, members in people_df.groupby("Bucket"):
    buckets[bucket] = list(members.index)
    all_skills = set()
    for s in members["Skills"]:
        all_skills.update([x.strip().lower() for x in str(s).split(",") if x.strip()])
    bucket_skills[bucket] = all_skills
    bucket_exp[bucket] = members["Experience (Years)"].mean()

bucket_keys = list(buckets.keys())
n = len(bucket_keys)



adj_matrix = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if i == j:
            adj_matrix[i, j] = 1.0
        else:
            b1, b2 = bucket_keys[i], bucket_keys[j]
            s1, s2 = bucket_skills[b1], bucket_skills[b2]
            skill_overlap = len(s1 & s2) / len(s1 | s2) if (s1 | s2) else 0
            skill_div = 1 - skill_overlap
            role1, role2 = b1.split("_")[0], b2.split("_")[0]
            role_div = 1 if role1 != role2 else 0.5
            exp1, exp2 = bucket_exp[b1], bucket_exp[b2]
            exp_sim = max(0, 1 - abs(exp1 - exp2) / 10)
            score = round(0.4 * skill_div + 0.3 * role_div + 0.3 * exp_sim, 2)
            adj_matrix[i, j] = score

# Save Adjacency Matrix
adj_df = pd.DataFrame(adj_matrix, index=bucket_keys, columns=bucket_keys)
adj_df.to_csv("adjacency_matrix.csv")
print("Adjacency Matrix saved to adjacency_matrix.csv")



num_teams = (len(people_df) + max_team_size - 1) // max_team_size
teams = [[] for _ in range(num_teams)]
idx = 0
for bucket, members in sorted(buckets.items(), key=lambda x: -len(x[1])):
    random.shuffle(members)
    for p in members:
        team_id = idx % num_teams
        if len(teams[team_id]) < max_team_size:
            teams[team_id].append(p)
        else:
            for t in range(num_teams):
                if len(teams[t]) < max_team_size:
                    teams[t].append(p)
                    break
        idx += 1

team_out = []
for t_id, members in enumerate(teams, 1):
    for p in members:
        team_out.append([t_id, people_df.iloc[p]["Name"]])
pd.DataFrame(team_out, columns=["Team", "Member"]).to_csv("final_teams_AM.csv", index=False)
print("Final Teams saved to final_teams_AM.csv")




summary = []
bucket_index_map = {b: i for i, b in enumerate(bucket_keys)}

for t_id, members in enumerate(teams, 1):
    if not members:
        continue
    subset = people_df.iloc[members]
    avg_exp = subset["Experience (Years)"].mean()
    roles = {}
    for r in subset["Job Role"]:
        if r in roles:
            roles[r] += 1
        else:
            roles[r] = 1

    all_skills = set()
    for s in subset["Skills"]:
        all_skills.update([x.strip().lower() for x in str(s).split(",") if x.strip()])

    
    buckets_in_team = list(subset["Bucket"].unique())
    scores = []
    for i in range(len(buckets_in_team)):
        for j in range(i + 1, len(buckets_in_team)):
            b1, b2 = buckets_in_team[i], buckets_in_team[j]
            if b1 in bucket_index_map and b2 in bucket_index_map:
                scores.append(adj_matrix[bucket_index_map[b1], bucket_index_map[b2]])

    team_score = round(sum(scores) / len(scores), 3) if scores else 0
    summary.append([
        t_id,
        len(subset),
        round(avg_exp, 2),
        roles,
        len(all_skills),
        team_score
    ])

pd.DataFrame(summary, columns=[
    "Team", "Size", "AvgExperience", "RoleDistribution", "UniqueSkills", "CompatibilityScore"
]).to_csv("team_summary_AM.csv", index=False)

print("Team Summary with Compatibility Scores saved to team_summary_AM.csv")
