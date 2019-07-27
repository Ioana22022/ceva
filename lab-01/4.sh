#!/bin/bash

##
# straceme generates a password and writes it to /tmp/cnsXXXXX, and after that
# destroys the file using unlink. Also it expects to be given a parameter, which
# in this case, should be the password. $ebp+0x8 stores the first argument given
# to main(), argc. You did not supply any parameters when running ./straceme so
# this is why argc evaluates to 1. To read the password, open straceme with gdb
# add breakpoint in main, hit "run 1"(or anything, you need 2 paramteres)
# and add a breakpoint just before unlink has been called (b unlink), and then
# hit continue. The password is written in the file /tmp/cnsXXXXX.
##
./straceme sixoclockofachristmasmorning
