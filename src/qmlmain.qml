import QtQuick 1.0
import QtWebKit 1.0


Rectangle {
    id: rectangle1
    width: 400
    height: 400
    opacity: 1
    state: "Books"

    function setHTML(html) {
        webview.html = html
    }

    function setContents(mod) {
        contents.model = mod
    }

        BookList {
            id: booklist
            model: bookList
            contr: controller
            x: 0
            height: parent.height
            width: parent.width
        }
        ListView {
            objectName: "contents"
            id: contents
            width: parent.width
            property variant contr
            contr: controller
            anchors.left: booklist.right
            height: parent.height
            delegate: Component {
                Rectangle {
                    width: contents.width
                    height: 20
                    Text {
                        id: title
                        elide: Text.ElideRight
                        text: model.title
                        anchors.leftMargin: 10
                        verticalAlignment: Text.AlignBottom
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: { contents.contr.gotoChapter(model.fname) }
                    }
                }
            }
        WebView {
            objectName: "webview"
            id: webview
            settings.javascriptEnabled: true
            width: parent.width
            height: parent.height
            anchors.left: contents.right
        }
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

