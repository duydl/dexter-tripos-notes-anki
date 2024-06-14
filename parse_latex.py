import glob
import os

def print_new(x, file):
    print_old(x.strip(), file = file, end=" ")
print_old = print

def print_final(tag):
    global section, subsection
    print(indent + r"\xplain{" + subsection + r"}", file=g)
    print(indent + r"\xplain{" + section + r"}", file=g)
    print(indent + r"\xplain{}", file=g)
    print(indent + r"\xplain{" + tag + r"}", file=g)
    print(r"\end{note}", file=g)

input_dir = "cam-notes/"
output_dir = "out/"

tex_files = glob.glob(input_dir + "**/*.tex", recursive=True)
print(tex_files)
for filetex in tex_files:
    print(filetex)
    count = 0
    switch = 0 # mode - print line when switch >0
    check = 1 # check if close note or not
    indent = ""
    section = ""
    subsection = ""

    # Extract relative path and create corresponding output directory
    relative_path = os.path.dirname(filetex[len(input_dir):])
    output_subdir = os.path.join(output_dir, relative_path)
    os.makedirs(output_subdir, exist_ok=True)

    with open(filetex, 'r') as f:
        output_path = os.path.join(output_subdir, os.path.basename(filetex) + "_anki.tex")
        with open(output_path, 'w') as g:
            count_of_section = -1
            count_of_subsection = 0
            print(r"\input{_anki_header.tex}", file=g)
            print(r"\input{_build_card_1}", file=g)
            print(r"\begin{document}", file=g)     
            for x in f:
                if r"\[" in x or r"\begin{align*}" in x:
                    print = print_new
                if r"\]" in x or r"\end{align*}" in x:
                    print = print_old
                
                x = x.rstrip()
                if r"\section{" in x:
                    count_of_section += 1
                    count_of_subsection = 0
                    section = str(count_of_section) + " " + x[x.find("{")+1: x.rfind("}")]
                    print(x, file=g)
                    
                if r"\subsection{" in x:
                    count_of_subsection += 1
                    subsection = str(count_of_section) + "." + str(count_of_subsection) + " " + x[x.find("{")+1: x.rfind("}")]
                    print(x, file=g)
                
                # if r"\section{" in x:
                #     print(x, file=g)
                # if r"\subsection{" in x:
                #     print(x, file=g)


                if (r"\begin{defi}" in x or r"\begin{law}" in x) and switch != 2:
                    if check == 0:
                        print(indent + r"\begin{field}", file=g)
                        print(indent + r"\end{field}", file=g)
                        print_final("GENERAL KNOWLEDGE") 
                    switch = 1               
                    check = 0 
                    print(r"\begin{note}", file=g)
                    count = count + 1
                    # print(r"%" + "Note " + str(count) + " " + filetex, file=g)
                    print(indent + r"\xplain{" + os.path.basename(filetex) + " " + str(count) + r"}", file=g)
                    print(indent + r"\begin{field}", file=g)
                    if x.find("[") > 0:
                        print(indent + indent + x[x.find("[")+1: x.find("]")], file=g)
                    else : print("add here" + str(count), file = g)
                    print(indent + r"\end{field}", file=g)
                    print(indent + r"\begin{field}", file=g)
                    
                if (r"\end{defi}" in x or r"\end{law}" in x) and switch == 1:
                    print (indent + indent + x, file=g)
                    print(indent + r"\end{field}", file=g)
                    print_final("VOCABULARY")
                    check = 1
                    switch = 0
                

                if (r"\begin{thm}" in x or r"\begin{prop}" in x or r"\begin{lemma}" in x or r"\begin{cor}" in x or r"\begin{eg}" in x) and switch != 1: 
                    if check == 0:
                        print(indent + r"\begin{field}", file=g)
                        print(indent + r"\end{field}", file=g)
                        print_final("GENERAL KNOWLEDGE")  
                    switch = 2
                    check = 0
                    print(r"\begin{note}", file=g)
                    count = count + 1
                    # print(r"%" + "Note " + str(count) + " " + filetex, file=g)
                    print(indent + r"\xplain{" + os.path.basename(filetex) + " " + str(count) + r"}", file=g)
                    print(indent + r"\begin{field}", file=g)     
                if (r"\end{thm}" in x or r"\end{prop}" in x or r"\end{lemma}" in x or r"\end{cor}" in x or r"\end{eg}" in x) and switch == 2:
                    print (indent + indent + x, file=g)
                    print(indent + r"\end{field}", file=g)
                    switch = 0

                if r"\begin{proof}" in x and check == 0:
                    switch = 3
                    print(indent + r"\begin{field}", file=g)
                if r"\end{proof}" in x and switch == 3:
                    print(indent + indent + x, file=g)
                    print(indent + r"\end{field}", file=g)
                    print_final("PROOF EXCERCISE")
                    check = 1
                    switch = 0
            
                
    
                if not x: continue
                
                if switch > 0:
                    if r"\includegraphics" in x:
                        print (indent + indent + r"%" + x, file=g)
                    else:
                        print (indent + indent + x, file=g)
                

            if check == 0:
                print(indent + r"\begin{field}", file=g)
                print(indent + r"\end{field}", file=g)
                print_final("GENERAL KNOWLEDGE") 
                
            print(r"\end{document}", file=g)
        

