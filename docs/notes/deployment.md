# Deployment

I am re-deploying the project on EC2 since I wanted to change the machine type I'm using. This is a good opportunity to document what I do during the deployment process so that I can automate it at a later stage.

## General

1. Start EC2 machine (I've used a Ubuntu image type with two EBS volumes; an 8GB root volume and a 22GB data volumn that does not delete on termination).
2. Configure local SSH alias to allow connecting to the machine.
3. `sudo apt-get update`
4. Add an SSH key for Github using [this link](https://help.github.com/articles/generating-ssh-keys/) (note that I had to manually copy the public key since pbcopy does not come pre-installed and I couldn't find it).
5. `mkdir -p projects && git clone git@github.com:jdgillespie91/trackerSpend.git projects/trackerSpend`
6. Copy over config file from local.

## Virtual environment

1. `sudo apt-get install python-pip`
2. `sudo pip install virtualenv`
3. `mkdir -p .envs && virtualenv -p /usr/bin/python3.4 .envs/trackerSpend`

## .bashrc

1. Add the following to `~/.bashrc`.
```bash
# trackerSpend configuration.
function trackerSpend {
    virtual_env_dir="/home/ubuntu/.envs/trackerSpend"
    base_dir="/home/ubuntu/projects/trackerSpend"

    if [ -d "${virtual_env_dir}" ]; then
        source "${virtual_env_dir}/bin/activate"
        if [ "$?" -eq "0" ]; then
            echo "Virtual environment activated: ${virtual_env_dir}."
        fi
    fi

    if [ -d "${base_dir}" ]; then
        cd "${base_dir}"
        if [ "$?" -eq "0" ]; then
            echo "Moved to base directory: ${base_dir}."
        fi  

        export PYTHONPATH="${PYTHONPATH}:${base_dir}"
        if [ "$?" -eq "0" ]; then
            echo "Appended base directory to PYTHONPATH: ${PYTHONPATH}."
        fi
    fi
}
```
