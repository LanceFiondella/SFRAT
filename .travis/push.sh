#!/bin/sh

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

commit_website_files() {
  git add -f tests/report.xls
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git remote rm origin
  git remote add origin https://${GITHUB_TOKEN}@https://github.com/LanceFiondella/SFRAT.git > /dev/null 2>&1
  git push origin dev --quiet
}


setup_git
commit_website_files
upload_files