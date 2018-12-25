#!/usr/bin/env bash

DOMAIN="example.com"
if [ ! -z "$1" ]; then
    DOMAIN="$1"
fi

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=linux; extension="";;
    Darwin*)    machine=darwin; extension="";;
    CYGWIN*)    machine=windows; extension=".exe";;
    MINGW*)     machine=windows;extension=".exe";;
    *)          machine="UNKNOWN:${unameOut}"
esac

Architecture=$(uname -m)
case "$Architecture" in
    x86)    Architecture="386"                  ;;
    ia64)   Architecture="amd64"                 ;;
    i?86)   Architecture="386"                  ;;
    amd64)  Architecture="amd64"                    ;;
    x86_64) Architecture="386"                   ;;
    sparc64)    Architecture="sparc64"                  ;;
    arm)    Architecture="arm"                  ;;
* ) echo    "Your Architecture '$Architecture' -> ITS NOT SUPPORTED."   ;;
esac
CFSSL="$PWD/cfssl$extension"
if [ ! -f "$CFSSL"  ]; then
    curl -o "$CFSSL" "https://pkg.cfssl.org/R1.2/cfssl_$machine-$Architecture$extension"
    chmod +x "$CFSSL"
fi
CFSSLJSON="$PWD/cfssljson$extension"
if [ ! -f "$CFSSLJSON"  ]; then
    curl -o "$CFSSLJSON" "https://pkg.cfssl.org/R1.2/cfssljson_$machine-$Architecture$extension"
    chmod +x "$CFSSLJSON"
fi

if [ ! -f root_ca.pem ]; then
    $CFSSL gencert -initca ca-csr.json | $CFSSLJSON -bare root_ca
fi

if [[ $DOMAIN == www* ]] ; then
    DOMAIN_LIST="$DOMAIN,${DOMAIN#\"www.\"}"
else
    DOMAIN_LIST="$DOMAIN,www.${DOMAIN}"
fi

echo '{"key":{"algo":"rsa","size":2048}}' | $CFSSL gencert -ca=root_ca.pem -ca-key=root_ca-key.pem -config=cfssl.json \
    -hostname="$DOMAIN_LIST" - | $CFSSLJSON -bare $DOMAIN
