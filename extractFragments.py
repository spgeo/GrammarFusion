import sys 


def importENabnf():
    hm = {}
    f_in = open("en.abnf","r")
    for line in f_in:
        line = line.replace("\n","")
        line = line.replace("\"","")
        if line == ",":
            pass
        else:
            if "=" in line:
                tmp = line.split("=")
                name = tmp[0].replace("$","")
    #            I only want terminal to non-terminal relations and not rules, which point to another non-terminal.
                if "$" in tmp[1]:
                    pass
                else:
                    tmp_terminal = tmp[1].split("|")
                    for x in tmp_terminal:
                        hm[x.lower()] = name
                    
                
#    print hm
    f_in.close()
    return hm

#First simple approach for extracting pattern from an input file and additionoly substitution of words, e.g. Los Angeles to <CITYNAME>

def extractFromFile(input_file, output_file):
#    if len(sys.argv) < 3:
#        print "python extractFragments.py input.txt output.txt"
#        exit(1)
#        
    hm_terminal = importENabnf()
#    input_file = sys.argv[1]
#    output_file = sys.argv[2]
        
    f = open(input_file,"r")
    f_out_overall = open(output_file,"w")
    
    counter_line = 0
    original_sentence = []
    statement_hm = {}
    statement_overall = {}

    
    for line in f:
        line = line.replace("\n","")
        flag = False
        if line == "":
            counter_line = 0
            pass
            
        else:
            if counter_line == 0:
                sentence = line.replace("0.000000","")
                sentence = sentence.replace("  "," ")
                counter_line += 1
                original_sentence = sentence.split(" ")
            tmp = line.split(" ")
            
            first_pos = 0
            last_pos = 0
            if "<SGM>" in tmp:
                counter = 0
                for x in tmp:
                    if "<SGM>" == x and first_pos == 0:
                        first_pos = counter
                    elif "<SGM>" == x:
                        last_pos = counter + 2
                    counter += 1
                    if "Statement" in x:
                        flag = True
            if flag == True:
                statement = tmp[first_pos - 2]
                if statement_overall.has_key(statement):
                    tmp = statement_overall[statement]
                    write_string =""
                    old_string = ""
                    for x in original_sentence[(first_pos - 2)/2:last_pos/2]:
                        blub = old_string + " "+ x
                        if hm_terminal.has_key(blub.lower()):
                            write_string += "<"+hm_terminal[blub.lower()].replace(" ","").upper()+">"+ "-"
                            write_string = write_string.replace("-"+old_string+"-", "-")
 
                        elif hm_terminal.has_key(x.lower()):
                            write_string += "<"+hm_terminal[x.lower()].replace(" ","").upper()+">"+ "-"
                        else:
                            write_string += x+ "-"
                    old_string = x
                    write_string = write_string[:-1]
                    write_string += ""
                    if write_string not in tmp:
                        tmp.append(write_string)
                    statement_overall[statement] = tmp
                    
                else:
                    write_string =""
                    old_string = ""
                    for x in original_sentence[(first_pos - 2)/2:last_pos/2]:
                        blub = old_string + " "+ x
                        old_string = x
                        if hm_terminal.has_key(blub.lower()):
                            write_string += "<"+hm_terminal[blub.lower()].replace(" ","").upper()+">"+ "-"
 
                        elif hm_terminal.has_key(x.lower()):
                            write_string += "<"+hm_terminal[x.lower()].replace(" ","").upper()+">"+ "-"
                        else:
                            write_string += x+ "-"
                    write_string = write_string[:-1]
                    write_string += ""
                    statement_overall[statement] = [write_string]
            
                
    #f_out.close()
    for key in statement_overall:
        write_string=""
        if len(statement_overall[key]) > 0:
            write_string += key+": "
            for x in statement_overall[key]:
                write_string += x+","
            write_string = write_string[:-1]
            while ", \"," in write_string:
                write_string = write_string.replace(", \",",",")
            write_string = write_string.replace("\", \",","\",")
            write_string = write_string.replace(":  \",", ": ")
            if write_string.endswith(":  \""):
                pass
            else:
                write_string += "\n\n\n"
                f_out_overall.write(write_string)
            
    f_out_overall.close()
    print "Done"





def mapping():
    pass


