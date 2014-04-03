#!/bin/sh
 
javabin=java
scdir=/usr/lib/jitsi
libpath="$scdir/lib"
classpath="$libpath/jdic_stub.jar:$libpath/jdic-all.jar:$libpath/felix.jar:$libpath/bcprovider.jar:$scdir/sc-bundles/sc-launcher.jar:$scdir/sc-bundles/util.jar"
felix_config="$libpath/felix.client.run.properties"
log_config="$libpath/logging.properties"
 
# set add libpath to LD_LIBRARY_PATH for any sc natives (e.g. jmf .so's)
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}$libpath/native"
 
cd -- "$scdir" &&
  exec "$javabin" \
    -classpath "$classpath" \
    -Djna.library.path="$libpath/native" \
    -Dfelix.config.properties="file:$felix_config" \
    -Djava.util.logging.config.file="$log_config" \
    net.java.sip.communicator.launcher.SIPCommunicator