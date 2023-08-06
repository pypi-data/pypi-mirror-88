try:

	def fun(Path,Function):
		#(column).str.l1()
		Function_List1 = ["slice","upper","lower","rstrip","pad","abs","floor","round"]
		#l2(column)
		Function_List2 = ["chr","ord"]
		#l3(column1,column2)
		Function_List3 = ["+"]

		Dataset = pd.read_csv(Path)
		IndexColumn = Dataset.columns[0]

		#This statement for functions with "."
		if any(value in Function for value in Function_List1):
			Function = Function.split(".",1)
			Column = Function[0]
			Column = Column[1:-1]
			Fun = Function[1]
			Dataset[Column] = eval("Dataset['{}'].{}".format(Column,Fun))

		#This statement for function without "."
		elif any(value in Function for value in Function_List2):
			Function = Function.split("(",1)
			Fun = Function[0]
			Column = Function[1]
			Column = Column[0:-1]
			Dataset[Column] = [ord(val) for val in Dataset[Column].str[0]]

		#This statement for function with two column
		elif any(value in Function for value in Function_List3):
			Function = Function.split("(",1)
			Fun = Function[0]
			Column = Function[1]
			Column = Column[0:-1]
			Column = Column.split(",",1)
			if("+" in Fun):
				Dataset["CONCAT"] = " "
				for x in Column:
					Dataset['CONCAT'] += Dataset[x]

		else:
			print("Code not implemented")

		Dataset = Dataset.set_index([IndexColumn])
		print(Dataset)

except Exception as e:
	raise e