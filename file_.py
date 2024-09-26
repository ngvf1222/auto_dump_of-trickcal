import inquirer
import os
import json

file_list = list(filter(lambda x: x[-5:] == ".json", os.listdir('./dumps')))

questions = [
    inquirer.List(
        "one",
        message="select 1st file",
        choices=file_list,
    ),
    inquirer.List("two", message="select 2nd file", choices=file_list),
]

answers = inquirer.prompt(questions)
F_name = './dumps/'+answers["one"]
S_name = './dumps/'+answers["two"]
with open(F_name) as f:
    F_data = json.load(f)
with open(S_name) as f:
    S_data = json.load(f)


def compare(a, b, src="root"):
    # print(type(a), type(b))
    if type(a) == type("str") or type(b) == type("str"):
        if a != b:
            print(f"{src}:{a}=>{b}")
        return
    for i in a:
        if i in b:
            compare(a[i], b[i], src=src + f".{i}")
        else:
            print(f"{src}{i} X")
    for i in set(b.keys()) - set(a.keys()):
        print(f"{src}{i} O")


print(compare(F_data, S_data))
