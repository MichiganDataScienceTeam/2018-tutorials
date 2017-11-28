# MDST Flux Tutorial

Jonathan Stroud

November 28, 2017

**Disclaimer:** This guide to Flux is meant as a brief tutorial, and
  intentionally leaves out some crucial information. For a
  comprehensive tutorial, see the [Flux User
  Guide](http://arc-ts.umich.edu/flux-user-guide/).

## What is Flux?

**Flux** is a shared computing cluster used by students and
  researchers at U of M. Flux is managed by Advanced Research
  Computing - Technology Services (ARC-TS).

Flux contains:
 - 1,372 compute nodes
 - 27,000 cores
 - Minimum 4GB RAM per core

There are several node types:
 - **CPU**
 - **GPU + CPU**
 - CPU + extra RAM
 - HIPAA-compliant CPU
 - Hadoop
 - Custom nodes
 - ... several others
 
Several storage options:
 - **Home directory** across Flux for permament small files
 - **Scratch space** across Flux for temporary large file storage
 - **Temp space** per node for temporary files during compute jobs
 - Long-term disk storage for permanent large files

For more information about Flux, refer to the [ARC-TS
website](http://arc-ts.umich.edu/resources/compute-resources/).

## Creating an Account

Before you join our MDST flux allocation, you need a general Flux
account. Fill out [**this form**](http://arc-ts.umich.edu/fluxform/)
to create an account.

To log in to flux, you will have to set up two-factor authentication.
Follow the instructions on the flux signup form for more information.

Once you have a flux account, you can join the MDST allocation
account. MDST does not add all members to our Flux allocation accounts
automatically. To be added, message Jonathan Stroud (@stroud).

## MDST Allocation Accounts

MDST has access to a CPU allocation and a GPU allocation. You should
use whichever is most appropriate for your work.

### `mdatascienceteam_flux`

This allocation account contains only CPUs, and is part of the regular
flux CPU cluster.

```
mdatascienceteam_flux
CPUs:           1000
Memory:         4TB
Queue:          preempt
Scratch space:  /scratch/mdatascienceteam_flux/
```

These cores are provided as part of the **preempt** queue. This means
that MDST does not own or rent a specific block of cores. Instead, we
have the ability to use any currently-unused cores for a short amount
of time. There is a small chance that, when using this queue, a job
will be cancelled because its cores are needed by another user. While
this does not seem to happen frequently, you should always
periodically save the progress of your job so that you can pick up on
it later if it is cancelled.

We graciously acknowledge free use of the Flux preempt queue from
ARC-TS.

### `mdstproject_fluxg`

In addition, we have two NVIDIA K40 GPUs available for special
projects that require additional computing resources. Access to GPU
resources is limited and granted as needed.

```
mdstproject_fluxg
GPUs:           2
CPUs:           4
Memory:         16GB
Queue:          fluxg
Scratch space:  /scratch/mdstproject_fluxg/
```

These GPUs are not part of the preempt queue, but you should still
periodically save the progress of your jobs when using the GPUs. This
will help you recover if your job ends due to an unexpected bug.

We graciously acknowledge donation of these GPUs by NVIDIA.

## Logging In & The Login Node

Most of the work you do on Flux will be on the **login node**. From
this machine, you can write code, launch jobs, and check on your
running jobs. You should not use this node to run code!

To enter the login node, open a terminal window and `ssh` in
(replacing `uniqname` with your uniqname):

```
$ ssh uniqname@flux-login.arc-ts.umich.edu
```

**Note:** you must be on the UofM network or VPN in order to use Flux.
  Otherwise, the above step will not work.

If you use a Windows machine, you can use
[putty](http://www.putty.org/) to SSH into flux.

You'll be prompted for both an MToken code and a password when you log
in.

### The `home` Directory

Once logged in, you'll be in your `home` directory.

This directory is intended for code and other small files that are
shared across your current jobs. It is not intended to for large
datasets or long-term storage.

Each user has a strict **80GB quota** in `/home/`. If you need more
storage space, use `/scratch/`.

### The `scratch` Directory

The `scratch` space is intended for temporary storage of large files.
For optimal performance, you should store your data as a few large
files rather than many small files. 

To navigate to your `scratch` directory:

```
$ cd /scratch/mdatascienceteam_flux/uniqname
```

In this directory, you have essentially unlimited temporary storage
space. **Any data that is stored here will be deleted after 90 days if
not in use.** We recommend periodically backing up your important
code and data to another location, such as MBox or Google Drive.

## PBS Jobs

To run compute jobs on Flux, you must first request nodes using the
`qsub` command. Typically, we use `qsub` by passing a PBS script,
which contains a request for resources and the job commands.

This repository contains a few examples of PBS scripts. To clone this
git repository to flux (and access the scripts), you'll first need to
set up an SSH key for use with Github. Refer to Github's tutorial on
the subject
[here](https://help.github.com/articles/generating-an-ssh-key/). Once
you've done that, you should be able to clone the directory as
follows:

```
$ cd ~
$ git clone git@github.com:MichiganDataScienceTeam/tutorials.git
$ cd tutorials/flux
```

### PBS scripts

Let's take a look at `flux_template.pbs`. This PBS script launches a
job on the `mdatascienceteam_flux` allocation account. Let's take a
look at a few important parts:

Here, you can replace `job_name` with whatever you want, like
`randomforest_train`. Pick something descriptive!

```
#PBS -N job_name
```

Here, make sure to replace `uniqname` with your actual uniqname:

```
#PBS -M uniqname@umich.edu
```

This line specifies how much computing power you want. Make sure to
request a little more than you think you need (but not too much!). As
is, we are requesting 2 CPUs on 1 node (each node has 16
CPUs) and 8GB of RAM, for 1 hour. If your job ends before
time is up, nothing bad will happen. However, if time is up before
your job ends, you might lose the results of your computation. It's
therefore good practice to save intermediate snapshots of your results
when running long jobs.

```
#PBS -l nodes=1:ppn=2,mem=8GB,walltime=01:00:00
```

At the end of the script, you can run whatever commands you want.
These commands will run on CPU nodes.

```
#  Put your job commands here:
echo "Hello, world"
```

Try modifying `flux_template.pbs` to make it load and run a python
script of your choosing, and save it as `myfirstpbs.pbs`. You can
submit the job to flux by entering the following:

```
$ qsub pbs/myfirstpbs.pbs
```

You'll receive an email when the job starts running, and an additional
email when it either aborts or completes. Once the job completes, it
will create a file called `<job_name>.o<job_id>` which contains the
job output. When I ran it, it looked like this:

```
$ cat job_name.o25820895
nyx6201
nyx6201
Hello, world
$
```

### Interactive Jobs

Often, you'll want to test things out interactively before submitting
big jobs. You can spawn an interactive session on Flux by including
the `#PBS -I` flag in your PBS scripts. For convenience, we've
included a script that will launch an interactive session. To launch,
simply run the script (no need to qsub, the script will qsub itself):

```
$ ./interactive_flux.sh
```

Make sure to edit the file to include your own uniqname first.

## Checking the Queue

While your jobs run, you may want to check their status. You can view
all of your current jobs using:

```
$ qstat -u $USER
```

To view all of the current jobs for our CPU allocation:

```
$ showq -w acct=mdatascienceteam_flux
```

### Job Statuses

In the output of `showq`, you will see that jobs have several possible
statuses.

- `active`: the job is currently running or starting.
- `eligible`: the job is queued and eligible to start.
- `blocked`: the job is queued and not eligible to start.

Jobs are typically blocked because they require more resources than
what is available. If your job is blocked for a long period of time,
check your PBS script for errors.

## Modules

Flux uses a program called `Lmod` to manage software installations and
versions. Each piece of software is loaded as a module, which may have
dependencies in other modules. Modules are incredible helpful when
you, for example, need to run code that works on a specific version of
Python, or need to compile a library with a specific version of a
compiler.

To view your currently-loaded modules:

```
$ module list
```

To view available modules, or available version of a specific module:

```
$ module av
$ module av matlab
```

To load a module:

```
$ module load matlab/R2016a
```

To unload module:

```
$ module unload matlab
```

If you frequently use a particular combination of modules, you can
save it using:

```
$ module save my_modules
```

and reload it at any time:

```
$ module purge
$ module restore my_modules
```

The `default` module list can be changed in the same way, and will be
loaded whenever you log in to Flux.

### PBS and Modules

When a job starts, it will load the default module list. If you need
an alternate set of modules, you can load them via `module load`
within your PBS script.

## Creating Modules

If and when you install software on Flux, you should create new
modules to manage it. To create a private module:

First, create a place to store your modules. We recommend putting all
your modules in a subdirectory called `$USER`, to ensure that each of
your modules is named `$USER/mymodule`. This helps distinguish your
private modules from shared modules.

```
mkdir $HOME/privatemodules/$USER
```

Tell Lmod where to find your modules.

```
module use $HOME/privatemodules
```

Install some software. Let's say you want to install Python/Anaconda
locally. You can follow the installation instructions
[here](https://docs.anaconda.com/anaconda/install/), and make sure to
set the install location somewhere in your `$HOME` directory, such as
`$HOME/libs/python-anaconda3`.

Now, we create a modulefile, a short lua script which tells Lmod what
changes to make to our environment variables in order to load the
software. Let's say you installed Anaconda 3.6. You should named your
modulefile `$HOME/privatemodules/$USER/python-anaconda3/3.6.lua`.

Your modulefile should look like this:

```
local base_dir = "$HOME/libs"
local version = "3.6"
local name = "python-anaconda3"
prepend_path('PATH', pathJoin(base_dir, name, '/bin'))
```

The key piece here is `prepend_path`. This function adds the location
of the anaconda python interpreter to the front of the `$PATH`
variable, meaning that it will be used instead of the default python
installation on Flux.

To load your new module:

```
$ module load $USER/python-anaconda3/3.6
```

Your new module works just like any other. You can unload it or save
it to your defaults.

For more information on Lmod, please refer to the [Lmod
documentation](https://lmod.readthedocs.io/en/latest/)

## Flux Policies and Best Practices

Please refer to MDST's [Flux User Policy
Notebook](https://docs.google.com/a/umich.edu/document/d/199L4IKaz0tpHPDDeZvtSwkagsuqlEpFhBlCydrlG6K0/edit?usp=sharing)
for computing a complete list of policies. In general,

*Do*:
- Use MDST Flux allocations for MDST projects
- Use MDST Flux allocations to learn and practice new data science skills
- Back up your code and data
- Save intermediate progress during large jobs
- Ask if you have questions or concerns

*Do not*:
- Use MDST Flux allocations for personal research
- Use MDST Flux allocations for class projects
- Run significant computation on the login node
- Request more resources than you need
- Use `scratch` for permanent storage
- Request interactive jobs > 4 hrs


### Computing Support

If you run into trouble with Flux, you should check out MDST's
#computing channel on our Slack workspace. Feel free to ask questions,
or search through the history to see if your question has already been
addressed.

Otherwise, please contact hpc-support@umich.edu with questions. They
are very responsive and helpful!
