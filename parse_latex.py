import glob
import os

def print_start(file): 
    print("", file=file)
    print("%", file=file)
    print(r"\begin{note}", file=file)

def print_end(tag, section, subsection, file, indent="  "): 
    print(indent + r"\xplain{" + subsection + r"}" + r"% Subsection", file=file)
    print(indent + r"\xplain{" + section + r"}" + r"% Section", file=file)
    print(indent + r"\xplain{}" + r"% Subject", file=file)
    print(indent + r"\xplain{" + tag + r"}" + r"% Label", file=file)
    print(r"\end{note}", file=file)

def process_tex_files(input_dir, output_dir):

    # Environment to tag mapping
    env_tags = {
        "defi": "VOCABULARY",
        "law": "VOCABULARY",
        "thm": "THEOREM",
        "prop": "PROPOSITION",
        "lemma": "LEMMA",
        "cor": "COROLLARY",
        "eg": "EXAMPLE",
        "proof": "PROOF EXERCISE"
    }
    
    tex_files = glob.glob(input_dir + "**/*.tex", recursive=True)
    print(tex_files)
    for filetex in tex_files:
        # print = print_old
        print(filetex)
        count = 0
        buffer = []
        environment_active = False
        indent = "  "
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
                    x = x.rstrip()
                    if not x.strip():
                        continue

                    # Detect the beginning of a new environment
                    if r"\begin{" in x:
                        env_name = x.split("{")[1].split("}")[0]
                        if env_name in env_tags:
                            count += 1
                            environment_active = True
                            environment_name = env_name
                            buffer.append(x)
                            print_start(output_tex)
                            print(indent + r"\xplain{" + os.path.basename(filetex) + " " + str(count) + r"}", file=output_tex)
                            continue

                    # Detect the end of the current environment
                    if environment_active and r"\end{" + environment_name + "}" in x:
                        buffer.append(x)
                        # Process the entire buffer here
                        for line in buffer:
                            print(indent + line, file=output_tex)
                        print_end(env_tags[environment_name], section, subsection, output_tex, indent)
                        buffer = []
                        environment_active = False
                        continue

                    if environment_active:
                        buffer.append(x)
                    else:
                        # Regular line processing outside of environments
                        if r"\section{" in x:
                            count_of_section += 1
                            count_of_subsection = 0
                            section = str(count_of_section) + " " + x[x.find("{")+1: x.rfind("}")]
                            print("% " + x, file=output_tex)
                        
                        if r"\subsection{" in x:
                            count_of_subsection += 1
                            subsection = str(count_of_section) + "." + str(count_of_subsection) + " " + x[x.find("{")+1: x.rfind("}")]
                            print("% " + x, file=output_tex)

                print(r"\end{document}", file=output_tex)

if __name__ == "__main__":
    input_dir = "cam-notes/"
    output_dir = "out/"
    process_tex_files(input_dir, output_dir)