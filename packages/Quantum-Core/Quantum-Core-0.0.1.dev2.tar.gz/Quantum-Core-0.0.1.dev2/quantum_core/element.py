class Element(object):
    namespaceURI = None
    prefix = None
    localName = None
    tagName = None
    id = None
    className = None
    classList = None
    slot = None
    part = None
    attributes = None
    shadowRoot = None
    assignedSlot = None
    innerHTML = None
    innerText = None
    outerHTML = None
    scrollTop = None
    scrollLeft = None
    scrollWidth = None
    scrollHeight = None
    clientTop = None
    clientLeft = None
    clientWidth = None
    clientHeight = None
    attributeStyleMap = None
    onbeforecopy = None
    onbeforecut = None
    onbeforepaste = None
    onsearch = None
    elementTiming = None
    previousElementSibling = None
    nextElementSibling = None
    children = None
    firstElementChild = None
    lastElementChild = None
    childElementCount = None
    onfullscreenchange = None
    onfullscreenerror = None
    onwebkitfullscreenchange = None
    onwebkitfullscreenerror = None
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

    def setPointerCapture(self):
        raise NotImplementedError

    def releasePointerCapture(self):
        raise NotImplementedError

    def hasPointerCapture(self):
        raise NotImplementedError

    def hasAttributes(self):
        raise NotImplementedError

    def getAttributeNames(self):
        raise NotImplementedError

    def getAttribute(self):
        raise NotImplementedError

    def getAttributeNS(self):
        raise NotImplementedError

    def setAttribute(self):
        raise NotImplementedError

    def setAttributeNS(self):
        raise NotImplementedError

    def removeAttribute(self):
        raise NotImplementedError

    def removeAttributeNS(self):
        raise NotImplementedError

    def hasAttribute(self):
        raise NotImplementedError

    def hasAttributeNS(self):
        raise NotImplementedError

    def toggleAttribute(self):
        raise NotImplementedError

    def getAttributeNode(self):
        raise NotImplementedError

    def getAttributeNodeNS(self):
        raise NotImplementedError

    def setAttributeNode(self):
        raise NotImplementedError

    def setAttributeNodeNS(self):
        raise NotImplementedError

    def removeAttributeNode(self):
        raise NotImplementedError

    def closest(self):
        raise NotImplementedError

    def matches(self):
        raise NotImplementedError

    def webkitMatchesSelector(self):
        raise NotImplementedError

    def attachShadow(self):
        raise NotImplementedError

    def getElementsByTagName(self):
        raise NotImplementedError

    def getElementsByTagNameNS(self):
        raise NotImplementedError

    def getElementsByClassName(self):
        raise NotImplementedError

    def insertAdjacentElement(self):
        raise NotImplementedError

    def insertAdjacentText(self):
        raise NotImplementedError

    def insertAdjacentHTML(self):
        raise NotImplementedError

    def requestPointerLock(self):
        raise NotImplementedError

    def getClientRects(self):
        raise NotImplementedError

    def getBoundingClientRect(self):
        raise NotImplementedError

    def scrollIntoView(self):
        raise NotImplementedError

    def scroll(self):
        raise NotImplementedError

    def scrollTo(self):
        raise NotImplementedError

    def scrollBy(self):
        raise NotImplementedError

    def scrollIntoViewIfNeeded(self):
        raise NotImplementedError

    def animate(self):
        raise NotImplementedError

    def computedStyleMap(self):
        raise NotImplementedError

    def before(self):
        raise NotImplementedError

    def after(self):
        raise NotImplementedError

    def replaceWith(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

    def prepend(self):
        raise NotImplementedError

    def append(self):
        raise NotImplementedError

    def querySelector(self):
        raise NotImplementedError

    def querySelectorAll(self):
        raise NotImplementedError

    def requestFullscreen(self):
        raise NotImplementedError

    def webkitRequestFullScreen(self):
        raise NotImplementedError

    def webkitRequestFullscreen(self):
        raise NotImplementedError

    def createShadowRoot(self):
        raise NotImplementedError

    def getDestinationInsertionPoints(self):
        raise NotImplementedError
