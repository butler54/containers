builder=$(buildah from registry.redhat.io/ubi9/ubi)
container=$(buildah from registry.redhat.io/ubi9-micro)
mountpoint=$(buildah mount ${container})




# Install dependencies into the runtime container
buildah run ${builder} --volume $mountpoint:/hello:z -- bash -C <<EOF
    yum install -y \
        --installroot /hello --releasever 9 \
        --setopt install_weak_deps=false \
        --nodocs \
        httpd
    yum clean all --installroot /hello
EOF

buildah commit --format docker ${container} ubi-micro-httpd
buildah unmount ${container}

