from .element import Element


class Document(object):
    implementation = None
    URL = None
    documentURI = None
    compatMode = None
    characterSet = None
    charset = None
    inputEncoding = None
    contentType = None
    doctype = None
    documentElement = None
    xmlEncoding = None
    xmlVersion = None
    xmlStandalone = None
    domain = None
    referrer = None
    cookie = None
    lastModified = None
    readyState = None
    title = None
    dir = None
    body = None
    head = None
    images = None
    embeds = None
    plugins = None
    links = None
    forms = None
    scripts = None
    currentScript = None
    defaultView = None
    designMode = None
    onreadystatechange = None
    anchors = None
    applets = None
    fgColor = None
    linkColor = None
    vlinkColor = None
    alinkColor = None
    bgColor = None
    all = None
    scrollingElement = None
    onpointerlockchange = None
    onpointerlockerror = None
    hidden = None
    visibilityState = None
    wasDiscarded = None
    webkitVisibilityState = None
    webkitHidden = None
    onbeforecopy = None
    onbeforecut = None
    onbeforepaste = None
    onfreeze = None
    onresume = None
    onsearch = None
    onsecuritypolicyviolation = None
    onvisibilitychange = None
    fonts = None
    oncopy = None
    oncut = None
    onpaste = None
    activeElement = None
    styleSheets = None
    pointerLockElement = None
    fullscreenElement = None
    adoptedStyleSheets = None
    onabort = None
    onblur = None
    oncancel = None
    oncanplay = None
    oncanplaythrough = None
    onchange = None
    onclick = None
    onclose = None
    oncontextmenu = None
    oncuechange = None
    ondblclick = None
    ondrag = None
    ondragend = None
    ondragenter = None
    ondragleave = None
    ondragover = None
    ondragstart = None
    ondrop = None
    ondurationchange = None
    onemptied = None
    onended = None
    onerror = None
    onfocus = None
    oninput = None
    oninvalid = None
    onkeydown = None
    onkeypress = None
    onkeyup = None
    onload = None
    onloadeddata = None
    onloadedmetadata = None
    onloadstart = None
    onmousedown = None
    onmouseenter = None
    onmouseleave = None
    onmousemove = None
    onmouseout = None
    onmouseover = None
    onmouseup = None
    onmousewheel = None
    onpause = None
    onplay = None
    onplaying = None
    onprogress = None
    onratechange = None
    onreset = None
    onresize = None
    onscroll = None
    onseeked = None
    onseeking = None
    onselect = None
    onstalled = None
    onsubmit = None
    onsuspend = None
    ontimeupdate = None
    ontoggle = None
    onvolumechange = None
    onwaiting = None
    onwheel = None
    onauxclick = None
    ongotpointercapture = None
    onlostpointercapture = None
    onpointerdown = None
    onpointermove = None
    onpointerup = None
    onpointercancel = None
    onpointerover = None
    onpointerout = None
    onpointerenter = None
    onpointerleave = None
    onselectstart = None
    onselectionchange = None
    onanimationend = None
    onanimationiteration = None
    onanimationstart = None
    ontransitionend = None
    children = None
    firstElementChild = None
    lastElementChild = None
    childElementCount = None
    fullscreenEnabled = None
    fullscreen = None
    onfullscreenchange = None
    onfullscreenerror = None
    webkitIsFullScreen = None
    webkitCurrentFullScreenElement = None
    webkitFullscreenEnabled = None
    webkitFullscreenElement = None
    onwebkitfullscreenchange = None
    onwebkitfullscreenerror = None
    rootElement = None
    featurePolicy = None
    onformdata = None
    onpointerrawupdate = None
    pictureInPictureElement = None
    pictureInPictureEnabled = None
    nodeType = None
    nodeName = None
    baseURI = None
    isConnected = None
    ownerDocument = None
    parentNode = None
    parentElement = None
    childNodes = None
    firstChild = None
    lastChild = None
    previousSibling = None
    nextSibling = None
    nodeValue = None
    textContent = None

    def getElementById(self, id):
        raise NotImplementedError

    def getElementsByTagName(self, name):
        raise NotImplementedError

    def getElementsByClassName(self, name):
        raise NotImplementedError

    def createElement(self, element):
        result = Element()
        result.tagName = element
        return result

    def removeChild(self, element):
        raise NotImplementedError

    def appendChild(self, element):
        raise NotImplementedError

    def replaceChild(self, new, old):
        raise NotImplementedError

    def write(self, text):
        raise NotImplementedError

    def querySelectorAll(self, query):
        raise NotImplementedError
