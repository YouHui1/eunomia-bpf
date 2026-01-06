#!/usr/bin/env python3
import subprocess
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Build and run eBPF program",
        usage="python %(prog)s [build|run|clean|pkghelp|help] [-f FILE]"
    )

    parser.add_argument(
        "action",
        choices=["build", "run", "clean", "pkghelp", "help"],
        help="build: compile, run: execute, clean: remove files"
    )

    parser.add_argument(
        "-f", "--file",
        nargs='+',
        default="template.bpf.c",
        help="specify BPF source file (default: template.bpf.c)"
    )


    args, extra_args = parser.parse_known_args()

    try:
        if args.action == "build":
            # header_file = args.file.replace(".bpf.c", ".h")
            cmd = ["./ecc"];
            cmd.extend(args.file)
            print(f"cmd: {' '.join(cmd)}")
            subprocess.run(cmd, cwd="src", check=True)
        elif args.action == "run":
            cmd = ["sudo", "./ecli", "run", "package.json"]
            cmd.extend(extra_args)
            print(f"cmd: {' '.join(cmd)}")
            subprocess.run(cmd, cwd="src")
        elif args.action == "clean":
            for pattern in ["*.json", "*.o"]:
                cmd = ["find", ".", "-name", pattern, "-delete"]
                subprocess.run(cmd, cwd="src", check=True)
        elif args.action == "pkghelp":
            subprocess.run(["./ecli", "package.json", "-h"], cwd="src")
        elif args.action == "help":
            subprocess.run(["./ecli", "-h"], cwd="src")
        else:
            pass
    except FileNotFoundError:
        print("错误: src目录或命令不存在")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
