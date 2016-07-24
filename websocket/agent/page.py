class Page():

    @staticmethod
    def enable():
        """
            https://developer.chrome.com/devtools/docs/protocol/1.1/page#page.enable
        """
        return {
            "error": "Unimplemented"
        }

    @staticmethod
    def canScreencast():
        return {
            "error": "Unimplemented"
        }

    #@staticmethod
    #def getResourceTree():
    #    return {"result": {"frameTree": {"frame": {"url": "http://www.chromium.org/", "mimeType": "text/html", "loaderId": "7897.2", "id": "7897.1", "securityOrigin": "http://www.chromium.org"}, "resources": [{"url": "http://www.chromium.org/_/rsrc/1439160688000/system/app/css/camelot/allthemes-view.css", "mimeType": "text/css", "type": "Stylesheet"}, {"url": "http://www.gstatic.com/sites/p/ae80a1/system/app/themes/beigeandblue/standard-css-beigeandblue-ltr-ltr.css", "mimeType": "text/css", "type": "Stylesheet"}, {"url": "http://www.chromium.org/_/rsrc/1438811752264/chromium-projects/logo_chrome_color_1x_web_32dp.png", "mimeType": "image/png", "type": "Image"}, {"url": "http://www.chromium.org/_/rsrc/1439160688000/system/app/css/overlay.css?cb=beigeandblueundefineda100%25%25150goog-ws-leftthemedefaultstandard", "mimeType": "text/css", "type": "Stylesheet"}, {"url": "http://www.gstatic.com/sites/p/ae80a1/system/js/jot_min_view__en.js", "mimeType": "text/javascript", "type": "Script"}, {"url": "http://www.chromium.org/_/rsrc/1438879449147/config/customLogo.gif?revision=3", "mimeType": "image/png", "type": "Image"}]}}}