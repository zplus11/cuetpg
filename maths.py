response = "dc.pdf"
answers = {'866585378': '8665851504', '866585387': '8665851539', '866585388': '8665851541', '866585389': '8665851547', '866585390': '8665851552', '866585391': '8665851554', '866585392': '8665851557', '866585393': '8665851564', '866585394': '8665851568', '866585395': '8665851570', '866585396': '8665851575', '866585379': '8665851507', '866585397': '8665851577', '866585398': '8665851583', '866585399': '8665851586', '866585400': '8665851591', '866585401': '8665851594', '866585402': '8665851600', '866585403': '8665851604', '866585404': '8665851606', '866585405': '8665851612', '866585406': '8665851615', '866585380': '8665851512', '866585407': '8665851617', '866585408': '8665851621', '866585409': '8665851628', '866585410': '8665851632', '866585411': '8665851633', '866585412': '8665851640', '866585413': '8665851643', '866585414': '8665851645', '866585415': '8665851651', '866585416': '8665851656', '866585381': '8665851516', '866585417': '8665851658', '866585418': '8665851662', '866585419': '8665851667', '866585420': '8665851670', '866585421': '8665851673', '866585422': '8665851679', '866585423': '8665851682', '866585424': '8665851686', '866585425': '8665851689', '866585426': '8665851696', '866585382': '8665851520', '866585427': '8665851698', '866585428': '8665851701', '866585429': '8665851705', '866585430': '8665851711', '866585431': '8665851713', '866585432': '8665851718', '866585433': '8665851723', '866585434': '8665851727', '866585435': '8665851731', '866585436': '8665851736', '866585383': '8665851524', '866585437': '8665851739', '866585438': '8665851741', '866585439': '8665851746', '866585440': '8665851752', '866585441': '8665851756', '866585442': '8665851760', '866585443': '8665851762', '866585444': '8665851766', '866585445': '8665851772', '866585446': '8665851776', '866585384': '8665851527', '866585447': '8665851778', '866585448': '8665851783', '866585449': '8665851788', '866585450': '8665851790', '866585451': '8665851793', '866585452': '8665851800', '866585385': '8665851529', '866585386': '8665851535'}

import fitz

doc = fitz.open(response)
data = ""
for page in doc:
    data += page.get_text()
doc.close()

data = data.split('\n')
del data[13:27]

results = {}
question_id = None
option_ids = {}
chosen_option = None

for item in data:
    item = item.strip()
    if item.startswith("Question ID"):
        question_id = item.split(":")[1].strip()
    elif item.startswith("Option"):
        # like: Option 2 ID : 123456
        parts = item.split(":")
        if "ID" in parts[0]:
            key_part = parts[0].strip()
            value = parts[1].strip()
            if "Option" in key_part:
                num = key_part.split()[1]
                option_ids[num] = value
    elif item.startswith("Chosen Option"):
        value = item.split(":")[1].strip()
        chosen_option = value
        # finalise one question block
        if question_id:
            if chosen_option == "--":
                results[question_id] = "NA"
            else:
                answer_id = option_ids.get(chosen_option, "NA")
                results[question_id] = answer_id
            # reset for next question
            question_id = None
            option_ids = {}
            chosen_option = None

correct = 0
wrong = 0
unanswered = 0
def marks():
    global correct, wrong
    return correct*4 - wrong
for i, response in enumerate(results):
    print("question", i+1)
    print("Correct", answers[response])
    print("Selected", results[response])
    if results[response] == answers[response]:
        correct += 1
        print("right: +4 =", marks())
    elif results[response] == "NA":
        unanswered += 1
        print("nothing: +0 =", marks())
    else:
        wrong += 1
        print("wrong: -1 =", marks())
    print()
print()
print("Total Correct:", correct)
print("Total Wrong:", wrong)
print("Total Unaswered:", unanswered)
print("Final Marks")
print(marks())
