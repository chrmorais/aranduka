import QtQuick 1.0

Rectangle {
    property alias model: bookstores.model
    property alias contr: bookstores.contr
    property variant currentPage
    property variant pages
    pages : [bsc1, bookdetails]
    
    function newModel () {
        bsc1.width = width
        bookstores.width = 0
        console.log(bookstores.width)
        main.currentpanel = bsc1
    }

    function setDetailsModel (model) {
        bookdetails.width = width
        bsc1.width = 0 
        bookdetails.title = "<b>"+(model.title || "No title")+"</b>"
        bookdetails.subtitle = model.subtitle || ""
        bookdetails.rights = model.rights || ""
        console.log(model.rights)
        main.currentpanel = bookdetails
    }

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
                    Image {
                        id: icon
                        // FIXME: If I enable this, the webview for book reading segfaults
                        // WTF? But really, WTF?
                        // source: model.store.icon
                        height: 40
                        width: 40
                        y: 5
                        x: 5
                    }
                    Text {
                        transformOrigin: Item.TopLeft
                        color: "white"
                        id: title
                        elide: Text.ElideRight
                        text: model.store.name
                        y: (parent.height - height) / 2
                        x: 5
                        anchors.right: parent.right
                        anchors.left: icon.right
                        anchors.margins: 5
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            bookstores.contr.openStore(model.store)
                            bookstores.currentIndex=index
                        }
                    }
                }
            }
        }
    }
    BookStoreContents {
        visible: true ? parent.currentpanel == bsc1: false
        id: bsc1
        leftside: bookstores
        anchors.left: leftside.right
        width: 0
        next: bookdetails
    }
    Column {
        visible: true ? parent.currentpanel == bookdetails: false
        id: bookdetails
        width: 0
        clip: true
        anchors.top: bookstores.top
        anchors.bottom: bookstores.bottom
        anchors.left: bsc1.right
        property alias title: _title.text
        property alias subtitle: _subtitle.text
        property alias rights: _rights.text
        spacing: 5
        Rectangle {
            color: "red"
            radius: 5
            anchors.left: parent.left
            anchors.right: parent.right
            height: _title.height + 20
            Text {
                transformOrigin: Item.TopLeft
                id: _title
                color: "white"
                text: "No text"
                x: 10
                y: (parent.height - height) / 2
                wrapMode: Text.Wrap
            }
        }
        Rectangle {
            color: "green"
            radius: 5
            anchors.left: parent.left
            anchors.right: parent.right
            height: _subtitle.height + 20
            visible: true ? _subtitle.text!="": false
            Text {
                transformOrigin: Item.TopLeft
                id: _subtitle
                color: "white"
                text: ""
                x: 10
                y: (parent.height - height) / 2
                wrapMode: Text.Wrap
            }
        }
        Rectangle {
            color: "blue"
            radius: 5
            anchors.left: parent.left
            anchors.right: parent.right
            height: _rights.height + 20
            visible: true
            clip: true
            Text {
                transformOrigin: Item.TopLeft
                id: _rights
                color: "white"
                text: ""
                x: 10
                y: (parent.height - height) / 2
                wrapMode: Text.WordWrap
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
