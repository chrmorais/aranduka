import QtQuick 1.0

ListView {
    id: bookstorecontents
    property variant contr
    property variant leftside
    property variant next
    width: parent.width
    anchors.top: bookstores.top
    anchors.bottom: bookstores.bottom
    delegate: Component {
        Rectangle {
            height: 60
            width: bookstores.width
            color: "#00000000"
            Rectangle {
                width: parent.width -10
                height: 50
                radius: 5
                y: 5
                x: 5
                color: ListView.isCurrentItem ? "steelblue" : ((index % 2 == 0)?"#222":"#111")
                clip: true
                Image {
                    id: cover
                    fillMode: Image.PreserveAspectFit
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
                    anchors.right: parent.right
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
                    anchors.right: parent.right
                    anchors.leftMargin: 10
                    verticalAlignment: Text.AlignTop
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        console.log("clicked");
                        controller.openStoreURL(model.item.url)
                    }
                }
            }
        }
    }
}
