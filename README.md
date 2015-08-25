#debug chrome protocol
- window 1

	/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --no-first-run --user-data-dir=~/temp/chrome-dev-profile http://localhost:9222 http://chromium.org
	http://localhost:9222/devtools/inspector.html?ws=192.168.99.100:9000/ws
	# then click on the chromium tab
	
- window 2

	http://localhost:9222/json
	find websocketdebuggerurl
	chrome-devtools://devtools/bundled/devtools.html?ws=localhost:9222/devtools/page/60333B1C-DF75-450A-BBB0-7B971D9F935C
	reload window 1
	find websocket, view connection informaiton
	
