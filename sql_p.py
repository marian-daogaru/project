import re

nickname = '123456'

print(re.sub(r'[^a-zA-Z0-9_\.]', '', nickname))


b = re.sub('^[a-zA-Z0-9_\.]', '', nickname)
print(b)
