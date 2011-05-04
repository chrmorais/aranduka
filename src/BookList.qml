import QtQuick 1.0

ListView {
    id: bookListView
    property variant contr
    width: parent.width
    height: parent.height
    focus: true
    highlightFollowsCurrentItem: true
    
    delegate: Component {
        Rectangle {
            height: 60
            width: bookListView.width
            color: "#00000000"
            Rectangle {
                width: bookListView.width-10
                height: 50
                radius: 5
                y: 5
                x: 5
                color: ListView.isCurrentItem ? "steelblue" : ((index % 2 == 0)?"#222":"#111")
                clip: true
                Image {
                    id: cover
                    source: model.book.cover
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
                    text: model.book.title
                    color: "white"
                    font.bold: true
                    anchors.top: parent.top
                    anchors.left: cover.right
                    anchors.right: parent.right
                    anchors.margins: 5
                    verticalAlignment: Text.AlignBottom
                }
                Text {
                    id: subtitle
                    elide: Text.ElideRight
                    color: "#eee"
                    text: model.book.author || "Unknown Author"
                    font.pointSize: 10
                    anchors.top: title.bottom
                    anchors.left: cover.right
                    anchors.right: parent.right
                    anchors.margins: 5
                    verticalAlignment: Text.AlignTop
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        contr.bookSelected(model.book)
                        bookListView.currentIndex=index
                    }
                }
            }
        }
    }
    states: [
        State {
            name: "Shown"
            PropertyChanges {
                target: bookListView
                opacity: 1
            }
        },
        State {
            name: "Hidden"
            PropertyChanges {
                target: bookListView
                opacity: 0.001
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
        
