import glob
import os

# def print_start(file): 
#     print("%", file=file)
#     print(r"\begin{note}", file=file)

def print_end(tag, section, subsection, file, indent=""): 
    print(indent + r"\xplain{" + subsection + r"}", file=file)
    print(indent + r"\xplain{" + section + r"}", file=file)
    print(indent + r"\xplain{}", file=file)
    print(indent + r"\xplain{" + tag + r"}", file=file)
    print(r"\end{note}", file=file)

def process_tex_files(input_dir, output_dir):
    # global print
    # def print_new(x, file):
    #     print_old(x.strip(), file = file, end=" ")
    # print_old = print

    tex_files = glob.glob(input_dir + "**/*.tex", recursive=True)
    print(tex_files)
    for filetex in tex_files:
        # print = print_old
        print(filetex)
        count = 0
        switch = 0 # mode - print line when switch > 0
        check = 1 # check if close note or not
        indent = ""
        section = ""
        subsection = ""

        # Extract relative path and create corresponding output directory
        relative_path = os.path.dirname(filetex[len(input_dir):])
        output_subdir = os.path.join(output_dir, relative_path)
        os.makedirs(output_subdir, exist_ok=True)

        with open(filetex, 'r') as input_tex:
            output_path = os.path.join(output_subdir, os.path.basename(filetex) + "_anki.tex")
            with open(output_path, 'w') as output_tex:
                count_of_section = -1
                count_of_subsection = 0
                print(r"\input{_anki_header.tex}", file=output_tex)
                print(r"\input{_build_card_1}", file=output_tex)
                print(r"\begin{document}", file=output_tex)     
                for x in input_tex:
                    
                    # if r"\[" in x or r"\begin{align*}" in x:
                    #     print = print_new
                    # if r"\]" in x or r"\end{align*}" in x:
                    #     print = print_old
                    
                    x = x.rstrip()
                    if not x: continue
                    
                    if r"\section{" in x:
                        count_of_section += 1
                        count_of_subsection = 0
                        section = str(count_of_section) + " " + x[x.find("{")+1: x.rfind("}")]
                        print(x, file=output_tex)
                        
                    if r"\subsection{" in x:
                        count_of_subsection += 1
                        subsection = str(count_of_section) + "." + str(count_of_subsection) + " " + x[x.find("{")+1: x.rfind("}")]
                        print(x, file=output_tex)


                    if (r"\begin{defi}" in x or r"\begin{law}" in x) and switch != 2:
                        if check == 0:
                            print(indent + r"\begin{field}", file=output_tex)
                            print(indent + r"\end{field}", file=output_tex)
                            print_end("GENERAL KNOWLEDGE", section, subsection, output_tex) 
                        switch = 1               
                        check = 0 
                        print(r"\begin{note}", file=output_tex)
                        count = count + 1
                        # print(r"%" + "Note " + str(count) + " " + filetex, file=output_tex)
                        print(indent + r"\xplain{" + os.path.basename(filetex) + " " + str(count) + r"}", file=output_tex)
                        print(indent + r"\begin{field}", file=output_tex)
                        if x.find("[") > 0:
                            print(indent + indent + x[x.find("[")+1: x.find("]")], file=output_tex)
                        else : print("add here" + str(count), file=output_tex)
                        print(indent + r"\end{field}", file=output_tex)
                        print(indent + r"\begin{field}", file=output_tex)
                    if (r"\end{defi}" in x or r"\end{law}" in x) and switch == 1:
                        print (indent + indent + x, file=output_tex)
                        print(indent + r"\end{field}", file=output_tex)
                        print_end("VOCABULARY", section, subsection, output_tex)
                        check = 1
                        switch = 0


                    if (r"\begin{thm}" in x or 
                        r"\begin{prop}" in x or r"\begin{lemma}" in x or 
                        r"\begin{cor}" in x or r"\begin{eg}" in x) and switch != 1: 
                        if check == 0:
                            print(indent + r"\begin{field}", file=output_tex)
                            print(indent + r"\end{field}", file=output_tex)
                            print_end("GENERAL KNOWLEDGE", section, subsection, output_tex)  
                        switch = 2
                        check = 0
                        print(r"\begin{note}", file=output_tex)
                        count = count + 1
                        # print(r"%" + "Note " + str(count) + " " + filetex, file=output_tex)
                        print(indent + r"\xplain{" + os.path.basename(filetex) + " " + str(count) + r"}", file=output_tex)
                        print(indent + r"\begin{field}", file=output_tex)     
                    if (r"\end{thm}" in x or r"\end{prop}" in x or 
                        r"\end{lemma}" in x or r"\end{cor}" in x or 
                        r"\end{eg}" in x) and switch == 2:
                        print (indent + indent + x, file=output_tex)
                        print(indent + r"\end{field}", file=output_tex)
                        switch = 0


                    if r"\begin{proof}" in x and check == 0:
                        switch = 3
                        print(indent + r"\begin{field}", file=output_tex)
                    if r"\end{proof}" in x and switch == 3:
                        print(indent + indent + x, file=output_tex)
                        print(indent + r"\end{field}", file=output_tex)
                        print_end("PROOF EXCERCISE", section, subsection, output_tex)
                        check = 1
                        switch = 0


                    if switch > 0:
                        if r"\includegraphics" in x:
                            print (indent + indent + r"%" + x, file=output_tex)
                        else:
                            print (indent + indent + x, file=output_tex)


                if check == 0:
                    print(indent + r"\begin{field}", file=output_tex)
                    print(indent + r"\end{field}", file=output_tex)
                    print_end("GENERAL KNOWLEDGE", section, subsection, output_tex) 
                    
                print(r"\end{document}", file=output_tex)

if __name__ == "__main__":
    input_dir = "cam-notes/"
    output_dir = "out/"
    process_tex_files(input_dir, output_dir)