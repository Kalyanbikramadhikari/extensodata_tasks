from Load_DF import load_df,sanitize
from datetime import datetime
def read_datas():
    layout1 = load_df('ABC_layout_1')
    layout2 = load_df('PQR_layout_2')
    layout3 = load_df('layout_3_voters')
    layout4 = load_df('KLM_layout_4')
    layout5 = load_df('layout_5_license_dropped')

    layout1 = layout1.rename(
        columns={"First Name": "Name", "Father Name": "Father_Name", "Permanent_Adress": "Permanent_Address"})
    layout2 = layout2.rename(columns={"Customer_ID": "Mobile Number"})
    layout3 = layout3.rename(
        columns={"votersName": "Name", "votersFatherName": "Father_Name", "votersMotherName": "Mother Name",
                 " Gender": "Gender", "Permanent_Adress": "Permanent_Address"})
    layout4 = layout4.rename(columns={"Father Name": "Father_Name"})

    del layout1["Last Name"]
    del layout2["Unnamed: 0"]
    del layout4["Unnamed: 0"]
    layouts = [layout1, layout2, layout3, layout4, layout5]
    layout_sources = ['bank', 'esewa', 'voter', 'electricity', 'license']

    for layout, source in zip(layouts, layout_sources):
        layout['source'] = source
        layout['modified_date'] = datetime.now()
    layout_copies = []
    for layout in layouts:
        try:
            if layout is not None:
                sanitized_layout = sanitize(layout.copy())
                layout_copies.append(sanitized_layout)
            else:
                layout_copies.append(None)
        except Exception as e:
            print(f"An error occurred while sanitizing a layout: {e}")
            layout_copies.append(None)

    for i in range(len(layout_copies)):
        layout_copies[i] = sanitize(layout_copies[i])

    return layouts,layout_copies

