import QtQuick 1.0

Rectangle {
    property alias model: bookstores.model
    property alias contr: bookstores.contr
    property variant currentPage
    property variant pages
    
    function setDetailsModel (model) {
        bookdetails.title = "<b>"+(model.title || "No title")+"</b>"
        bookdetails.subtitle = model.subtitle || ""
        bookdetails.rights = model.rights || ""
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
                            console.log("clicked on the store list")
                            controller.openStore(model.store)
                            bookstores.currentIndex=index
                        }
                    }
                }
            }
        }
    }
}
