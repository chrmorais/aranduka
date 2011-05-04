import QtQuick 1.0

Rectangle {
    property alias model: bookstores.model
    property alias contr: bookstores.contr
    property variant currentPage
    property variant pages
    currentPage: 0
    pages : [bsc1, bsc2, bsc3, bsc4, bsc5, bsc6, bsc7, bookdetails]
    
    function newModel (model) {
        pages[currentPage].model = model
        pages[currentPage].width = width
        currentPage = currentPage +1
        bookstores.x = -1 * currentPage * width
    }

    function setDetailsModel (model) {
//         console.log(model)
        bookdetails.width= width
        bookdetails.text= model.title
        bookstores.x = -1 * (currentPage+1) * width
        currentPage = 7
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
        id: bsc1
        leftside: bookstores
        anchors.left: leftside.right
        width: 0
        next: bsc2
    }
    BookStoreContents {
        id: bsc2
        leftside: bsc1
        anchors.left: leftside.right
        width: 0
        next: bsc3
    }
    BookStoreContents {
        id: bsc3
        leftside: bsc2
        anchors.left: leftside.right
        width: 0
        next: bsc4
    }
    BookStoreContents {
        id: bsc4
        leftside: bsc3
        anchors.left: leftside.right
        width: 0
        next: bsc5
    }
    BookStoreContents {
        id: bsc5
        leftside: bsc4
        anchors.left: leftside.right
        width: 0
        next: bsc6
}
    BookStoreContents {
        id: bsc6
        leftside: bsc5
        anchors.left: leftside.right
        width: 0
        next: bsc7
    }
    BookStoreContents {
        id: bsc7
        leftside: bsc6
        width: 0
        anchors.left: leftside.right
        next: bookdetails
    }
    Rectangle {
        property alias text: details.text
        width: 0
        clip: true
        anchors.top: bookstores.top
        anchors.bottom: bookstores.bottom
        anchors.left: bsc7.right
        color: "red"
        radius: 5
        id: bookdetails
        Text {
            anchors.fill: parent
            id: details
            color: "white"
            text: "No text"
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
