#!/bin/bash
mkdir /n/autobuild/$1
mkdir /n/autobuild/$1/scripts
mkdir /n/autobuild/$1/build
printf "#!/bin/bash\n/n/elidupree-autobuild/watch.py /n/documents-share/$1/modify_noticer /n/autobuild/$1/scripts/build.sh 1000000"> /n/autobuild/$1/scripts/watch.sh
printf "#!/bin/bash\n/n/elidupree-autobuild/copy_source.sh /n/documents-share/$1/ /n/autobuild/$1/build\ncd /n/autobuild/$1/build\nexport RUST_BACKTRACE=1\ncargo update && cargo run"> /n/autobuild/$1/scripts/build.sh
chmod +x /n/autobuild/$1/scripts/watch.sh
chmod +x /n/autobuild/$1/scripts/build.sh
