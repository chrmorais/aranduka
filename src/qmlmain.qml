import QtQuick 1.0
import QtWebKit 1.0
import "components" 

Rectangle {
    property variant currentpanel
    id: main
    width: 400
    height: 400
    opacity: 1
    state: "Books"

    function setURL(url) {
        webview.url = url
    }
    function setHTML(ht) {
        webview.html = ht
    }
    
    function setBookStoreModel() {
        bookstores.newModel ()
    }
    
    function setBookDetailsModel(model) {
        bookstores.setDetailsModel (model)
    }

    function setContents(mod) {
        console.log(mod)
        contents.model = mod
    }

    function setBookStorePage(url) {
        bookstorepage.url = url
    }

    Image {
        source: "icons/118222-Just_Green_Curls.svgz"
    }

    Row {
        id: leftmodes
        anchors.left: main.left
        anchors.right: webview.left
        anchors.bottom: main.bottom
        anchors.rightMargin: 5
        anchors.leftMargin: 5
        anchors.bottomMargin: 5
        height: 60
        spacing: 5
        state: "Books"
        
        Button {
            height: 60
            width: parent.width / 2
            id: booksbutton
            text: "Books"
            onClicked: parent.state = "Books"
        }
        Button {
            height: 60
            width: parent.width / 2
            id: storesbutton
            text: "Stores"
            onClicked: parent.state = "Stores"
        }
        states: [
            State {
                name: "Books"
                PropertyChanges {
                    target: booksbutton
                    opacity: .8 }
                PropertyChanges {
                    target: storesbutton
                    opacity: .4 }
                PropertyChanges {
                    target: booklist
                    z: 10
                    visible: true }
                PropertyChanges {
                    target: bookstores
                    z: 0
                    visible: false }
                PropertyChanges {
                    target: main
                    currentpanel: booklist
                }
            },
            State {
                name: "Stores"
                PropertyChanges {
                    target: booksbutton 
                    opacity: .4 }
                PropertyChanges {
                    target: storesbutton 
                    opacity: .8 }
                PropertyChanges {
                    target: booklist
                    z: 0
                    visible: false }
                PropertyChanges {
                    target: bookstores
                    z: 10
                    visible: true }
                PropertyChanges {
                    target: main
                    currentpanel: bookstores
                }
            }
        ]
        transitions: [
            Transition {
                PropertyAnimation {
                    properties: "x,y,opacity"
                    duration: 500
                }
            }
        ]
    }

    Row {
        id: rightmodes
        anchors.left: webview.right
        anchors.right: main.right
        anchors.bottom: main.bottom
        anchors.rightMargin: 5
        anchors.leftMargin: 5
        anchors.bottomMargin: 5
        height: 60
        spacing: 5
        state: "Contents"
        
        Button {
            height: 60
            width: parent.width / 2
            id: contentsbutton
            text: "Contents"
            onClicked: parent.state = "Contents"
        }
        Button {
            height: 60
            width: parent.width / 2
            id: infobutton
            text: "Info"
            onClicked: parent.state = "Info"
        }
        states: [
            State {
                name: "Contents"
                PropertyChanges {
                    target: contentsbutton
                    opacity: .8 }
                PropertyChanges {
                    target: infobutton
                    opacity: .4 }
                PropertyChanges {
                    target: contents
                    z: 10
                    visible: true }
/*                PropertyChanges {
                    target: infowidget
                    z: 0
                    visible: false }*/
/*                PropertyChanges {
                    target: main
                    currentpanel2: contentsbutton
                }*/
            },
            State {
                name: "Info"
                PropertyChanges {
                    target: contentsbutton 
                    opacity: .4 }
                PropertyChanges {
                    target: infobutton 
                    opacity: .8 }
                PropertyChanges {
                    target: contents
                    z: 0
                    visible: false }
/*                PropertyChanges {
                    target: infowidget
                    z: 10
                    visible: true }*/
/*                PropertyChanges {
                    target: main
                    currentpanel2: contents
                }*/
            }
        ]
        transitions: [
            Transition {
                PropertyAnimation {
                    properties: "x,y,opacity"
                    duration: 500
                }
            }
        ]
    }


    BookList {
        height: parent.height
        anchors.right: webview.left
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: leftmodes.top
        id: booklist
        model: bookList
        contr: controller
    }

    BookStoreView {
        height: parent.height
        anchors.right: webview.left
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: leftmodes.top
        id: bookstores
        model: bookStoreList
        contr: controller
    }
    BookStoreContents {
        height: parent.height
        anchors.right: webview.left
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: leftmodes.top
        id: bookstorecontents
        model: storeContents
    }
    
    BookContents {
        id: contents
        contr: controller
        anchors.left: webview.right
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: rightmodes.top
        model: bookContents
        clip: true
    }


    FlickableWebView {
        id: webview
        width: 860
        height: parent.height
        x: (main.width-860) / 2
        y:0
        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: main.state="Focused"
            onExited: {console.log("Leaving webview"); main.state="Busy"; }
            acceptedButtons: Qt.NoButton
        }
    }
    states: [
        State {
            name: "Focused"
            PropertyChanges {
                target: leftmodes
                opacity: .1 }
            PropertyChanges {
                target: rightmodes
                opacity: .1 }
            PropertyChanges {
                target: main.currentpanel
                opacity: .1 }
            PropertyChanges {
                target: contents
                opacity: .1 }
            PropertyChanges {
                target: webview
                opacity: 1 }
        },
        State {
            name: "Busy"
            PropertyChanges {
                target: leftmodes
                opacity: 1 }
            PropertyChanges {
                target: rightmodes
                opacity: 1 }
            PropertyChanges {
                target: main.currentpanel
                opacity: 1 }
            PropertyChanges {
                target: contents
                opacity: 1 }
            PropertyChanges {
                target: webview
                opacity: 1 }
        }
    ]
    transitions: [
        Transition {
            PropertyAnimation {
                properties: "x,y,opacity"
                duration: 500
            }
        }
    ]
}

