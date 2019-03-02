def seperate(list1):
	for i in range(len(list1)):
		if "," in list1[i]:
			list1[i]=list1[i].split(',')
		else:
			list1[i]=list1[i].split(' ')
	for j in list1:
		if " " in j[0]:
			splitAgain=j[0]
			l=splitAgain.split(" ")
			j[0]=l[0]
			j.insert(1,l[1])
	return list1
def split_file(codename):
	file=open(codename)
	x=file.readlines()
	list1=[]
	for i in x:
		i=i.strip()
		list1.append(i)
	for j in range(len(list1)):
		if list1[j]==".text":
			list1=list1[j+1:]
			break
	for i in list1:
		if i.find(':')>=0 or i.find('#')==0:
			list1.remove(i)
		elif i.find('#')>0:
			j=i.find('#')
			k=list1.index(i)
			list1.remove(i)
			i=i[0:j]
			i=i.strip()
			list1.insert(k,i)
	list1.remove("syscall")
	return list1
def variable_split(list):
	new_list=[]
	command=[]
	input_list=[]
	output_list=[]
	for i in list:
		y=len(i)
		if(y>2):

			if((i[0]!="li") and (i[1]!="$v0")):
				if((i[0]!="sw") and (i[0]!="lw") and (i[0]!="lb") and (i[0]!="sb") and (i[0]!="bgt") and (i[0]!="blt") and (i[0]!="beqz") and (i[0]!="bne") and (i[0]!="beq") and (i[0]!="bge")):
					if((i[0]=="sll")):
						command.append('mul')
					elif((i[0]=="srl")):
						command.append('div')
					else:
						command.append(i[0])
					output_list.append(i[1])
					input_list=[]
					input_list=i[2:]
					i=[]
					i.append(command)
					i.append(output_list)
					i.append(input_list)
					new_list.append(i)
					command=[]
					output_list=[]
				elif i[0]=="lw" or i[0]=="lb" or i[0]=="move":
					command.append(i[0])
					output_list.append(i[1])
					input_list=[]
					i=i[2:]
					input_list=i[0].split('(')
					input_list.remove(input_list[0])
					input_list[0]=input_list[0][:-1]
					i=[]
					i.append(command)
					i.append(output_list)
					i.append(input_list)
					new_list.append(i)
					command=[]
					output_list=[]
				elif i[0]=="sw" or i[0]=="sb":
					command.append(i[0])
					output_list.append(i[1])
					input_list=[]
					i=i[2:]

					input_list=i[0].split('(')
					input_list.remove(input_list[0])
					input_list[0]=input_list[0][:-1]
					i=[]
					i.append(command)
					i.append(input_list)
					i.append(output_list)
					new_list.append(i)
					command=[]
					output_list=[]

				elif((i[0]=="beqz")):
					command.append(i[0])
					input_list=[]
					input_list.append(i[1])
					input_list.append('0')
					output_list=i[2:]
					i=[]
					i.append(command)
					i.append(output_list)
					i.append(input_list)
					new_list.append(i)
					command=[]
					output_list=[]
				elif i[0]=="bgt" or i[0]=="blt" or i[0]=="bne" or i[0]=="beq" or i[0]=="bge":
					command.append(i[0])
					input_list=[]
					input_list.append(i[1])
					input_list.append(i[2])
					output_list=i[3:]
					i=[]
					i.append(command)
					i.append(output_list)
					i.append(input_list)
					new_list.append(i)
					command=[]
					output_list=[]	
				else:
					command.append(i[0])
					output_list.append(i[1])
					input_list=i[2:]
					i=[]
					i.append(command)
					i.append(input_list)
					i.append(output_list)
					new_list.append(i)
					command=[]
					output_list=[]
			elif((i[0]=="li") and (i[1]=="$v0")):
				input_list=[]
				command.append('addi')
				output_list.append(i[1])
				input_list.append(i[2])
				input_list.append('$zero')
				i=[]
				i.append(command)
				i.append(output_list)
				i.append(input_list)
				new_list.append(i)
				command=[]
				output_list=[]
	return new_list
def two_output_lists(check_1,check_2):
	flag=0
	if(check_1==check_2):
		flag=1
	return flag
def check_commandand(to_check):
	commandands={'add':3 , 'sub' :3 , 'mul':3 , 'div':3 , 'lw':4 , 'sw':5 ,'slt':1, 'beq':1,'beqz':1,'bge':1, 'bgt':1, 'blt':1,'li':1 ,'bne':1,'la':1 ,'lb':4,'sb':5,'move':5 ,'addi':3}
	return commandands[to_check]
def check_without_bypassing_dependency_read_after_write(list):
	x=len(list)
	for i in range(x-4):
		for j in range(i+1,i+4):
			if ((list[i][1][0] in list[j][2])):
				print(list[i][1][0],list[j][2],i+1,j+1,"=>dependency(-r-a-w-)")
	for i in range(x-4,x-3):
		for j in range(x-3,x):
			if ((list[i][1][0] in list[j][2])):
				print(list[i][1][0],list[j][2],i+1,j+1,"=>dependency(-r-a-w-)")
	for i in range(x-3,x-2):
		for j in range(x-2,x):
			if ((list[i][1][0] in list[j][2])):
				print(list[i][1][0],list[j][2],i+1,j+1,"=>dependency(-r-a-w-)")
	for i in range(x-2,x-1):
		for j in range(x-1,x):
			if ((list[i][1][0] in list[j][2])):
				print(list[i][1][0],list[j][2],i+1,j+1,"=>dependency(-r-a-w-)")
