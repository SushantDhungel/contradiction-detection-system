# For nested branch
git pull phase-1
git switch -c feat/new-branch

# work, commit, push
(in new branch)
git add .
git commit -m "msg"
git push origin feat/new-branch
(still in newbranc)
gh pr create --base phase-1 --fill
gh pr merge

(now switched to phase -1)
git pull phase-1
