from cubes import Workspace

workspace = Workspace()
workspace.register_default_store("sql", url="sqlite:///webshop.sqlite")
workspace.import_model("model.json")
browser = workspace.browser("sales")
result = browser.aggregate()
print("sum = ", result.summary["quantity_sum"])

result = browser.aggregate(drilldown=["date_sale:week",  "product"])
for record in result:
    print(record)