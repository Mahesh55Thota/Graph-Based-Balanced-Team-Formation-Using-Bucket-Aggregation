import pandas as pd
import random

file_path = r"C:\Users\peddi\OneDrive\Desktop\dsa_project\final_50000_dataset.csv"
limit = 50000  
min_team_size = 2
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



adj_list = {b: [] for b in bucket_keys}  # plain dict instead of defaultdict
edges = []

for i in range(len(bucket_keys)):
    for j in range(i + 1, len(bucket_keys)):
        b1, b2 = bucket_keys[i], bucket_keys[j]
        s1, s2 = bucket_skills[b1], bucket_skills[b2]
        skill_overlap = len(s1 & s2) / len(s1 | s2) if (s1 | s2) else 0
        skill_div = 1 - skill_overlap
        role1, role2 = b1.split("_")[0], b2.split("_")[0]
        role_div = 1 if role1 != role2 else 0.5
        exp1, exp2 = bucket_exp[b1], bucket_exp[b2]
        exp_sim = max(0, 1 - abs(exp1 - exp2) / 10)
        score = round(0.4*skill_div + 0.3*role_div + 0.3*exp_sim, 2)
        adj_list[b1].append((b2, score))
        adj_list[b2].append((b1, score))
        edges.append([b1, b2, score])



adjacency_data = []
for bucket in adj_list:
    neighbours_text = ""
    for neighbour, score in adj_list[bucket]:
        neighbours_text += f"{neighbour} ({score}), "
    neighbours_text = neighbours_text.rstrip(", ")  

    adjacency_data.append([bucket, neighbours_text])

adjacency_df = pd.DataFrame(adjacency_data, columns=["Bucket", "Neighbors"])
adjacency_df.to_csv("adjacency_list.csv", index=False)
print("Adjacency List saved to adjacency_list.csv in correct format")




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
            # find next available team
            for t in range(num_teams):
                if len(teams[t]) < max_team_size:
                    teams[t].append(p)
                    break
        idx += 1


team_out = []
for t_id, members in enumerate(teams, 1):
    for p in members:
        team_out.append([t_id, people_df.iloc[p]["Name"]])
pd.DataFrame(team_out, columns=["Team", "Member"]).to_csv("final_teams_AL.csv", index=False)
print("Final Teams saved to final_teams_AL.csv")



summary = []
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
            for neigh, sc in adj_list[b1]:
                if neigh == b2:
                    scores.append(sc)
    team_score = round(sum(scores)/len(scores), 3) if scores else 0

    summary.append([t_id, len(subset), round(avg_exp,2), roles, len(all_skills), team_score])

pd.DataFrame(summary, columns=["Team", "Size", "AvgExperience", "RoleDistribution", "UniqueSkills", "CompatibilityScore"]).to_csv("team_summary_AL.csv", index=False)
print("Team Summary with Compatibility Scores saved to team_summary_AL.csv")
