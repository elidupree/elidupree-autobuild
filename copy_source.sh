#!/bin/bash
rsync -av --del --exclude ".git" --exclude "target/" --exclude ".embuild/" --exclude "build/" --exclude "temp-hilariou*" --exclude "modify_noticer" --exclude "Cargo.lock" --exclude "package-lock.json" --exclude "proptest-regressions/" --exclude "callgrind.out.*" --exclude "node_modules/" --exclude ".idea" "$@"
