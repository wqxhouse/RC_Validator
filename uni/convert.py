import glob
import os
import re
os.chdir(".")

# global vars
isVoidMain = False;
param_array_dict = {};

def isAllUpperCase(str) :
	for l in str :
		if l.islower() :
			return False;
	
	return True;
	
def isAllUpperCaseBeforeBracket(str) :
	sub = str.split("[")[0];
	sub.replace(" ", "");
	if isAllUpperCase(sub) :
		return True;
	return False;

def process(str) :
	str = strip_function(str);
	str = strip_structdef(str);
	str = modify_array(str);
	str = modify_array_param_to_pointer(str);
	str = process_tf(str);
	str = process_void_main(str);
	str = process_cout_cin_expr(str);
	str = process_sizeof_param(str);
	
	return str;
	
def format_elem_coutcin(str) :
	if ";" in str and "endl" not in str:
		return "(" + str[: str.find(";")] + ")" + str[str.find(";") :];
	elif ";" in str and "endl" in str:
		return str;
	else :
		return "(" + str + ")"
	return str;
	
def process_cout_cin_expr(str) :
	if "<<" in str or ">>" in str :
		exprarr = re.split('<<|>>', str);
		counter = 0;
		cout_or_cin = -1; # 0 is cout ; 1 is cin

		#if len(exprarr) == 2 and ("endl" in exprarr[1] ) :
			#if "cout" in exprarr[0] :
				#exprarr.insert(1, "<<");
			#elif "cin" in exprarr[0] :
				#exprarr.insert(1, ">>");
		#else :
		while True:
			elem = exprarr[counter];
			#if (elem == "<<" or elem == ">>") and \
			#   (counter + 2) < len(exprarr) and \
			#   (exprarr[counter+2] == "<<" or exprarr[counter+2] == ">>") :
			   
			#	str = exprarr[counter+1];
			#	str = "(" + str + ")";
			#	exprarr[counter+1] = str;
			if "cout" not in elem and "cin" not in elem  :	
				if "endl" in elem :
					exprarr[counter] = " << " + format_elem_coutcin(elem);
				elif "cout" in exprarr[counter-1] or cout_or_cin == 0 :
					cout_or_cin = 0;
					exprarr[counter] = " << " + format_elem_coutcin(elem);
				elif "cin" in exprarr[counter-1] or cout_or_cin == 1:
					cout_or_cin = 1;
					exprarr[counter] = " >> " + format_elem_coutcin(elem);
			
			counter += 1;
			
			if counter >= len(exprarr) :
				break;

		str = "".join(exprarr);

	return str;	
		
def process_sizeof_param(str) :
	if "sizeof" in str :
		s = str[str.find("sizeof") + 6 :];

		counter = 0;
		pcount = 0;
		expr = "";
		while True :
			if counter >= len(s):
				break;
				
			if counter != 0 and pcount == 0:
				pleft = s[ : counter-1 ];
				expr = pleft[pleft.find("(") + 1 :].split()[0];		
				break;
			
			if s[counter] == '(' :
				pcount += 1;
			elif s[counter] == ')' :
				pcount -= 1;
				
			counter += 1;

		whole_expr = str[str.find("sizeof") : str.find(")") + 1 ];
		#print param_array_dict;
		if expr in param_array_dict :
			sizestr = param_array_dict[expr];
			pair = sizestr.split();
			size = pair[0];
			type_name = pair[1];
			str = str.replace(whole_expr, size + " * sizeof(" + type_name + ")  // sizeof(" + expr + "[" + size + "])");
				
	return str;

def process_tf(str) :
	if "true" in str :
		str = str.replace("true", "1");
	if "false" in str :
		str = str.replace("false", "0");
		
	return str;
	
def process_void_main(str) :
	global isVoidMain;
	if "void" in str and "main" in str :
		str = str.replace("void", "int");
		isVoidMain = True;
	return str;
	
def modify_array(str) :
	if "[" in str and \
	   "(" not in str and \
	   ("int" in str or \
	   "float" in str or \
	   "bool" in str or \
	   isAllUpperCaseBeforeBracket(str)) :

		bracket = str[str.find("[") : str.find("]") + 1];
		#rest = str[str.find("]") : len(str)];
		str = str.replace(bracket, "");
		if ";" in str :
			str = str[: str.find(";")] + bracket + str[str.find(";") :];

	return str;
	
	
def modify_array_param_to_pointer(str) :
	global param_array_dict;
	if "[" in str and \
	   "(" in str and \
	   ("int" in str or \
	   "float" in str or \
	   "bool" in str or \
	   isAllUpperCaseBeforeBracket(str)):
	   
		#print "(" in str + ": " + str;
		list = str[str.find('(')+1 : str.find(')')];
		#print list;
		listarr = list.split(',');
		
		newlist = "";
		for l in listarr :
			brac = l[l.find("["): l.find("]")+1];
			
			# insert size to dict for future sizeof() substitution
			arr_name = l[l.find("]") + 1:].split()[0];
			type_name = l[: l.find("[")].split()[-1];
			size = brac[brac.find("[") + 1 : brac.find("]")] + " " + type_name;
			param_array_dict[arr_name] = size;		
			
			l = l.replace(brac, "*");
			newlist += l + ", ";
			
		newlist = newlist[: len(newlist)-2];
		str = str.replace(list, newlist);
		
	return str;
	
def strip_function(str) :
	if "function" in str :
		# reset global param dict first
		param_array_dict.clear();
		
		str = str.replace("function", "");
		str = str.replace(":", "");
	
	return str;
	
def strip_structdef(str) :
	if "structdef" in str:
		str = str.replace("structdef", "struct");
	return str;
	
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

for filename in glob.glob("*.rc"):
	file = open(filename, 'r');
	write = open(filename + ".cpp", "w");
	write.write("#include <iostream>\n");
	write.write("using namespace std;\n");
	count = 0;
	for line in file :
		if line not in ['\n', '\r\n'] : 
			line = process(line);
			write.write(line);
			count = count + 1;
	write.close();

	if isVoidMain == True : 
		write = open(filename + ".cpp", "r");
		contents = write.readlines();
		write.close();

		contents.insert(count-1+2, "   return 0;\n");
		contents = "".join(contents);

		write = open(filename + ".cpp", "w");
		write.write(contents);
		write.close();
		
	file.close();
	
	
		