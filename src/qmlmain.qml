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
        console.log(url)
        webview.url = url
    }

    function setContents(mod) {
        contents.model = mod
    }

    Rectangle {
        id: actions
        height: 65
        width: parent.width
        y: -60
        z: 100
        Row {
            Button {
                text: "Books"
                width: 80
                height: 60
                z: 101
                onClicked: { main.state="Books"}
            }
            Button {
                text: "Contents"
                width: 80
                height: 60
                z: 101
                onClicked: { main.state="Contents"}
            }
            Button {
                text: "Read"
                width: 80
                height: 60
                z: 101
                onClicked: { main.state="Text"}
            }
        }
        states: [
            State {
                name: "Shown"
                PropertyChanges {
                    target: actions
                    y: 0
                }
            },
            State {
                name: "Hidden"
                PropertyChanges {
                    target: actions
                    y: -60
                }
            }
        ]
        transitions: [
            Transition {
                PropertyAnimation {
                    properties: "y,opacity"
                    duration: 300
                }
            }
        ]
        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: { parent.state="Shown" }
            onExited: { parent.state="Hidden" }
            acceptedButtons: Qt.NoButton
        }
    }

    BookList {
        id: booklist
        model: bookList
        contr: controller
        x: 0
        height: parent.height-5
        width: parent.width
        y:5
    }

    
    
    ListView {
        objectName: "contents"
        id: contents
        width: parent.width
        property variant contr
        contr: controller
        anchors.left: booklist.right
        height: parent.height-5
        y:5
        delegate: Component {
            Rectangle {
                width: contents.width
                height: 40
                color: ((index % 2 == 0)?"#222":"#111")
                Text {
                    color: "white"
                    id: title
                    elide: Text.ElideRight
                    text: model.title
                    height: 20
                    y: 10
                    verticalAlignment: Text.AlignBottom
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: { contents.contr.gotoChapter(model.fname) }
                }
            }
        }
    }

    FlickableWebView {
        id: webview
        anchors.left: contents.right
        height: parent.height-5      
        y:5
    }
   
    states: [
    State {
        name: "Books"
        PropertyChanges {
            target: booklist
            x: 0
        }
    },
    State {
        name: "Contents"
        PropertyChanges {
            target: booklist
            x: -1 * parent.width
        }
    },
    State {
        name: "Text"
        PropertyChanges {
            target: booklist
            x: -2 * parent.width
        }
    }
    ]
    transitions: [
        Transition {
            PropertyAnimation {
                properties: "x,opacity"
                duration: 500
            }
        }
    ]
}

