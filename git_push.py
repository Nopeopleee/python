import git
import os

def git_push():
    try:
        repo = git.Repo(os.getcwd())
        repo.git.add(A=True)
        repo.index.commit("commit message")
        origin = repo.remote(name='origin')
        push_info = origin.push(refspec='main')
        
        for info in push_info:
            if info.flags & info.ERROR:
                print(f"Error: {info.summary}")
            else:
                print(f"Success: {info.summary}")
    except git.exc.GitCommandError as e:
        print(f"Git command error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

git_push()