let EVENT_WIDTH = 125
const groupId = JSON.parse(document.getElementById('groupId').textContent);
const combination = JSON.parse(document.getElementById('combination').textContent);
const caseIds = JSON.parse(document.getElementById('caseIds').textContent);
let textWidths = {}

let height = EVENT_HEIGHT * 2
let width = 0
let svg
axios.get('/partial-order/colors')
    .then((response) => {
            let colorMap = new Map(Object.entries(response.data['colors']))
            textWidths = JSON.parse(response.data['textWidths'])
            let longestActivityWidth = textWidths[response.data['longestActivityName']]
            if (longestActivityWidth + 20 > EVENT_WIDTH) {
                EVENT_WIDTH = longestActivityWidth + 20
            }
            width = combination.length * EVENT_WIDTH + (combination.length - 1) * GAP + EVENT_DIAMETER + STROKE_SPACE
            svg = d3.selectAll(`#combination`).append("svg").attr("width", width).attr("height", height)
            drawTotalOrder(combination, colorMap)
        }
    );

let saveButton = document.getElementById('save');

saveButton.onclick = function () {
    if (confirm("The order will be saved and added to the original log")) {
        axios.post('/partial-order/save-delay', {
            'groupId': JSON.stringify(groupId),
            'combination': JSON.stringify(combination),
            'caseIds': JSON.stringify(caseIds)
        })
        alert('The order was saved')
        location.href = 'groups'
    }
}

function drawTotalOrder(events, colorMap) {

    for (let i = 0; i < events.length; i++) {
        let activityName = events[i][ACTIVITY_KEY];
        let polygon
        if (i === 0) {
            // starting events do not have a corner on the left
            polygon = `${i * (EVENT_WIDTH + GAP)},0 ${(EVENT_WIDTH) + i * (EVENT_WIDTH + GAP)},0 ${EVENT_WIDTH + EVENT_DIAMETER + i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT / 2} ${EVENT_WIDTH + i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT} ${i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT}`
        } else {
            // standard event, not starting and finishing
            polygon = `${i * (EVENT_WIDTH + GAP)},0 ${(EVENT_WIDTH) + i * (EVENT_WIDTH + GAP)},0 ${EVENT_WIDTH + EVENT_DIAMETER + i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT / 2} ${EVENT_WIDTH + i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT} ${i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT} ${EVENT_DIAMETER + i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT / 2}`
        }
        svg.append('polygon')
            .attr('points', polygon)
            .attr('fill', colorMap.get(activityName))

        if (i === 0) {
            svg.append('text')
                .attr('x', i * (EVENT_WIDTH + GAP) + ((EVENT_WIDTH) / 2) - textWidths[activityName] / 2)
                .attr('y', 31)
                .text(activityName)
        } else {
            svg.append('text')
                .attr('x', i * (EVENT_WIDTH + GAP) + ((EVENT_WIDTH + EVENT_DIAMETER) / 2) - textWidths[activityName] / 2)
                .attr('y', 31)
                .text(activityName)
        }

    }
    visualizeDelay()
}

function visualizeDelay() {
    let i = 0, count = 1;
    while (combination[i][TIMESTAMP_KEY] !== combination[i + 1][TIMESTAMP_KEY])
        i++
    i += 1
    while (i < combination.length - 1) {
        let text = '+' + count + ' delta'
        if (combination[i][TIMESTAMP_KEY] !== combination[i + 1][TIMESTAMP_KEY]) {
            svg.append('text')
                .attr('x', i * (EVENT_WIDTH + GAP) + ((EVENT_WIDTH + EVENT_DIAMETER) / 2) - getTextWidth(text) / 2)
                .attr('y', 75)
                .attr('fill', '#28a745')
                .attr('font-weight', 'bolder')
                .text(text)
            i++
        } else {
            svg.append('text')
                .attr('x', i * (EVENT_WIDTH + GAP) + ((EVENT_WIDTH + EVENT_DIAMETER) / 2) - getTextWidth(text) / 2)
                .attr('y', 75)
                .attr('fill', '#28a745')
                .attr('font-weight', 'bolder')
                .text(text)

            count++
            i++
        }
    }
    svg.append('text')
        .attr('x', i * (EVENT_WIDTH + GAP) + ((EVENT_WIDTH + EVENT_DIAMETER) / 2) - getTextWidth('+' + count + ' delta') / 2)
        .attr('y', 75)
        .attr('fill', '#28a745')
        .attr('font-weight', 'bolder')
        .text('+' + count + ' delta')
}