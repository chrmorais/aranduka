import QtQuick 1.0

Column {
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
/*    Rectangle {
        color: "green"
        radius: 5
        anchors.left: parent.left
        anchors.right: parent.right
        height: _subtitle.height + 20
        visible: _subtitle.text!=""? true: false
        Text {
            transformOrigin: Item.TopLeft
            id: _subtitle
            color: "white"
            text: ""
            x: 10
            y: (parent.height - height) / 2
            wrapMode: Text.Wrap
        }
    }*/
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
