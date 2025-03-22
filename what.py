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

so_mon_hoc = df_vietnamese.groupby(["Học Kỳ Label", "Loại môn học"])["Tên học phần"].nunique().to_dict()
tong_mon_hoc_hoc_ky = df_vietnamese.groupby("Học Kỳ Label")["Tên học phần"].nunique().to_dict()

labels = []
parents = []
values = []
ids = []
hover_data = {}

for hoc_ky, tin_chi in hoc_ky_tin_chi.items():
    hoc_ky_label = f"Học kỳ {hoc_ky} ({tin_chi} TC)"
    labels.append(hoc_ky_label)
    parents.append("")
    values.append(tin_chi)
    ids.append(hoc_ky_label)
    hover_data[hoc_ky_label] = tong_mon_hoc_hoc_ky[hoc_ky_label]

for (hoc_ky_label, loai_mon), tin_chi in data_pivot.groupby(["Học Kỳ Label", "Loại môn học"])["Số Tín Chỉ"].sum().items():
    label = f"{hoc_ky_label}/{loai_mon}"
    labels.append(label)
    parents.append(hoc_ky_label)
    values.append(tin_chi)
    ids.append(label)
    hover_data[label] = so_mon_hoc.get((hoc_ky_label, loai_mon), 0)

for _, row in data_pivot.iterrows():
    labels.append(row["Tên học phần"])
    parent_label = f"{row['Học Kỳ Label']}/{row['Loại môn học']}"
    parents.append(parent_label)
    values.append(row["Số Tín Chỉ"])
    ids.append(f"{parent_label}/{row['Tên học phần']}")
    hover_data[row["Tên học phần"]] = 1

fig = go.Figure(go.Sunburst(
    name="",
    labels=labels,
    parents=parents,
    values=values,
    ids=ids,
    branchvalues="total",
    hovertemplate=(
        "label: %{label}<br>"
        "parent: %{parent}<br>"
        "sizes: %{customdata}<br>"
        "id: %{id}<br>"
    ),
    customdata=[hover_data.get(label, 0) for label in labels],
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