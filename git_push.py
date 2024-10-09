import git
import os
import argparse
from datetime import datetime


def git_push(commit_message, branch="main", path="."):
    try:
        repo = git.Repo(path)

        changelog_path = os.path.join(path, "changelog.txt")
        with open(changelog_path, "a") as changelog_file:
            changelog_file.write(f"{commit_message}\n")
        print(f"Commit message written to {changelog_path}")

        repo.git.add(A=True)
        print(commit_message)
        repo.index.commit(commit_message)
        print(f"Changes committed to {branch} branch.")
        origin = repo.remote(name='origin')
        push_info = origin.push(refspec=branch)
        
        for info in push_info:
            if info.flags & info.ERROR:
                print(f"Error: {info.summary}")
            else:
                print(f"Success: {info.summary}")

    except git.exc.GitCommandError as e:
        print(f"Git command error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Push changes to git repository.")
    parser.add_argument("commit_message", type=str, nargs='?', default="commit", help="The commit message for the changes.")
    parser.add_argument("--branch", type=str, default="main", help="The branch to push the changes to.")
    parser.add_argument("--path", type=str, default=".", help="The path to the git repository.")
    args = parser.parse_args()
    
    # 取得當前時間並格式化
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_commit_message = f"{args.commit_message} - {current_time}"
    
    git_push(full_commit_message, args.branch, args.path)