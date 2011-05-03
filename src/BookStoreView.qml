import QtQuick 1.0

ListView {
    id: bookstores
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
                text: model.store.name
                height: 20
                y: 10
                verticalAlignment: Text.AlignBottom
            }
            MouseArea {
                anchors.fill: parent
                onClicked: { bookstores.contr.openStore(model.store)}
            }
        }
    }
}
