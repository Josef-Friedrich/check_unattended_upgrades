#! /bin/sh

PROJECT_NAME="$(basename "$(pwd)")"

. ./test/lib/test-helper.sh

source_exec skeleton.sh

> README.md

########################################################################

cat <<EOF >> README.md
[![Build Status](https://travis-ci.org/JosefFriedrich-shell/$PROJECT_NAME.svg?branch=master)](https://travis-ci.org/JosefFriedrich-shell/$PROJECT_NAME)

# $PROJECT_NAME
EOF

###### README HEADER ###################################################

echo >> README.md
[ -f README-header.md ] && cat README-header.md >> README.md
echo >> README.md

### SHORT_DESCRIPTION ##################################################

echo '## Summary / Short description' >> README.md
echo >> README.md
echo "> $SHORT_DESCRIPTION" >> README.md
echo >> README.md

### USAGE ##############################################################

cat <<'EOF' >> README.md
## Usage

```
EOF
echo "$USAGE" >> README.md
echo '```'  >> README.md

### TESTING ############################################################

cat <<'EOF' >> README.md
## Testing

```
make test
```
EOF

### README FOOTER ######################################################

echo >> README.md
[ -f README-footer.md ] && cat README-footer.md >> README.md
