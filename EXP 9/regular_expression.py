import re

text = "My name is Prasad and my phone number is 2345678903"

result = re.search("Prasad", text)

if result:
    print("Word found:", result.group())
else:
    print("Word not found")

digits = re.findall(r"\d", text)
print("Digits:", digits)

phone = re.search(r"\d{10}", text)

if phone:
    print("Phone number:", phone.group())
else:
    print("Phone number not found")
