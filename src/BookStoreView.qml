import QtQuick 1.0

Rectangle {
    property alias model: bookstores.model
    property alias contentsmodel: bookstorecontents.model
    property alias contr: bookstores.contr
    clip: true
    color: "#00000000"
    ListView {
        id: bookstores
        property variant contr
        width: parent.width
        height: parent.height
        x: 0
        delegate: Component {
            Rectangle {
                height: 60
                width: bookstores.width
                color: "#00000000"
                Rectangle {
                    width: bookstores.width -10
                    height: 50
                    radius: 5
                    y: 5
                    x: 5
                    color: ListView.isCurrentItem ? "steelblue" : ((index % 2 == 0)?"#222":"#111")
                    clip: true
                    Text {
                        color: "white"
                        id: title
                        elide: Text.ElideRight
                        text: model.store.name
                        height: 16
                        anchors.fill: parent
                        anchors.margins: 10
                        verticalAlignment: Text.AlignBottom
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: { bookstores.contr.openStore(model.store)
                        bookstores.currentIndex=index
                        }
                    }
                }
            }
        }
   }
    ListView {
        id: bookstorecontents
        property variant contr
        width: parent.width
        anchors.left: bookstores.right
        anchors.top: bookstores.top
        anchors.bottom: bookstores.bottom
        delegate: Component {
            Rectangle {
                height: 60
                width: bookstores.width                
                color: "#00000000"
                Rectangle {
                    width: contents.width -10
                    height: 50
                    radius: 5
                    y: 5
                    x: 5
                    color: ListView.isCurrentItem ? "steelblue" : ((index % 2 == 0)?"#222":"#111")
                    clip: true
                    Image {
                        id: cover
                        source: model.item.icon
                        sourceSize {
                            width: height
                            height: height
                        }
                        width: 50
                        height: 50
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.leftMargin: (parent.height - width)/2
                        anchors.topMargin: (parent.height - height)/2
                    }
                    Text {
                        id: title
                        elide: Text.ElideRight
                        text: model.item.title
                        color: "white"
                        font.bold: true
                        anchors.top: parent.top
                        anchors.left: cover.right
                        anchors.bottom: parent.verticalCenter
                        anchors.leftMargin: 10
                        verticalAlignment: Text.AlignBottom
                    }
                    Text {
                        id: subtitle
                        elide: Text.ElideRight
                        color: "#aaa"
                        text: model.item.subtitle || ""
                        font.pointSize: 10
                        anchors.top: title.bottom
                        anchors.left: cover.right
                        anchors.leftMargin: 10
                        verticalAlignment: Text.AlignTop
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {bookstores.contr.openStoreURL(model.item.url)}
                    }
                }
            }
        }
    }
    states: [
        State {
            name: "StoreList"
            PropertyChanges {
                target: bookstores
                x: 0
            }
        },
        State {
            name: "StoreContents"
            PropertyChanges {
                target: bookstores
                x: -1 * bookstores.width
            }
        }
    ]
    transitions: [
        Transition {
            PropertyAnimation {
                properties: "x,opacity"
                duration: 300
            }
        }
    ]
}