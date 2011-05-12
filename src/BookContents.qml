import QtQuick 1.0

ListView {
    id: list
    property variant contr
    delegate: Component {
        Rectangle {
            height: 60
            width: contents.width
            color: "#00000000"
            Rectangle {
                width: contents.width-10
                radius: 5
                height: 50
                y: 5
                x: 5
                color: ListView.isCurrentItem ? "steelblue" : ((index % 2 == 0)?"#222":"#111")
                clip: true
                Text {
                    id: _title
                    text: model.entry.title
                    color: "white"
                    elide: Text.ElideRight
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: 5
                    height: 20
                    y: 10
                    x: 5
                    verticalAlignment: Text.AlignBottom
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                         contents.contr.gotoChapter(model.entry.fname)
                        contents.currentIndex=index
                    }
                }
            }
        }
    }
    transitions: [
        Transition {
            PropertyAnimation {
                properties: "y,opacity"
                duration: 300
            }
        }
    ]    
}
