# 5905-fall-2021 - Noah and Brian's project
The files changed (different from envoy-master) are as follows:

For c++: 
- envoy/source/extensions/health_checkers/redis/redis.cc
- envoy/source/extensions/health_checkers/redis/redis.h

To compile envoy into a binary which can be used in our sample environment, run the following commands in a Linux environment (with Docker installed) in the envoy directory:

1. sudo ENVOY_DOCKER_BUILD_DIR='envoy_build_directory' ./ci/run_envoy_docker.sh './ci/do_ci.sh bazel.release.server_only'
    - This will compile envoy and create a binary. Substitute the envoy_build_directory with whatever directory you want. Note this takes a powerful PC with a large amount of disk space.
2. sudo docker build --build-arg TARGETPLATFORM="./linux/amd64" -f ci/Dockerfile-envoy -t envoy .
    - This will take the compiled binary and turn it into a local Docker image called 'envoy'
3. sudo docker tag envoy:latest briangregg/envoy-noah:latest
    - This tags the remote docker image as our new envoy image
4. sudo docker push briangregg/envoy-noah:latest
    - Pushes our changes to the remote docker image. This is the image we used in our environment, but you can also use any Dockerhub image you want (or create your own)

To start up our environment and test the load balancer, run these commands in the directory envoy/examples/front-proxy:

1. docker-compose up -d
    - This brings up the two services, front-proxy and service1
2. docker-compose scale service1=x
    - Scales service1 up to x nodes
3. bash ./test_load_balancer.sh
    - Tests the load balancer with the new health check by sending Redis requests and printing which servers the requests get routed to
