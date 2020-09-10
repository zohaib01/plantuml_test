import sys
import argparse
import subprocess

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-o", "--output", required=True)
# Read arguments from command line
args = vars(parser.parse_args())

input_md = args["input"]
output_md = args["output"]


def render_uml():

    opening_tag = "```plantuml"
    closing_tag = "```"
    plantUML_code = []
    opening_tag_found = False

    try:
        with open(str(input_md), 'r') as input_file:
            for line in input_file:
                if opening_tag in line:
                    opening_tag_found = True
                    print('found {}'.format(line))
                    plantUML_code.append(line)

                else:
                    if opening_tag_found:
                        if closing_tag in line:
                            plantUML_code.append(line)
                            break
                        else:
                            plantUML_code.append(line)

            input_file.close()

        stdout, stderr = subprocess.Popen(['pandoc', input_md, '-o', 'test_out.md', '--filter', 'pandoc-plantuml'],
                                          stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()

        print(stdout.decode("utf-8"))
        if stderr:

            try:
                with open(str(output_md), 'w') as out_file:
                    for data in plantUML_code:
                        out_file.write(data)

                    try:
                        with open('test_out.md', 'r') as input_file:
                            for line in input_file:
                                out_file.write(line)
                            input_file.close()

                    except IOError:
                        print("No test_out.md file found")
                        sys.exit(1)

                    out_file.close()

            except IOError:
                print("No {} file found".format(output_md))
                sys.exit(1)

        #elif pandoc_cmd.stderr:
        else:
            print('failed to run pandoc. Following error occured')
            print(stderr.decode('utf-8'))
            sys.exit(1)

    except IOError:
        print("No {} file found".format(input_md))
        sys.exit(1)


if __name__ == "__main__":
    render_uml()
