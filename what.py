import pandas as pd
import plotly.graph_objects as go

file_path = "dataset-406H.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet1")
df.columns = df.columns.str.strip()
df_vietnamese = df[df["Ngôn ngữ"] == "TV"].copy()

df_vietnamese["Học Kỳ"] = df_vietnamese["Học Kỳ"].astype(str)
hoc_ky_tin_chi = df_vietnamese.groupby("Học Kỳ")["Số Tín Chỉ"].sum().astype(int).to_dict()
df_vietnamese["Học Kỳ Label"] = df_vietnamese["Học Kỳ"].apply(lambda x: f"Học kỳ {x} ({hoc_ky_tin_chi[x]} TC)")
data_pivot = df_vietnamese.groupby(["Học Kỳ Label", "Loại môn học", "Tên học phần"])["Số Tín Chỉ"].sum().reset_index()

labels = []
parents = []
values = []
ids = [] 

for hoc_ky, tin_chi in hoc_ky_tin_chi.items():
    hoc_ky_label = f"Học kỳ {hoc_ky} ({tin_chi} TC)"
    labels.append(hoc_ky_label)
    parents.append("")
    values.append(tin_chi)
    ids.append(hoc_ky_label)

for (hoc_ky_label, loai_mon), tin_chi in data_pivot.groupby(["Học Kỳ Label", "Loại môn học"])["Số Tín Chỉ"].sum().items():
    label = f"{hoc_ky_label}/{loai_mon}"
    labels.append(label)
    parents.append(hoc_ky_label)
    values.append(tin_chi)
    ids.append(label)

for _, row in data_pivot.iterrows():
    labels.append(row["Tên học phần"])
    parent_label = f"{row['Học Kỳ Label']}/{row['Loại môn học']}"
    parents.append(parent_label)
    values.append(row["Số Tín Chỉ"])
    ids.append(f"{parent_label}/{row['Tên học phần']}")
fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    ids=ids,
    branchvalues="total",
    hovertemplate=(
        "<b>Labels</b>: %{label}<br>"
        "<b>Sizes</b>: %{value}<br>"
        "<b>Parent</b>: %{parent}<br>"
        "<b>ID</b>: %{id}<br>"
    ),
    insidetextorientation="radial"
))

fig.update_layout(
    font=dict(size=12),
    margin=dict(t=60, l=0, r=0, b=0)
)

fig.write_html("chart.html")

try:
    fig.show()
    print("Success")
except Exception as e:
    print(f"Error: {e}")