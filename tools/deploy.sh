#!/bin/bash
# usage: deploy.sh REPO_DIR NAME   (NAME = netlify site name = surge subdomain)
set -e
R=$1; N=$2; D=/tmp/dist-$N
rm -rf $D && mkdir -p $D
(cd $R && tar --exclude=.git --exclude=__pycache__ --exclude=_shots --exclude=.netlify --exclude=tools --exclude=node_modules --exclude='*.py' --exclude=.netrc --exclude=.env --exclude=CNAME --exclude='*.secret' -cf - .) | (cd $D && tar xf -)
TOK=$(python3 -c 'import json;print(json.load(open("/home/box/agent-data/box-secrets.json"))["card"]["NETLIFY_AUTH_TOKEN"])')
SID=$(curl -s -H "Authorization: Bearer $TOK" "https://api.netlify.com/api/v1/sites?name=$N&filter=all" | python3 -c "import json,sys;n=sys.argv[1];print(next((s['id'] for s in json.load(sys.stdin) if s['name']==n),''))" $N)
if [ -z "$SID" ]; then SID=$(curl -s -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d "{\"name\":\"$N\"}" https://api.netlify.com/api/v1/sites | python3 -c 'import json,sys;print(json.load(sys.stdin)["id"])'); echo "created netlify site"; fi
python3 -c "import shutil,sys;shutil.make_archive(\"/tmp/\"+sys.argv[1],\"zip\",sys.argv[2])" $N $D
curl -s -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/zip' --data-binary @/tmp/$N.zip "https://api.netlify.com/api/v1/sites/$SID/deploys" | python3 -c 'import json,sys;d=json.load(sys.stdin);print("netlify deploy",d.get("id"),d.get("state"),d.get("ssl_url") or d.get("url"))'
surge $D $N.surge.sh 2>&1 | tail -3
