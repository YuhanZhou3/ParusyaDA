import sqlite3
import pandas as pd


## === GET GROUP NAME AND TAGS ===
## ------------------------------------------------------------------------------------------
# TODO: user input for group name
GNAME = "Grupo Deus é Amor" # TODO

conn = sqlite3.connect('dataset/railway.sqlite')
cursor = conn.cursor()

# Get all tags for a group
query_tags = "SELECT name FROM tags WHERE group_id = (SELECT id FROM groups WHERE name = ?)"
cursor.execute(query_tags, (GNAME,))
tags = cursor.fetchall()
tags = [tag[0] for tag in tags]

# TODO: drop down menu for tags

# TODO: user input for tag selection(s)
TAG = ['quinta'] # TODO

## === QUERY FROM DATABASE ===
## ------------------------------------------------------------------------------------------
def get_placeholder(target_list):
    return ','.join(['?'] * len(target_list))

# Get all event ids for the group with the specified tags
placeholder_tags = get_placeholder(TAG)
query_eid = f"\
    SELECT DISTINCT e.id \
    FROM events AS e \
    JOIN event_tags AS et ON et.event_id = e.id \
    JOIN tags ON tags.id = et.tag_id \
    WHERE e.group_id = (SELECT id FROM groups WHERE name = ?)\
        AND tags.name IN ({placeholder_tags})"
    
cursor.execute(query_eid, [GNAME]+TAG)
event_ids = cursor.fetchall()
event_ids = [eid[0] for eid in event_ids]

# Get participant & checkin info for the events
placeholder_eids = get_placeholder(event_ids)
query = f"\
    SELECT e.id AS event_id, e.name AS event_name, e.start_date_time AS event_time, \
        p.id AS participant_id, p.full_name AS participant_name, c.timestamp AS checkin_time, \
        p.birth_date AS participant_birth, p.gender AS participant_gender \
    FROM events AS e \
    JOIN check_ins AS c ON c.event_id = e.id \
    JOIN participants AS p ON p.id = c.participant_id \
    WHERE e.id IN ({placeholder_eids})" 
# cursor.execute(query, event_ids)
# results = cursor.fetchall()
df = pd.read_sql_query(query, conn, params=event_ids)

## === Data Cleaning and Preprocessing ===
## ------------------------------------------------------------------------------------------
# # Check for missing values
# df.isnull().sum()
# df.isna().sum()
# Convert date columns to datetime format
for col in ["event_time", "checkin_time", "participant_birth"]:
    df[col] = pd.to_datetime(df[col], errors='coerce')
# Adjust time zone
df['checkin_time'] = df['checkin_time'].dt.tz_localize('UTC').dt.tz_convert('Brazil/East')
# Add age column
df["participant_age"] = (pd.to_datetime("today") - df["participant_birth"]).dt.days // 365
# De-identify participants by only keeping initials of first and last names & delete birthdate column
names = df["participant_name"].str.split()
df["participant_name"] = names.str[0].str[0] + names.str[-1].str[0]
df = df.drop(columns=["participant_birth"])

# # abnormal age value check
# abnormal_age_ids = df[df["participant_age"] <= 7]["participant_id"].drop_duplicates().tolist()

# # Get contact info for abnormal age participants
# placeholders = ",".join("?" * len(abnormal_age_ids))
# query = f"SELECT id, full_name, email, phone, birth_date FROM participants WHERE id IN ({placeholders})"

# contact_info = pd.read_sql(query, conn, params=abnormal_age_ids)
# contact_info.to_csv("dataset/abnormal_age_participants.csv", index=False)

conn.close()

## === SAVE CLEANED DATAFRAME TO CSV ===
## ------------------------------------------------------------------------------------------
df.to_csv("data_public/cleaned_data.csv", index=False)