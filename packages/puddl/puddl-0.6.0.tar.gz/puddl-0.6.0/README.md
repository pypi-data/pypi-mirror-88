# Prerequisites
- Python 3.8 (a virtual environment is recommended)
- PostgreSQL


# Installation from Source
```
mkdir ~/puddl
git clone https://gitlab.com/puddl/puddl.git
cd ~/puddl/puddl/
pip install -e .
```

Install completion for bash (for other shells please refer to [the click
documentation][click-completion]):
```
mkdir -p ~/.bash/
_PUDDL_COMPLETE=source_bash puddl > ~/.bash/puddl

cat <<'EOF' >> ~/.bashrc
[[ -f ~/.bash/puddl ]] && source ~/.bash/puddl
EOF

exec $SHELL
```
[click-completion]: https://click.palletsprojects.com/en/7.x/bashcomplete/#activation-script

Initialize the database. The command `puddl config init` will consume the `.env`
file if present in the current working directory.
```
cd ~/puddl/puddl/

# generate environment variables suitable for development
./env/dev/generate_env_file.sh > .env

# write initdb script and start postgres
./env/dev/create_database.sh

# based on the environment, write ~/.puddlrc
puddl config init

# make sure initialization was successful
puddl db health

# apply library sql functions as "puddl" user in "public" schema
cat puddl/db/init_sql/*.sql | puddl db shell
```

Try it:
```
puddl app add puddl.felix.file
puddl file db create

puddl file index README.md
puddl file ls

puddl db shell
```


# Writing an App
The following creates a schema `foo` and binds an engine to it:
```
from puddl.db.alchemy import App
app = App('foo')
app.engine
```


# Development
Run flake8 before committing
```
ln -s $(readlink -m env/dev/git-hooks/pre-commit.sample) .git/hooks/pre-commit
```

Basic development workflow:
```
# hack, hack
make
```

Got `psql` installed?
```
source <(puddl db env)
echo "SELECT path, stat->>'st_uid' as uid FROM file.file" | psql
```


# Rsync Service
```
cat ~/.ssh/id_*.pub > $PUDDL_HOME/rsync_authorized_keys
ln -s env/dev/docker-compose.override.yml
docker-compose build && docker-compose up -d
```
