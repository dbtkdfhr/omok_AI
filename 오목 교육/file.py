file = open("./기보.txt","r")

txt = ""
while True:
	line = file.readline()
	if not line: break
	txt += line + "\n"

while txt.find("<") != -1:
	a = txt.find("<")
	b = txt.find(">")
	txt = txt.replace(txt[a:b+1],"")

txt = "\n".join([s for s in txt.split("\n") if s])

file.close()

file = open("./새기보.txt","w")
file.write(txt)

file.close()
