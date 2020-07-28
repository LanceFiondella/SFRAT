#!/bin/sh

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

commit_website_files() {
  git checkout -b dev
  git add .
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git remote add  https://${GITHUB_TOKEN}@github.com/LanceFiondella/SFRAT/tree/dev > /dev/null 2>&1
  git push --quiet --set-upstream origin HEAD: dev
}


setup_git
commit_website_files
upload_files