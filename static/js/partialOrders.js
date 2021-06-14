const EVENT_WIDTH = 125
const EVENT_HEIGHT = 50
const GAP = 10
const EVENT_DIAMETER = 25
const EVENTS_KEY = 'events'
const ACTIVITY_KEY = 'concept:name'
const TIMESTAMP_KEY = 'time:timestamp'

axios.get('/partial-order/po-groups')
    .then((response) => {
            let colorMap = new Map(Object.entries(response.data['colors']))
            let partialOrderGroups = response.data['groups']

            let groupKeys = Object.keys(partialOrderGroups)
            for (let i = 0; i < groupKeys.length; i++) {
                drawPartialOrders(i, partialOrderGroups[groupKeys[i]][EVENTS_KEY], colorMap)
            }
        }
    );

function drawPartialOrders(groupNumber, events, colorMap) {
    let partialOrders = []
    let maxParallelEvents = 1
    for (let i = 0; i < events.length;) {
        let parallelEvents = [events[i]]
        let j = 1
        for (; i + j < events.length; j++) {
            if (events[i][TIMESTAMP_KEY] === events[i + j][TIMESTAMP_KEY]) {
                parallelEvents.push(events[i + j])
            } else {
                break
            }
        }
        if (parallelEvents.length > maxParallelEvents) {
            maxParallelEvents = parallelEvents.length
        }
        partialOrders.push(parallelEvents)
        i = i + j
    }

    let height = maxParallelEvents * EVENT_HEIGHT + (maxParallelEvents - 1) * GAP
    let width = partialOrders.length * EVENT_WIDTH + (partialOrders.length - 1) * GAP * 2 + EVENT_DIAMETER
    console.log(partialOrders.length)
    let svg = d3.selectAll(`#partial-order-${groupNumber}`).append("svg").attr("width", width).attr("height", height)
    $(`#partial-order-${groupNumber}`).click(function () {
        redirectPost("/partial-order/combinations", {
            "partialOrder": JSON.stringify(events)
        })
    })
    drawPartialOrder(svg, partialOrders, maxParallelEvents, colorMap)
}

function drawPartialOrder(svg, eventList, maxParallelEvents, colorMap) {
    let baseY
    if (maxParallelEvents % 2 === 0) {
        baseY = (maxParallelEvents / 2 - 0.5) * (EVENT_HEIGHT + GAP)
    } else {
        baseY = Math.floor(maxParallelEvents / 2) * (EVENT_HEIGHT + GAP)
    }

    let xOffset = 0
    for (let i = 0; i < eventList.length; i++) {
        if ((i !== 0 && eventList[i].length % 2 === 0 && (eventList[i - 1].length % 2 !== 0)) ||
            (i !== 0 && eventList[i].length % 2 !== 0 && (eventList[i - 1].length % 2 === 0))
        ) {
            xOffset = xOffset + GAP * 2
        }
        for (let j = 0; j < eventList[i].length; j++) {
            let yOffset
            if (eventList[i].length % 2 === 0) {
                yOffset = (eventList[i].length / 2 - 0.5) - j
            } else {
                yOffset = Math.floor(eventList[i].length / 2) - j
            }

            let polygon
            if (i === 0) {
                // starting events do not have a corner on the left
                polygon = `${xOffset + i * (EVENT_WIDTH + GAP)},${baseY - (yOffset * (EVENT_HEIGHT + GAP))} ${(xOffset + EVENT_WIDTH) + i * (EVENT_WIDTH + GAP)},${baseY - (yOffset * (EVENT_HEIGHT + GAP))} ${xOffset + EVENT_WIDTH + EVENT_DIAMETER + i * (EVENT_WIDTH + GAP)},${(baseY - (yOffset * (EVENT_HEIGHT + GAP))) + EVENT_DIAMETER} ${xOffset + EVENT_WIDTH + i * (EVENT_WIDTH + GAP)},${(baseY - (yOffset * (EVENT_HEIGHT + GAP))) + EVENT_HEIGHT} ${xOffset + i * (EVENT_WIDTH + GAP)},${(baseY - (yOffset * (EVENT_HEIGHT + GAP))) + EVENT_HEIGHT}`
            } else {
                // standard event, not starting and finishing
                polygon = `${xOffset + i * (EVENT_WIDTH + GAP)},${baseY - (yOffset * (EVENT_HEIGHT + GAP))} ${(xOffset + EVENT_WIDTH) + i * (EVENT_WIDTH + GAP)},${baseY - (yOffset * (EVENT_HEIGHT + GAP))} ${xOffset + EVENT_WIDTH + EVENT_DIAMETER + i * (EVENT_WIDTH + GAP)},${(baseY - (yOffset * (EVENT_HEIGHT + GAP))) + EVENT_DIAMETER} ${xOffset + EVENT_WIDTH + i * (EVENT_WIDTH + GAP)},${(baseY - (yOffset * (EVENT_HEIGHT + GAP))) + EVENT_HEIGHT} ${xOffset + i * (EVENT_WIDTH + GAP)},${(baseY - (yOffset * (EVENT_HEIGHT + GAP))) + EVENT_HEIGHT} ${xOffset + EVENT_DIAMETER + i * (EVENT_WIDTH + GAP)},${(baseY - (yOffset * (EVENT_HEIGHT + GAP))) + EVENT_DIAMETER}`
            }
            svg.append('polygon')
                .attr('points', polygon)
                .attr('fill', colorMap.get(eventList[i][j][ACTIVITY_KEY]))

            svg.append('text')
                .attr('x', 30 + xOffset + i * (EVENT_WIDTH + GAP))
                .attr('y', baseY - (yOffset * (EVENT_HEIGHT + GAP)) + 30)
                .attr('stroke', 'black')
                .text(eventList[i][j][ACTIVITY_KEY])
        }
    }
}