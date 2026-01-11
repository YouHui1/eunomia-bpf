#!/usr/bin/env python3
import subprocess
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(
        description="Build and run eBPF program",
        usage="python %(prog)s [mkdir|create|build|run|clean|pkghelp|help] [-f FILE]"
    )

    parser.add_argument(
        "action",
        choices=["mkdir", "create", "build", "run", "clean", "pkghelp", "help"],
        help="build: compile, run: execute, clean: remove files, help: ecc help, pkghelp: package help, create: create files"
    )

    parser.add_argument(
        "-f", "--file",
        nargs='+',
        default="template.bpf.c",
        help="specify BPF source file (default: template.bpf.c)"
    )

    parser.add_argument(
        "-d", "--dir",
        help="specify directory (default: src)"
    )


    args, extra_args = parser.parse_known_args()

    try:
        if args.action == "mkdir":
            cmd = ["mkdir"];
            cmd.append(args.dir)
            print(f"cmd: {' '.join(cmd)}")
            subprocess.run(cmd, cwd="src")
            pass
        elif args.action == "create":
            cmd = ["touch"];
            cmd.extend(args.file)
            directory = "src"
            if args.dir is not None:
                directory = os.path.join(directory, args.dir)
            print(f"cmd: {' '.join(cmd)}, dir: {directory}")
            subprocess.run(cmd, cwd=directory)
            pass
        elif args.action == "build":
            cmd = ["./ecc"];
            if args.dir is not None:
                cmd.extend([os.path.join(args.dir, f) for f in args.file])
            else:
                cmd.extend(args.file)
            print(f"cmd: {' '.join(cmd)}")
            subprocess.run(cmd, cwd="src", check=True)
        elif args.action == "run":
            path = ""
            if args.dir is not None:
                path = args.dir
            cmd = ["sudo", "./ecli", "run", os.path.join(path, "package.json")]
            cmd.extend(extra_args)
            print(f"cmd: {' '.join(cmd)}")

            valid_path = os.path.join("src", os.path.join(path, "package.json"))
            if (os.path.exists(valid_path)):
                subprocess.run(cmd, cwd="src")
        elif args.action == "clean":
            for pattern in ["*.json", "*.o"]:
                cmd = ["find", ".", "-name", pattern, "-delete"]
                print(f"cmd: {' '.join(cmd)}")
                subprocess.run(cmd, cwd="src", check=True)
        elif args.action == "pkghelp":
            path = ""
            if args.dir is not None:
                path = args.dir
            cmd = ["sudo", "./ecli", "run", os.path.join(path, "package.json"), "-h"]
            subprocess.run(cmd, cwd="src")
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
