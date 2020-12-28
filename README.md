# AWS Credentials sourced from KeePass

## Why do you need this?
- Do you use [KeePass](https://keepass.info/) to manage your secrets?
- Do you work with AWS and frequently need to source your credentials in to your terminal so that you can use the AWS CLI?
- Are you using OSX

If you answered yes to the above three questions, then this tool may be of use to you. 

## Requirements
- `keepassxc-cli`: This can be installed along with [KeePassXC](https://keepassxc.org/). For easy installation you can just use `brew install --cask keepassxc`
- Python: This was tested using `2.7.17`
- Add the following to your bash environment `export KEEPASS_DB=<path to your keepass DB`

## Usage
- Create entries in your KeePass database where the username is the AWS access key and the password is the AWS secret
- Create a new bash terminal that has your credentials sourced by running the command `aws-creds.py <path to entry>`
- Enter your KeePass DB password and a new bash terminal will be created (indicated by the change to your bash prompt, which will have the entry name.
- Close the bash terminal with to go back to the original terminal where your credentials are not present



