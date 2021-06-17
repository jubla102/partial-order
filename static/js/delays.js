let EVENT_WIDTH = 125
const combination = JSON.parse(document.getElementById('combination').textContent);
let textWidths = {}
axios.get('/partial-order/po-groups')

let height = EVENT_HEIGHT * 3
let width = combination.length * EVENT_WIDTH + (combination.length - 1) * GAP + EVENT_DIAMETER
let svg = d3.selectAll(`#combination`).append("svg").attr("width", width).attr("height", height)

axios.get('/partial-order/colors')
    .then((response) => {
            let colorMap = new Map(Object.entries(response.data['metadata']['colors']))
            textWidths = JSON.parse(response.data['metadata']['textWidths'])
            let longestActivityWidth = textWidths[response.data['metadata']['longestActivityName']]

            if (longestActivityWidth + 20 > EVENT_WIDTH) {
                EVENT_WIDTH = longestActivityWidth + 20
            }
            drawTotalOrder(combination, colorMap)
        }
    );

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
}

function visualize_delay() {
    console.log(combination)
    let i = 0, count = 1;
    while (combination[i][TIME_KEY] !== combination[i + 1][TIME_KEY])
        i++
    i += 1
    while (i < combination.length - 1) {
        console.log(i, count)
        if (combination[i][TIME_KEY] !== combination[i + 1][TIME_KEY]) {
            svg.append('text')
                .attr('x', 30 + i * (EVENT_WIDTH + GAP))
                .attr('y', 75)
                .attr('fill', 'rgba(92, 184, 92, 1)')
                .text('+' + count + ' delta')
            i++
        } else {
            svg.append('text')
                .attr('x', 30 + i * (EVENT_WIDTH + GAP))
                .attr('y', 75)
                .attr('fill', 'rgba(92, 184, 92, 1)')
                .text('+' + count + ' delta')

            count++
            i++
        }
    }
    svg.append('text')
        .attr('x', 30 + i * (EVENT_WIDTH + GAP))
        .attr('y', 75)
        .attr('fill', 'rgba(92, 184, 92, 1)')
        .text('+' + count + ' delta')
}