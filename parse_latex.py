import glob
import os
import argparse

def print_start(file, comment=""): 
    print("", file=file)
    print("%" + comment, file=file)
    print(r"\begin{note}", file=file)

def print_end(tag, section, subsection, file, indent="  "): 
    print(indent + r"\xplain{" + subsection + r"}" + r"% Subsection", file=file)
    print(indent + r"\xplain{" + section + r"}" + r"% Section", file=file)
    print(indent + r"\xplain{}" + r"% Subject", file=file)
    print(indent + r"\xplain{" + tag + r"}" + r"% Label", file=file)
    print(r"\end{note}", file=file)

def process_tex_files(input_dir, input_subdir, output_dir, env_tags, long_vocab_count):
    
    tex_files = glob.glob(os.path.join(input_dir, input_subdir, "**", "*.tex"), recursive=True)

    for tex_file in tex_files:
        if os.path.basename(tex_file) == "header.tex":
            continue

        count = 0
        buffer = []
        prev_buffer = []
        environment_active = False
        indent = "  "
        section = ""
        subsection = ""

        output_subdir_ = os.path.dirname(os.path.relpath(tex_file, start=input_dir))
        output_subdir = os.path.join(output_dir, output_subdir_)
        os.makedirs(output_subdir, exist_ok=True)
        
        tex_anki_file = os.path.splitext(os.path.basename(tex_file))[0]
        
        print(os.path.join(output_subdir_, os.path.basename(tex_file)))

        with open(tex_file, "r", encoding="utf-8") as input_tex:
            output_path = os.path.join(output_subdir, os.path.basename(tex_anki_file) + ".anki.tex")
            with open(output_path, "w") as output_tex:
                count_of_section = -1
                count_of_subsection = 0
                print(r"\input{../_math_header.tex}", file=output_tex)
                print(r"\input{../_build_card.tex}", file=output_tex)
                print(r"\begin{document}", file=output_tex)
                
                for line_number, x in enumerate(input_tex, start=1):
                    
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
                            continue

                    # Detect the end of the current environment, then process the buffer
                    if environment_active and r"\end{" + environment_name + "}" in x:
                        buffer.append(x)
                        
                        tag = env_tags[environment_name]
                        
                        # Process the buffer depending on tag
                        if tag == "VOCABULARY":
                            manual_edit = (buffer[0].find("[") == -1 or len(buffer) > long_vocab_count)
                            if manual_edit:
                                print_start(output_tex, comment=" To be manually edited")
                            else:
                                print_start(output_tex)
                            # ID Field
                            print(indent + r"\xplain{" + os.path.basename(tex_file) + " " + str(count) + r"}", file=output_tex)
                            # Question Field
                            print(indent + r"\begin{field}", file=output_tex)
                            if manual_edit:
                                for line in buffer:
                                    print(indent * 2 + line, file=output_tex)
                            else:
                                print(indent * 2 + buffer[0][buffer[0].find("[")+1:buffer[0].find("]")], file=output_tex)
                            print(indent + r"\end{field}", file=output_tex)
                            # Answer Field
                            print(indent + r"\begin{field}", file=output_tex)
                            for line in buffer:
                                print(indent * 2 + line, file=output_tex)
                            print(indent + r"\end{field}", file=output_tex)
                        
                        elif tag == "GENERAL KNOWLEDGE":
                            manual_edit = (buffer[0].find("[") == -1 or len(buffer) > long_vocab_count)
                            if manual_edit:
                                print_start(output_tex, comment=" To be manually edited")
                            else:
                                print_start(output_tex)
                            # ID Field
                            print(indent + r"\xplain{" + os.path.basename(tex_file) + " " + str(count) + r"}", file=output_tex)
                            # Question Field
                            print(indent + r"\begin{field}", file=output_tex)
                            if manual_edit:
                                for line in buffer:
                                    print(indent * 2 + line, file=output_tex)
                            else:
                                print(indent * 2 + buffer[0][buffer[0].find("[")+1:buffer[0].find("]")], file=output_tex) 
                            print(indent + r"\end{field}", file=output_tex)
                            # Answer Field
                            print(indent + r"\begin{field}", file=output_tex)
                            for line in buffer:
                                print(indent * 2 + line, file=output_tex)
                            print(indent + r"\end{field}", file=output_tex)
                            
                            prev_buffer = buffer
                            # prev_environment = environment_name

                        elif tag == "PROOF EXERCISE":
                            print_start(output_tex)
                            # ID Field
                            print(indent + r"\xplain{" + os.path.basename(tex_file) + " " + str(count) + r"}", file=output_tex)
                            # Question Field
                            print(indent + r"\begin{field}", file=output_tex)
                            for line in prev_buffer:
                                print(indent * 2 + line, file=output_tex)
                            print(indent + r"\end{field}", file=output_tex)
                            # Answer Field
                            print(indent + r"\begin{field}", file=output_tex)
                            for line in buffer:
                                print(indent * 2 + line, file=output_tex)
                            print(indent + r"\end{field}", file=output_tex)
                        
                        print_end(tag, section, subsection, output_tex, indent)
                        buffer = []
                        environment_active = False
                        continue

                    if environment_active:
                        buffer.append(x)
                    else:
                        # Line processing outside of environments
                        if r"\section{" in x:
                            count_of_section += 1
                            count_of_subsection = 0
                            section = str(count_of_section) + " " + x[x.find("{")+1: x.rfind("}")]
                            print("\n" + x, file=output_tex)
                        
                        if r"\subsection{" in x:
                            count_of_subsection += 1
                            subsection = str(count_of_section) + "." + str(count_of_subsection) + " " + x[x.find("{")+1: x.rfind("}")]
                            print("\n" + x, file=output_tex)
                    
                print(r"\end{document}", file=output_tex)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some LaTeX files.")
    parser.add_argument("--input_subdir", type=str, default="", 
                        help="Input subdirectory (i.e term)")
    parser.add_argument("--output_dir", type=str, default=".out",
                        help="Output directory")
    parser.add_argument("--long_vocab_count", type=int, default=10, # lines
                        help="Threshold count for long question")
    
    args = parser.parse_args()
    
    # Environment to tag mapping
    env_tags = {
        "defi": "VOCABULARY",
        "law": "VOCABULARY",
        "thm": "GENERAL KNOWLEDGE",
        "prop": "GENERAL KNOWLEDGE",
        "lemma": "GENERAL KNOWLEDGE",
        "cor": "GENERAL KNOWLEDGE",
        "eg": "GENERAL KNOWLEDGE",
        "proof": "PROOF EXERCISE"
        }
    
    base_dir = os.getcwd()
    input_dir = os.path.join(base_dir, "cam-notes")
    output_dir = os.path.join(base_dir, args.output_dir)

    process_tex_files(input_dir, args.input_subdir, output_dir, env_tags, args.long_vocab_count)