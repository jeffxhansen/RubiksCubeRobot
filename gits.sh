echo "Current directory: "
pwd
echo "\n"

# argument one is "<commit message>"
message=$1
# argument two is <branch>
branch=$2

# if the message argument isn't passed, set it to "syncing"
if [ -z "$message" ]; then
  message="syncing"
fi

# automatically detect the current branch if not passed in after the message
if [ -z "$branch" ]; then
  branch=$(git rev-parse --abbrev-ref HEAD) # Automatically detect the current branch
fi

echo "Adding, commiting, pulling and pushing to GitHub with message: $message on branch: $branch"

git add --all --verbose;
git commit -m "$message";
git pull --no-edit origin $branch;
git push origin $branch;