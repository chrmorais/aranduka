import QtQuick 1.0

ListView {
    property variant contr
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
