let EVENT_WIDTH = 125
const groupId = JSON.parse(document.getElementById('groupId').textContent)
const combinations = JSON.parse(document.getElementById('combinations').textContent)
const caseIds = JSON.parse(document.getElementById('caseIds').textContent)
let textWidths = {}
axios.get('/partial-order/colors')
    .then((response) => {
            let colorMap = new Map(Object.entries(response.data['colors']))
            textWidths = JSON.parse(response.data['textWidths'])
            let longestActivityWidth = textWidths[response.data['longestActivityName']]

            if (longestActivityWidth + 20 > EVENT_WIDTH) {
                EVENT_WIDTH = longestActivityWidth + 20
            }

            for (let i = 0; i < combinations.length; i++) {
                drawTotalOrders(i, combinations[i]['events'], colorMap)
            }

            $('#spinner').hide()
            $('.partial-order-groups').removeAttr('hidden')
        }
    );

function drawTotalOrders(combinationsNumber, events, colorMap) {
    let height = EVENT_HEIGHT
    let width = events.length * EVENT_WIDTH + (events.length - 1) * GAP + EVENT_DIAMETER + STROKE_SPACE
    let svg = d3.selectAll(`#combination-${combinationsNumber}`).append("svg").attr("width", width).attr("height", height)

    $(`#combination-${combinationsNumber}`).click(function () {
        redirectPost('/partial-order/delays', {
            'groupId': JSON.stringify(groupId),
            'combination': JSON.stringify(events),
            'caseIds': JSON.stringify(caseIds)
        })
    })

    for (let i = 0; i < events.length; i++) {
        let activityName = events[i][ACTIVITY_KEY]
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
            .attr('class', 'event')
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