#debug chrome protocol
- window 1

	/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --no-first-run --user-data-dir=/tmp/chrome-dev-profile http://localhost:9222 http://chromium.org
	http://localhost:9222/devtools/inspector.html?ws=proxy.bandit.io:9000/ws/all
	# then click on the chromium tab
	
- window 2

	http://localhost:9222/json
	find websocketdebuggerurl
	chrome-devtools://devtools/bundled/devtools.html?ws=localhost:9222/devtools/page/97EB937F-B13F-416B-A2CD-98A8453B4314
	reload window 1
	find websocket, view connection informaiton
	

http://blog.webernetz.net/2014/01/22/at-a-glance-http-proxy-packets-vs-normal-http-packets/