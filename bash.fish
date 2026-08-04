# 1. Scaffold a metadata file.
kaggle competitions init ./my-comp

# 2. Edit ./my-comp/competition-metadata.json (fill in the INSERT_* placeholders).

# 3. Create the (unlaunched) competition.
kaggle competitions create -p ./my-comp
# → Competition created: https://www.kaggle.com/competitions/my-comp-slug

# 4. Author the description and rules pages.
kaggle competitions pages create my-comp-slug --name description -f ./description.md --publish
kaggle competitions pages create my-comp-slug --name rules -f ./rules.md --publish

# 5. Update the competition data (train.csv, test.csv, sample_submission.csv, ...).
kaggle competitions data update my-comp-slug -p ./data -m "Initial release"

# 6. Upload the private solution CSV, then poll until scoring is ready.
kaggle competitions solution create my-comp-slug -p ./solution.csv
kaggle competitions solution status my-comp-slug
# → Ready: true

# 7. Optionally tune host-only settings not covered by competition-metadata.json
#    (deadlines, runtime caps, leaderboard behavior, etc.).
kaggle competitions settings get my-comp-slug
kaggle competitions settings update my-comp-slug -f ./settings.json

# 8. Launch the competition (now, or schedule a future UTC time).
kaggle competitions launch my-comp-slug --at 2027-01-01T00:00:00Z
node --input-type=module --eval "import { sep } from 'node:path'; console.log(sep);"

echo "import { sep } from 'node:path'; console.log(sep);" | node --input-type=module
git clone https://github.com/pjreddie/darknet
cd darknet
make
# 1. Scaffold a metadata file.
kaggle competitions init ./my-comp

# 2. Edit ./my-comp/competition-metadata.json (fill in the INSERT_* placeholders).

# 3. Create the (unlaunched) competition.
kaggle competitions create -p ./my-comp
# → Competition created: https://www.kaggle.com/competitions/my-comp-slug

# 4. Author the description and rules pages.
kaggle competitions pages create my-comp-slug --name description -f ./description.md --publish
kaggle competitions pages create my-comp-slug --name rules -f ./rules.md --publish

# 5. Update the competition data (train.csv, test.csv, sample_submission.csv, ...).
kaggle competitions data update my-comp-slug -p ./data -m "Initial release"

# 6. Upload the private solution CSV, then poll until scoring is ready.
kaggle competitions solution create my-comp-slug -p ./solution.csv
kaggle competitions solution status my-comp-slug
# → Ready: true

# 7. Optionally tune host-only settings not covered by competition-metadata.json
#    (deadlines, runtime caps, leaderboard behavior, etc.).
kaggle competitions settings get my-comp-slug
kaggle competitions settings update my-comp-slug -f ./settings.json

# 8. Launch the competition (now, or schedule a future UTC time).
kaggle competitions launch my-comp-slug --at 2027-01-01T00:00:00Z
