# examining the ssl certs for senate.gov and house.gov

this code tests US Capitol websites for valid HTTPS configurations. there are
two major bits of code. `capitolhttpstester.py` and `maketable.py`.  i would
like to state in my defense i obviously don't know html at all or i would not
have done it that way. 

the article that accompanies this post is >
https://sunlightfoundation.com/blog/2015/05/26/sunlight-analysis-reveals-15-of-congressional-websites-are-https-ready

`captiolhttpstest.py` -- goes out and creates a json summary

`maketable.py` -- parses that json summary and creates a webpage evaluating and summarizing the results. 

`get-cert.sh` -- simple script to go and get SSL certificate for hostname, because learning how to use openssl is painful.

`install.sh` -- simple script to create virtual env to get this thing up and running not the same as actually making a package!

`settings.py.example` -- should be copied to `settings.py` with proper sunlight api key 

all code is GPLv2.0

--timball@sunlightfoundation.com
2015-05-25
