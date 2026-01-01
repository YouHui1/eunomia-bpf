#!/usr/bin/env python3
import subprocess
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Build and run eBPF program",
        usage="python %(prog)s [build|run|clean] [-f FILE]"
    )

    parser.add_argument(
        "action",
        choices=["build", "run", "clean"],
        help="build: compile, run: execute, clean: remove files"
    )

    parser.add_argument(
        "-f", "--file",
        default="template.bpf.c",
        help="specify BPF source file (default: template.bpf.c)"
    )

    args = parser.parse_args()

    try:
        if args.action == "build":
            # header_file = args.file.replace(".bpf.c", ".h")
            subprocess.run(["./ecc", args.file], cwd="src", check=True)
        elif args.action == "run":
            subprocess.run(["sudo", "./ecli", "run", "package.json"], cwd="src")
        elif args.action == "clean":
            for pattern in ["*.json", "*.o"]:
                cmd = ["find", ".", "-name", pattern, "-delete"]
                subprocess.run(cmd, cwd="src", check=True)
    except FileNotFoundError:
        print("错误: src目录或命令不存在")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
