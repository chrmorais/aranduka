# Introduction #

This guide is meant to help developers work together to get the most out of this project. It's not supposed to be an exhaustive manual, but rather a simple set of guidelines to help us understand each other.

# Join the team #

Before being able to commit changes to the application you need to have the appropriate privileges. To do so, please join our [mailing list](http://groups.google.com/group/aranduka-discuss) and let us know.

# Getting the code #

The first thing you want to do is get a fresh copy of the source code from the [Git](http://git-scm.com/) repository. You should always clone the **integrate** branch which is the trunk were all working features are merged intoto (see the section below for more information).

```
git clone -b integrate https://code.google.com/p/aranduka/ aranduka 
```

# Git branches #

Aranduka uses [Git](http://git-scm.com/) as distributed source control management tool. In this type of system it's very common to work on many branches at the same time (more common than in Subversion, where merging branches is a bit more complicated).

The idea here is that we have a main branch or trunk (called **integrate**) were all tested features are _integrated_, and a separate branch for each new feature that is under development. In the next section you will see the workflow that has been defined to handle the branches.

# New feature workflow #

We've defined the following workflow to add new features for Aranduka.

Here's the short version:

  1. Create a branch for the new feature
  1. Test the branch separately
  1. Create a local merge of the feature branch with the latest revision of the integrate branch and test it
  1. Merge the feature branch to the integrate branch
  1. Delete the feature branch

(This is called **Topic Branches** on Git's book. Check it out [here](http://git-scm.com/book/en/Git-Branching-Branching-Workflows#Topic-Branches)).

And here's the detailed version:

## Create a branch for the new feature ##

After cloning the **integrate** branch, you will have to create a new branch for the new feature you're developing.

```
git branch new_feature
git checkout new_feature
```

or

```
git checkout -b new_feature
```

Then you will be able to work in that branch, commiting new changes, until you think the feature is ready to be tested.

## Test the branch separately ##

Once you coded the new feature, make sure to test it on your machine, to make sure everything works as expected and that you didn't break any old feature.

## Make a local merge ##

After you've tested the feature branch, you'll need to see if it works with the current version of the integrate branch. It is possible that while you were working on your feature, somebody else has submitted new changes to the integrate branch, so you'll have to update your copy of the integrate branch and merge it with the feature branch.

```
git checkout integrate
git merge new_feature
```

Then test everything to make sure that both your new feature and the rest of the application work as expected

## Close the feature branch ##

Now that your feature branch was merged into the integrate branch, we can delete it (unfortunately, it will still appear in Google Code's page, but hopefully they will change this behavior in the future).

```
git branch -d new_feature
```

## Push the changes to the remote repository ##

Once the new feature is properly tested with the current revision of the integrate branch, you can push the changes to the public repository.

```
git push integrate
```

# Plugins #

Most of the features of Aranduka should be created as plugins (unless, of course, they are core-related features), and therefore should be integrated with the plugin system.

For information on how to develop plugins for Aranduka, check out the [Plugins](Plugins.md) page.

# Discussion and suggestions #

If you have doubts or ideas that you want to share, about this guide or the whole development process, please share them with us using [Aranduka's Google Group](http://groups.google.com/group/aranduka-discuss).

# More information #

Here are some useful links for further information:

  * [Aranduka's Google Group](http://groups.google.com/group/aranduka-discuss)
  * [Git Book](http://git-scm.com/book/en/)
  * [Yapsy](http://yapsy.sourceforge.net/)
  * [Yapsy tutorial by Roberto Alsina](http://lateral.netmanagers.com.ar/weblog/posts/BB923.html)