'''def check_without_bypassing_dependency_write_after_write_output_reg_read_after(list):
	x=len(list)
	for i in range(x-4):
		if((check_commandand(list[i][0][0])==3) or (check_commandand(list[i][0][0])==4) or (check_commandand(list[i][0][0])==5)):
			for j in range(i+1,i+2):
				if ((list[i][1][0]==list[j][1][0]) or (two_output_lists(list[i][1][0],list[j][2])==1)):
					print(list[i][1][0],list[j][1][0],i+1,j+1,"=>dependency(-w-a-w-)")
	for i in range(x-4,x-3):
		if((check_commandand(list[i][0][0])==3) or (check_commandand(list[i][0][0])==4) or (check_commandand(list[i][0][0])==5)):
			for j in range(x-3,x):
				if ((list[i][1][0]==list[j][1][0]) or (two_output_lists(list[i][1][0],list[j][2])==1)):
					print(list[i][1][0],list[j][1][0],i+1,j+1,"=>dependency(-w-a-w-)")
	for i in range(x-3,x-2):
		if((check_commandand(list[i][0][0])==3) or (check_commandand(list[i][0][0])==4) or (check_commandand(list[i][0][0])==5)):
			for j in range(x-2,x):
				if ((list[i][1][0]==list[j][1][0]) or (two_output_lists(list[i][1][0],list[j][2])==1)):
					print(list[i][1][0],list[j][1][0],i+1,j+1,"=>dependency(-w-a-w-)")	
	for i in range(x-2,x-1):
		if((check_commandand(list[i][0][0])==3) or (check_commandand(list[i][0][0])==4) or (check_commandand(list[i][0][0])==5)):
			for j in range(x-1,x):
				if ((list[i][1][0]==list[j][1][0]) or (two_output_lists(list[i][1][0],list[j][2])==1)):
					print(list[i][1][0],list[j][1][0],i+1,j+1,"=>dependency(-w-a-w-)")'''
def check_with_bypassing_dependency_read_after_write(list):
	x=len(list)
	for i in range(x-4):
		if((list[i][0][0]=="lw") or (list[i][0][0]=="la")):
			for j in range(i+1,i+2):
				if ((list[i][1][0] in list[j][2])):
					print(list[i][1][0],list[j][2],i+1,j+1,"=>dependency(-r-a-w-)")	
		elif((list[i][0][0]=="sw") or (list[i][0][0]=="sb") or (list[i][0][0]=="move")):
			for j in range(i+1,i+3):
				if ((list[i][1][0] in list[j][2])):
					print(list[i][1][0],list[j][2],i+1,j+1,"=>dependency(-r-a-w-)")
	for i in range(x-4,x-3):
		if((list[i][0][0]=="lw") or (list[i][0][0]=="la")):
			for j in range(x-3,x-2):
				if ((list[i][1][0] in list[j][2])):
					print(list[i][1][0],list[j][2],i+1,j+1,"=>dependency(-r-a-w-)")	
		elif((list[i][0][0]=="sw") or (list[i][0][0]=="sb") or (list[i][0][0]=="move")):
			for j in range(x-3,x-1):
				if ((list[i][1][0] in list[j][2])):
					print(list[i][1][0],list[j][2],i+1,j+1,"=>dependency(-r-a-w-)")
	for i in range(x-3,x-2):
		if((list[i][0][0]=="lw") or (list[i][0][0]=="la")):
			for j in range(x-2,x-1):
				if ((list[i][1][0] in list[j][2])):
					print(list[i][1][0],list[j][2],i+1,j+1,"=>dependency(-r-a-w-)")	
		elif((list[i][0][0]=="sw") or (list[i][0][0]=="sb") or (list[i][0][0]=="move")):
			for j in range(x-2,x):
				if ((list[i][1][0] in list[j][2])):# or (check(list[i][1][0],list[j][2])==1)):
					print(list[i][1][0],list[j][2],i+1,j+1,"=>dependency(-r-a-w-)")	
	for i in range(x-2,x-1):
		if((list[i][0][0]=="lw") or (list[i][0][0]=="la")):
			for j in range(x-1,x):
				if ((list[i][1][0] in list[j][2])):# or (check(list[i][1][0],list[j][2])==1)):
					print(list[i][1][0],list[j][2],i+1,j+1,"=>dependency(-r-a-w-)")	
		elif((list[i][0][0]=="sw") or (list[i][0][0]=="sb") or (list[i][0][0]=="move")):
			for j in range(x-1,x):
				if ((list[i][1][0] in list[j][2])):# or (check(list[i][1][0],list[j][2])==1)):
					print(list[i][1][0],list[j][2],i+1,j+1,"=>dependency(-r-a-w-)")					
def main():
	ins=split_file("code.asm")
	comm=seperate(ins)
	final=variable_split(comm)
	print("------------------------------------------------------------------")
	print("ASSUMPTION: 'It takes an entire cycle to read and write'")
	print("------------------------------------------------------------------")
	for i in range(len(final)):
		print(final[i]," ===> ",i+1)
	print("----------read-after-write-dependencies-without----------")
	check_without_bypassing_dependency_read_after_write(final)
	'''print("----------write-after-write-dependencies-without----case-1-----------")
	check_without_bypassing_dependency_write_after_write_output_reg_read_after(final)'''
	print("-------------------------------------------------------------------------")
	print("There is no write after read or write after write dependancy inin-order pipelining")
	print("----------read-after-write-dependencies-with----------")
	check_with_bypassing_dependency_read_after_write(final)
main()
