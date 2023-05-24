import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
app = ttk.Window()
colors = app.style.colors
coldata = [
    {"text": "LicenseNumber", "stretch": True},
    "CompanyName",
    {"text": "UserCount", "stretch": True},
]
rowdata = [
    ('A123', 'IzzyCo', 12),
    ('A136', 'Kimdee Inc.', 45),
    ('A136', 'Kimdee Inc.', 45),
    ('A136', 'Kimdee Inc.', 45),
    ('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),
    ('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),
    ('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),
    ('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),
    ('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),
    ('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),
    ('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),
    ('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),
    ('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inddddddddddddddddddddddddddc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),
    ('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),
    ('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),('A136', 'Kimdee Inc.', 45),
    ('A999', 'search test', 9999),
]
dt = Tableview(
    master=app,
    coldata=coldata,
    rowdata=rowdata,
    paginated=True,
    searchable=True,
    bootstyle=PRIMARY,
    stripecolor=(colors.light, None),
    autofit = True,
)
dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)
app.mainloop()