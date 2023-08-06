# sym-flow-cli

Sym Flow CLI

## Usage

### Login

`symflow login` is used to authenticate a user and write credentials to the local filesystem. 

First, the CLI asks a user for their email address. From the address, Sym should be able to resolve the user's 
organization and then the user can log in with one of two authorization flows:

#### (Preferred) Auth Code Flow with PKCE

`symflow login`

The CLI will perform authorization with the Sym auth provider, by opening the browser and asking the user
to login with their Identity Provider. If successful, this returns a code to the CLI that can be used to 
securely acquire an access token. 

#### (If necessary) Password Owner Resource Flow

`symflow login --no-browser` can be used to perform a username-password flow. It will prompt the user, and then 
send these credentials to the Sym auth provider in exchange for an access token. 

This requires special setup in the Sym auth provider to verify the password against a database connection. 
