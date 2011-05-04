import QtQuick 1.0

ListView {
    id: bookstores
    property variant contr
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
    states: [
        State {
            name: "Shown"
            PropertyChanges {
                target: bookstores
                opacity: 1
            }
        },
        State {
            name: "Hidden"
            PropertyChanges {
                target: bookstores
                opacity: 0.1
            }
        }
    ]
    transitions: [
        Transition {
            PropertyAnimation {
                properties: "y,opacity"
                duration: 300
            }
        }
    ]    
}
