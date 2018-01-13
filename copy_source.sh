#!/bin/bash
rsync -av --exclude ".git" --exclude "target" --exclude "temp-hilariou*" --exclude "modify_noticer" --exclude "Cargo.lock" --exclude "package-lock.json" $1 $2
