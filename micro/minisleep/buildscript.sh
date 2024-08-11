#!/bin/sh
set -e
builder=$(buildah from registry.redhat.io/ubi9/ubi)
container=$(buildah from registry.redhat.io/ubi9-micro)
mountpoint=$(buildah mount ${container})


# --installroot ${mountpoint}
# Install dependencies into the runtime container
buildah run ${builder} -- bash -C <<EOF
    yum remove --installroot ${mountpoint} --releasever 9 bash sh
    yum list installed --installroot ${mountpoint}
    yum clean all --installroot ${mountpoint}
EOF

echo "hello" > ${mountpoint}/hello.txt

buildah commit --format docker ${container} microsleep
buildah unmount ${container}

