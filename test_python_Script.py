import subprocess
out = subprocess.run(["ls", '2>&1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

new_stdout =  out.stdout.decode("utf-8")
print(new_stdout)
print("std eeor is {}".format(out.stderr.decode("utf-8")))
