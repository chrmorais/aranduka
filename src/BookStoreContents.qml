import QtQuick 1.0

ListView {
    property variant contr
    delegate: Component {
        Rectangle {
            width: contents.width
            height: 60
            color: ((index % 2 == 0)?"#222":"#111")
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
                anchors.right: count.left
                anchors.leftMargin: 10
                verticalAlignment: Text.AlignTop
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {bookstorecontents.contr.openStoreURL(model.item.url)}
            }
        }
    }
}
