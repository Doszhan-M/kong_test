FROM kong/kong:2.7.0

ENV OIDC_PLUGIN_VERSION=1.2.3-2
ENV JWT_PLUGIN_VERSION=1.1.0-1
ENV GIT_VERSION=2.24.4-r0
ENV UNZIP_VERSION=6.0-r7
ENV LUAROCKS_VERSION=2.4.4-r1


USER root
RUN apk update && apk add git unzip luarocks
RUN luarocks install kong-oidc

RUN git clone --branch v1.2.3-2 https://github.com/revomatico/kong-oidc.git
WORKDIR /kong-oidc
RUN luarocks make

RUN luarocks pack kong-oidc ${OIDC_PLUGIN_VERSION} \
     && luarocks install kong-oidc-${OIDC_PLUGIN_VERSION}.all.rock

ENV KONG-PLUGINS=bundled,oidc
ENV KONG_PLUGINS=bundled,oidc

USER kong
