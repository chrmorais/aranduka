import QtQuick 1.0
import QtWebKit 1.0
import "components" 

Rectangle {
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
    
    function setBookStoreModel(model) {
        bookstorecontents.model = model
    }

    function setContents(mod) {
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
        anchors.rightMargin: 15
        anchors.leftMargin: 5
        anchors.bottomMargin: 5
        height: 60
        spacing: 5
        state: "Books"
        
        Button {
            height: 60
            width: parent.width / 3
            id: booksbutton
            text: "Books"
            onClicked: parent.state = "Books"
        }
        Button {
            height: 60
            width: parent.width / 3
            id: storesbutton
            text: "Stores"
            onClicked: parent.state = "Stores"
        }
        Button {
            height: 60
            width: parent.width / 3
            id: infobutton
            text: "Info"
            onClicked: parent.state = "Info"
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
                    target: infobutton
                    opacity: .4 }
                PropertyChanges {
                    target: booklist
                    opacity: 1 }
                PropertyChanges {
                    target: bookstores
                    opacity: 0 }
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
                    target: infobutton
                    opacity: .4 }
                PropertyChanges {
                    target: booklist
                    opacity: 0 }
                PropertyChanges {
                    target: bookstores
                    opacity: 1 }
            },
            State {
                name: "Info"
                PropertyChanges {
                    target: booksbutton
                    opacity: .4 }
                PropertyChanges {
                    target: storesbutton
                    opacity: .4 }
                PropertyChanges {
                    target: infobutton
                    opacity: .8 }
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
        state: "Shown"
        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: { parent.state="Shown" }
            onExited: { parent.state="Hidden" }
            acceptedButtons: Qt.NoButton
        }
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
        state: "Shown"
        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: { parent.state="Shown" }
            onExited: { parent.state="Hidden" }
            acceptedButtons: Qt.NoButton
        }
    }
    
    BookContents {
        id: contents
        contr: controller
        anchors.left: webview.right
        anchors.right: parent.right
        anchors.top: parent.top
        height: parent.height
        state: "Hidden"
        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: { parent.state="Shown" }
            onExited: { parent.state="Hidden" }
            acceptedButtons: Qt.NoButton
        }
    }


    BookStoreContents {
        id: bookstorecontents
        contr: controller
        width: 800
        height: parent.height-40
        x: (main.width-800) / 2
        y:20
    }


    FlickableWebView {
        id: storewebpage
        width: 860
        height: parent.height
        x: (main.width-860) / 2
        y:0
    }
    

    FlickableWebView {
        id: webview
        width: 860
        height: parent.height
        x: (main.width-860) / 2
        y:0
    }

}

