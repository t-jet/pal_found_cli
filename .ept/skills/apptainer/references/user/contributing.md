# Contributing
Apptainer is an open source project, meaning we have the challenge of limited resources. We are grateful for any support that you can offer. Helping other users, raising issues, helping write documentation, or contributing code are all ways to help!
## Join the community
This is a huge endeavor, and your help would be greatly appreciated! Post to online communities about Apptainer, and request that your distribution vendor, service provider, and system administrators include Apptainer for you!
You can reach the community through the mailing list or Slack. Links to join those are on the [apptainer help page](https://apptainer.org/help/).
## Raise an Issue
For general bugs/issues, you can open an issue [at the GitHub repo](https://github.com/apptainer/apptainer/issues/new). However, if you find a security related issue/problem, please email the Apptainer Security Team directly at security@apptainer.org. More information about the Apptainer security policies and procedures can be found [here](https://apptainer.org/security-policy/)
## Write Documentation
We (like almost all open source software providers) have a documentation dilemma… We tend to focus on the code features and functionality before working on documentation. And there is very good reason for this: we want to share the love so nobody feels left out!
You can contribute to the documentation by [raising an issue to suggest an improvement](https://github.com/apptainer/apptainer-userdocs/issues/new) or by sending a [pull request](https://github.com/apptainer/apptainer-userdocs/compare) on [our repository for documentation](https://github.com/apptainer/apptainer-userdocs).
The current documentation is generated with:
  * [reStructured Text (RST)](http://docutils.sourceforge.net/rst.html) and [ReadTheDocs](https://readthedocs.org/).


Other dependencies include:
  * [Python 3.5 or newer](https://www.python.org/downloads/).
  * [Sphinx](https://pypi.org/project/Sphinx/).


More information about contributing to the documentation, instructions on how to install the dependencies, and how to generate the files can be obtained [here](https://github.com/apptainer/apptainer-userdocs/blob/main/README.md).
For more information on using Git and GitHub to create a pull request suggesting additions and edits to the docs, see the [section on contributing to the code](contributing.md#contribute-to-the-code). The procedure is identical for contributions to the documentation and the code base.
## Contribute to the code
We use the traditional [GitHub Flow](https://guides.github.com/introduction/flow/) to develop. This means that you fork the main repo, create a new branch to make changes, and submit a pull request (PR) to the main branch.
Check out our official [CONTRIBUTING.md](https://github.com/apptainer/apptainer/blob/main/CONTRIBUTING.md) document, which also includes a [code of conduct](https://github.com/apptainer/apptainer/blob/main/CONTRIBUTING.md#code-of-conduct).
### Step 1. Fork the repo
To contribute to Apptainer, you should obtain a GitHub account and fork the [Apptainer](https://github.com/apptainer/apptainer) repository. Once forked, clone your fork of the repo to your computer. (Obviously, you should replace `your-username` with your GitHub username.)

```
$ git clone https://github.com/your-username/apptainer.git && \
    cd apptainer/

```

### Step 2. Checkout a new branch
[Branches](https://guides.github.com/introduction/flow//) are a way of isolating your features from the main branch. Given that we’ve just cloned the repo, we will probably want to make a new branch from main in which to work on our new feature. Lets call that branch `new-feature`:

```
$ git checkout main && \
    git checkout -b new-feature

```

Note
You can always check which branch you are in by running `git branch`.
### Step 3. Make your changes
On your new branch, go nuts! Make changes, test them, and when you are happy commit the changes to the branch. The Apptainer requires that all contributed git commits use the `-s` option which adds a `Signed-off-by` line to indicate agreement with the [Developer Certificate of Origin](https://developercertificate.org).

```
$ git add file-changed1 file-changed2...

$ git commit -s -m "what changed?"

```

This commit message is important - it should describe exactly the changes that you have made. Good commit messages read like so:

```
$ git commit -s -m "changed function getConfig in functions.go to output csv to fix #2"

$ git commit -s -m "updated docs about shell to close #10"

```

The tags `close #10` and `fix #2` are referencing issues that are posted on the upstream repo where you will direct your pull request. When your PR is merged into the main branch, these messages will automatically close the issues, and further, they will link your commits directly to the issues they intend to fix. This will help future maintainers understand your contribution, or (hopefully not) revert the code back to a previous version if necessary.
### Step 4. Push your branch to your fork
When you are done with your commits, you should push your branch to your fork (and you can also continuously push commits here as you work):

```
$ git push origin new-feature

```

Note that you should always check the status of your branches to see what has been pushed (or not):

```
$ git status

```

### Step 5. Submit a Pull Request
Once you have pushed your branch, then you can go to your fork (in the web GUI on GitHub) and [submit a Pull Request](https://help.github.com/articles/creating-a-pull-request/). Regardless of the name of your branch, your PR should be submitted to the Apptainer `main` branch. Submitting your PR will open a conversation thread for the maintainers of Apptainer to discuss your contribution. At this time, the continuous integration that is linked with the code base will also be executed. If there is an issue, or if the maintainers suggest changes, you can continue to push commits to your branch and they will update the Pull Request.
### Step 6. Keep your branch in sync
Cloning the repo will create an exact copy of the Apptainer repository at that moment. As you work, your branch may become out of date as others merge changes into the upstream main. In the event that you need to update a branch, you will need to follow the next steps:

```
$ git remote add upstream https://github.com/apptainer/apptainer.git && # to add a new remote named "upstream" \
    git checkout main && # or another branch to be updated \
    git pull upstream main && \
    git push origin main && # to update your fork \
    git checkout new-feature && \
    git merge main

```

