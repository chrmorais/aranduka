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

//     Rectangle {
//         id: actions
//         height: 65
//         width: parent.width / 3
//         y: 5
//         z: 100
//         Row {
//             Button {
//                 text: "Books"
//                 width: 80
//                 height: 60
//                 z: 101
//                 onClicked: { main.state="Books"; actions.state="Hidden"}
//             }
//             Button {
//                 text: "Bookstores"
//                 width: 80
//                 height: 60
//                 z: 101
//                 onClicked: { main.state="Bookstores"; actions.state="Hidden"}
//             }
//             Button {
//                 text: "Bookstore2"
//                 width: 80
//                 height: 60
//                 z: 101
//                 onClicked: { main.state="Bookstore2"; actions.state="Hidden"}
//             }
//             Button {
//                 text: "Contents"
//                 width: 80
//                 height: 60
//                 z: 101
//                 onClicked: { main.state="Contents"; actions.state="Hidden"}
//             }
//             Button {
//                 text: "Read"
//                 width: 80
//                 height: 60
//                 z: 101
//                 onClicked: { main.state="Text"; actions.state="Hidden"}
//             }
//         }
//         states: [
//             State {
//                 name: "Shown"
//                 PropertyChanges {
//                     target: actions
//                     y: 0
//                 }
//             },
//             State {
//                 name: "Hidden"
//                 PropertyChanges {
//                     target: actions
//                     y: -60
//                 }
//             }
//         ]
//         transitions: [
//             Transition {
//                 PropertyAnimation {
//                     properties: "y,opacity"
//                     duration: 300
//                 }
//             }
//         ]
//         MouseArea {
//             anchors.fill: parent
//             hoverEnabled: true
//             onEntered: { parent.state="Shown" }
//             onExited: { parent.state="Hidden" }
//             acceptedButtons: Qt.NoButton
//         }
//     }

    BookList {
        id: booklist
        model: bookList
        contr: controller
        anchors.right: webview.left
        anchors.left: parent.left
        anchors.top: parent.top
        height: parent.height
        opacity: 0.001
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
        opacity: 0.001
        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: { parent.state="Shown" }
            onExited: { parent.state="Hidden" }
            acceptedButtons: Qt.NoButton
        }
    }

    BookStoreView {
        id: bookstores
        model: bookStoreList
        contr: controller
        width: 800
        height: parent.height-40
        x: (main.width-800) / 2
        y:20
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

    states: [
    State {
        name: "Books"
        PropertyChanges {
            target: booklist
        }
    },
    State {
        name: "Bookstores"
        PropertyChanges {
            target: booklist
        }
    },
    State {
        name: "Bookstore2"
        PropertyChanges {
            target: booklist
        }
    },
    State {
        name: "Bookstore3"
        PropertyChanges {
            target: booklist
        }
    },
    State {
        name: "Contents"
        PropertyChanges {
            target: booklist
        }
    },
    State {
        name: "Text"
        PropertyChanges {
            target: booklist
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

