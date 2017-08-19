#! /bin/sh

cat <<EOF
[![Build Status](https://travis-ci.org/JosefFriedrich-shell/$PROJECT_NAME.svg?branch=master)](https://travis-ci.org/JosefFriedrich-shell/$PROJECT_NAME)

# $PROJECT_NAME

## Summary / Short description

> $SHORT_DESCRIPTION

## Usage

\`\`\`
$USAGE
\`\`\`

## Testing

\`\`\`
make test
\`\`\`
EOF
