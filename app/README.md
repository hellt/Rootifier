# PLAZA -- config rootifier
When an engineer configures remote device via telnet/ssh it is safer to use configuration commands in a full-context fashion.
This best-practice comes from a sad fact that large configuration snippets may render corrupted while 
pasting large chunks of data procedure in the terminal window. 
Chances are you end up with an inconsistent configuration or even an outage.

With this script one can transform tree-based config into full-context (aka display-set) in a blink of an eye.

This script is a part of a [PLAZA](http://noshut.ru/2016/04/building-web-front-end-for-python-scripts-with-flask/) project.