import subprocess

go = object()

class cmd:
    def __init__(self, log=True, decode=True, capture=False):
        self.subcommands = []
        self.log = log
        self.capture = capture
        self.decode = capture

    def __or__(self, other):
        self.subcommands.append(other)
        return self
    
    def __gt__(self, other):
        return self.run(output=other)

    def __rshift__(self, other):
        return self.run(output=other, append=True)

    def run(self, output=go, append=False):
        kwargs = {
            "shell": True
        }
        if self.capture:
            kwargs["stdout"] = subprocess.PIPE
            kwargs["stderr"] = subprocess.PIPE

        if output is go:
            command = " | ".join(self.subcommands)
            if self.log:
                print(command)
            r = subprocess.run(command, **kwargs)
            if self.decode:
                r.stdout = r.stdout.decode("utf-8")
                r.stderr = r.stderr.decode("utf-8")
            return r
        else:
            raise RuntimeError("output not supported")            
